"""
Candidate-related views - Profile, dashboard, applications, etc.
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from django.core.management import call_command
import os
import threading

from App.models import Candidate, Profile, DropdownMaster, ResumeProcessing
from App.forms import (
    CandidateProfileBasicForm,
    CandidateProfileContactForm,
    CandidateProfileSocialForm,
    CandidateResumeForm
)
from App.utils import MessageMixin


def candidate_grid_1(request):
    """Candidate grid view 1"""
    return render(request, 'pages/candidate-grid-1.html')


def candidate_grid_2(request):
    """Candidate grid view 2"""
    return render(request, 'pages/candidate-grid-2.html')


def candidate_list_1(request):
    """Candidate list view 1"""
    return render(request, 'pages/candidate-list-1.html')


def candidate_list_2(request):
    """Candidate list view 2"""
    return render(request, 'pages/candidate-list-2.html')


def candidate_half_map(request):
    """Candidate half map view"""
    return render(request, 'pages/candidate-half-map.html')


def candidate_half_map_list(request):
    """Candidate half map list view"""
    return render(request, 'pages/candidate-half-map-list.html')


def candidate_list_or_default(request):
    """Candidate list or default view"""
    candidates = Candidate.objects.all()
    return render(request, 'pages/candidate-detail.html', {'candidates': candidates})


def candidate_detail(request, title):
    """Candidate detail page by title/slug"""
    candidate = get_object_or_404(Candidate, slug=title)
    return render(request, 'pages/candidate-detail.html', {'candidate': candidate})


def candidate_detail_2(request):
    """Candidate detail layout 2"""
    return render(request, 'pages/candidate-detail-2.html')


def candidate_detail_3(request):
    """Candidate detail layout 3"""
    return render(request, 'pages/candidate-detail-3.html')


def candidate_dashboard(request):
    """Candidate dashboard"""
    return render(request, 'pages/candidate-dashboard.html')


def candidate_profile(request):
    """Redirect to current user's profile"""
    if request.user.is_authenticated:
        return redirect('App:candidate_profile_detail', username=request.user.username)
    return redirect('App:index')


@login_required
def candidate_profile_detail(request, username):
    """Show and update the profile for the given username"""
    user = get_object_or_404(User, username=username)
    profile, created = Profile.objects.get_or_create(user=user)
    
    # Prevent users from editing other users' profiles
    if request.user != user and not request.user.is_staff:
        MessageMixin.error_message(request, "You don't have permission to edit this profile.")
        return redirect('App:candidate_profile')
    
    # Handle resume deletion
    if request.GET.get('delete_resume') == 'true':
        if profile.resume:
            if os.path.isfile(profile.resume.path):
                os.remove(profile.resume.path)
            profile.resume = None
            profile.save()
            MessageMixin.success_message(request, "Resume deleted successfully!")
        return redirect('App:candidate_profile_detail', username=username)
    
    # Handle form submissions
    saved = False
    if request.method == 'POST':
        form_type = request.POST.get('form_type', 'basic')
        
        try:
            with transaction.atomic():
                if form_type == 'basic':
                    form_basic = CandidateProfileBasicForm(request.POST, instance=profile)
                    if form_basic.is_valid():
                        form_basic.save()
                        MessageMixin.success_message(request, "Basic information updated successfully!")
                        saved = True
                    else:
                        MessageMixin.error_message(request, "Please correct the errors in basic information.")
                
                elif form_type == 'contact':
                    form_contact = CandidateProfileContactForm(request.POST, instance=profile)
                    if form_contact.is_valid():
                        form_contact.save()
                        MessageMixin.success_message(request, "Contact details updated successfully!")
                        saved = True
                    else:
                        MessageMixin.error_message(request, "Please correct the errors in contact details.")
                
                elif form_type == 'social':
                    form_social = CandidateProfileSocialForm(request.POST, instance=profile)
                    if form_social.is_valid():
                        form_social.save()
                        MessageMixin.success_message(request, "Social links updated successfully!")
                        saved = True
                    else:
                        MessageMixin.error_message(request, "Please correct the errors in social links.")
                
                elif form_type == 'resume':
                    form_resume = CandidateResumeForm(request.POST, request.FILES, instance=profile)
                    if form_resume.is_valid():
                        # Delete old resume if exists and new one is uploaded
                        if 'resume' in request.FILES and profile.resume:
                            if os.path.isfile(profile.resume.path):
                                os.remove(profile.resume.path)
                        
                        # Save the resume file
                        saved_profile = form_resume.save()
                        
                        # Create ResumeProcessing entry for the new upload
                        if 'resume' in request.FILES:
                            resume_file = request.FILES['resume']
                            resume_record = ResumeProcessing.objects.create(
                                user=request.user,
                                profile=profile,
                                resume_path=saved_profile.resume.path if saved_profile.resume else '',
                                original_filename=resume_file.name,
                                file_size=resume_file.size,
                                file_extension=os.path.splitext(resume_file.name)[1].lower(),
                                status='pending'
                            )
                            
                            # Trigger automatic processing in background thread
                            def process_in_background():
                                try:
                                    call_command('process_resumes', user=request.user.username, verbosity=0)
                                except Exception as e:
                                    print(f"Background processing error: {e}")
                            
                            # Start processing in background thread
                            thread = threading.Thread(target=process_in_background, daemon=True)
                            thread.start()
                        
                        MessageMixin.success_message(request, "Resume uploaded successfully! Processing started in background.")
                        saved = True
                    else:
                        MessageMixin.error_message(request, "Please correct the errors in resume upload.")
                
                # If saved successfully, redirect to refresh the page
                if saved:
                    return redirect('App:candidate_profile_detail', username=username)
                    
        except Exception as e:
            MessageMixin.error_message(request, f"An error occurred: {str(e)}")
    
    # Initialize forms
    form_basic = CandidateProfileBasicForm(instance=profile)
    form_contact = CandidateProfileContactForm(instance=profile)
    form_social = CandidateProfileSocialForm(instance=profile)
    form_resume = CandidateResumeForm(instance=profile)
    
    # Get all dropdown items for the template
    education_items = DropdownMaster.objects.filter(group__text='Education', is_active=True)
    experience_items = DropdownMaster.objects.filter(group__text='Experience', is_active=True)
    country_items = DropdownMaster.objects.filter(group__text='Country', is_active=True)
    city_items = DropdownMaster.objects.filter(group__text='State/City', is_active=True)
    
    # Get resume processing history for this user
    resume_processing_records = ResumeProcessing.objects.filter(user=user).order_by('-created_at')[:5]
    latest_resume_processing = resume_processing_records.first() if resume_processing_records else None
    
    context = {
        'profile_user': user,
        'profile': profile,
        'form_basic': form_basic,
        'form_contact': form_contact,
        'form_social': form_social,
        'form_resume': form_resume,
        'education_items': education_items,
        'experience_items': experience_items,
        'country_items': country_items,
        'city_items': city_items,
        'profile_completion': profile.profile_completion,
        'resume_processing_records': resume_processing_records,
        'latest_resume_processing': latest_resume_processing,
    }
    
    return render(request, 'pages/candidate-profile.html', context)


def candidate_resume(request):
    """Candidate resume management"""
    return render(request, 'pages/candidate-resume.html')


def candidate_applied_jobs(request):
    """Candidate applied jobs"""
    return render(request, 'pages/candidate-applied-jobs.html')


def candidate_alert_job(request):
    """Candidate job alerts"""
    return render(request, 'pages/candidate-alert-job.html')


def candidate_saved_jobs(request):
    """Candidate saved jobs"""
    return render(request, 'pages/candidate-saved-jobs.html')


def candidate_follow_employers(request):
    """Candidate followed employers"""
    return render(request, 'pages/candidate-follow-employers.html')


def candidate_messages(request):
    """Candidate messages"""
    return render(request, 'pages/candidate-messages.html')


def candidate_change_password(request):
    """Candidate change password"""
    return render(request, 'pages/candidate-change-password.html')


def candidate_delete_account(request):
    """Candidate delete account"""
    return render(request, 'pages/candidate-delete-account.html')
