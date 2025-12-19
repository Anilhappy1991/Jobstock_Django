from django.shortcuts import render, get_object_or_404, redirect
from .models import Blog
from .models import Candidate
from .models import Employer
from .models import Job
from .models import DropdownGroup, DropdownMaster, ResumeProcessing
from .forms import (
    SignUpForm, CandidateProfileBasicForm, CandidateProfileContactForm,
    CandidateProfileSocialForm, CandidateResumeForm
)
from .utils import MessageMixin, FormHandlerMixin, generic_profile_save
from django.contrib.auth.models import User
from .models import Profile
from .forms import RoleAssignForm
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.core.management import call_command
import os
import subprocess
import sys
import threading

# Create your views here.

def index(request):
    return render(request, 'pages/index.html')

def home_2(request):
    return render(request, 'pages/home-2.html')

def home_3(request):
    return render(request, 'pages/home-3.html')

def home_4(request):
    return render(request, 'pages/home-4.html')

def home_5(request):
    return render(request, 'pages/home-5.html')

def home_6(request):
    return render(request, 'pages/home-6.html')

def home_7(request):
    return render(request, 'pages/home-7.html')

def home_8(request):
    return render(request, 'pages/home-8.html')

def home_9(request):
    return render(request, 'pages/home-9.html')

def home_10(request):
    return render(request, 'pages/home-10.html')

def home_11(request):
    return render(request, 'pages/home-11.html')

def home_12(request):
    return render(request, 'pages/home-12.html')

def grid_style_1(request):
    return render(request, 'pages/grid-style-1.html')

def grid_style_2(request):
    return render(request, 'pages/grid-style-2.html')

def grid_style_3(request):
    return render(request, 'pages/grid-style-3.html')

def grid_style_4(request):
    return render(request, 'pages/grid-style-4.html')

def grid_style_5(request):
    return render(request, 'pages/grid-style-5.html')

def full_job_grid_1(request):
    return render(request, 'pages/full-job-grid-1.html')

def full_job_grid_2(request):
    return render(request, 'pages/full-job-grid-2.html')

def list_style_1(request):
    return render(request, 'pages/list-style-1.html')

def list_style_2(request):
    return render(request, 'pages/list-style-2.html')

def list_style_3(request):
    return render(request, 'pages/list-style-3.html')

def full_job_list_1(request):
    return render(request, 'pages/full-job-list-1.html')

def full_job_list_2(request):
    return render(request, 'pages/full-job-list-2.html')

def half_map(request):
    return render(request, 'pages/half-map.html')

def half_map_2(request):
    return render(request, 'pages/half-map-2.html')

def half_map_3(request):
    return render(request, 'pages/half-map-3.html')

def half_map_list_1(request):
    return render(request, 'pages/half-map-list-1.html')

def half_map_list_2(request):
    return render(request, 'pages/half-map-list-2.html')

def candidate_grid_1(request):
    return render(request, 'pages/candidate-grid-1.html')

def candidate_grid_2(request):
    return render(request, 'pages/candidate-grid-2.html')

def candidate_list_1(request):
    return render(request, 'pages/candidate-list-1.html')

def candidate_list_2(request):
    return render(request, 'pages/candidate-list-2.html')

def candidate_half_map(request):
    return render(request, 'pages/candidate-half-map.html')

def candidate_half_map_list(request):
    return render(request, 'pages/candidate-half-map-list.html')

def single_layout_1(request):
    return render(request, 'pages/single-layout-1.html')

def single_layout_2(request):
    return render(request, 'pages/single-layout-2.html')

def single_layout_3(request):
    return render(request, 'pages/single-layout-3.html')

def single_layout_4(request):
    return render(request, 'pages/single-layout-4.html')

def single_layout_5(request):
    return render(request, 'pages/single-layout-5.html')

def single_layout_6(request):
    return render(request, 'pages/single-layout-6.html')

def candidate_list_or_default(request):
    # Get candidates from the database
    candidates = Candidate.objects.all()  # or any filter you need
    return render(request,'pages/candidate-detail.html', {'candidates': candidates})

def candidate_detail(request, title):
    candidate = get_object_or_404(Candidate, slug=title)  # Match the candidate by title (or slug, depending on how your model is set up)
    return render(request, 'pages/candidate-detail.html', {'candidate': candidate})

def candidate_detail_2(request):
    return render(request, 'pages/candidate-detail-2.html')

def candidate_detail_3(request):
    return render(request, 'pages/candidate-detail-3.html')

def advance_search(request):
    return render(request, 'pages/advance-search.html')

def candidate_dashboard(request):
    return render(request, 'pages/candidate-dashboard.html')

def candidate_profile(request):
    # Redirect to the profile detail for the current authenticated user
    if request.user.is_authenticated:
        return redirect('App:candidate_profile_detail', username=request.user.username)
    # If not authenticated, send them to the home page
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
        # Determine which form was submitted
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
                                    # Use Django's call_command for cleaner execution
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


def is_rpo_admin(user):
    if not user or not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    profile = Profile.objects.filter(user=user).first()
    return bool(profile and profile.role == 'rpo_admin')


def assign_roles(request):
    # Only RPO Admins (or superusers) can access
    if not is_rpo_admin(request.user):
        return HttpResponseForbidden('Forbidden')

    if request.method == 'POST':
        form = RoleAssignForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            role = form.cleaned_data['role']
            user = get_object_or_404(User, username=username)
            profile, _ = Profile.objects.get_or_create(user=user)
            profile.role = role
            profile.save()
            messages.success(request, f"Updated role for {username} to {dict(Profile.ROLE_CHOICES).get(role)}")
            return redirect('App:assign_roles')
    else:
        form = RoleAssignForm()

    users = User.objects.order_by('username').all()
    profiles = {p.user_id: p for p in Profile.objects.filter(user__in=users)}

    # prepare small list of (user, profile, form) tuples
    user_rows = []
    for u in users:
        p = profiles.get(u.id)
        initial = {'username': u.username, 'role': p.role if p else 'candidate'}
        frm = RoleAssignForm(initial=initial)
        user_rows.append((u, p, frm))

    return render(request, 'pages/assign-roles.html', {'user_rows': user_rows, 'form': form})


def assign_role_ajax(request):
    # JSON endpoint to update a user's role via AJAX
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    if not is_rpo_admin(request.user):
        return JsonResponse({'error': 'Forbidden'}, status=403)

    username = request.POST.get('username')
    role = request.POST.get('role')
    if not username or not role:
        return JsonResponse({'error': 'Missing parameters'}, status=400)

    # Validate role
    valid_roles = [r[0] for r in Profile.ROLE_CHOICES]
    if role not in valid_roles:
        return JsonResponse({'error': 'Invalid role'}, status=400)

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

    profile, _ = Profile.objects.get_or_create(user=user)
    profile.role = role
    profile.save()

    return JsonResponse({'ok': True, 'username': username, 'role': profile.role})

def candidate_resume(request):
    return render(request, 'pages/candidate-resume.html')

def candidate_applied_jobs(request):
    return render(request, 'pages/candidate-applied-jobs.html')

def candidate_alert_job(request):
    return render(request, 'pages/candidate-alert-job.html')

def candidate_saved_jobs(request):
    return render(request, 'pages/candidate-saved-jobs.html')

def candidate_follow_employers(request):
    return render(request, 'pages/candidate-follow-employers.html')

def candidate_messages(request):
    return render(request, 'pages/candidate-messages.html')

def candidate_change_password(request):
    return render(request, 'pages/candidate-change-password.html')

def candidate_delete_account(request):
    return render(request, 'pages/candidate-delete-account.html')

def employer_grid_1(request):
    return render(request, 'pages/employer-grid-1.html')

def employer_grid_2(request):
    return render(request, 'pages/employer-grid-2.html')

def employer_list_1(request):
    return render(request, 'pages/employer-list-1.html')

def employer_half_map(request):
    return render(request, 'pages/employer-half-map.html')

def employer_half_map_list(request):
    return render(request, 'pages/employer-half-map-list.html')

def employer_list_or_default(request):
    # Get employers from the database
    employers = Employer.objects.all()  # or any filter you need
    return render(request,'pages/employer-detail.html', {'employers': employers})

def employer_detail(request, title):
    employer = get_object_or_404(Employer, slug=title)  # Match the employer by title (or slug, depending on how your model is set up)
    return render(request, 'pages/employer-detail.html', {'employer': employer})

def employer_detail_2(request):
    return render(request, 'pages/employer-detail-2.html')

def employer_dashboard(request):
    return render(request, 'pages/employer-dashboard.html')

def employer_profile(request):
    return render(request, 'pages/employer-profile.html')

def employer_jobs(request):
    return render(request, 'pages/employer-jobs.html')

@login_required
def employer_submit_job(request):
    import logging
    logger = logging.getLogger(__name__)
    
    # ===== DEBUG BREAKPOINT START =====
    logger.info("="*80)
    logger.info("EMPLOYER SUBMIT JOB VIEW CALLED")
    logger.info(f"Method: {request.method}")
    logger.info(f"User: {request.user.username}")
    logger.info(f"Authenticated: {request.user.is_authenticated}")
    # ===== DEBUG BREAKPOINT END =====
    
    # Fetch all dropdown groups with their items
    dropdown_groups = DropdownGroup.objects.filter(is_active=True).prefetch_related('items')
    
    # Create a dictionary of dropdowns for easy access in template
    dropdowns = {}
    for group in dropdown_groups:
        dropdowns[group.value] = group.items.filter(is_active=True).order_by('sort_order', 'text')
    
    if request.method == 'POST':
        # ===== DEBUG BREAKPOINT START =====
        logger.info("-"*80)
        logger.info("POST REQUEST RECEIVED - FORM SUBMITTED")
        logger.info("POST Data:")
        for key, value in request.POST.items():
            if key != 'csrfmiddlewaretoken':
                logger.info(f"  {key}: {value[:100] if len(str(value)) > 100 else value}")
        
        if request.FILES:
            logger.info("FILES Uploaded:")
            for key, file in request.FILES.items():
                logger.info(f"  {key}: {file.name} ({file.size} bytes)")
        # ===== DEBUG BREAKPOINT END =====
        
        try:
            # Get dropdown master objects
            def get_dropdown_item(field_name):
                value = request.POST.get(field_name)
                if value:
                    try:
                        return DropdownMaster.objects.get(value=value)
                    except DropdownMaster.DoesNotExist:
                        logger.warning(f"DropdownMaster not found for {field_name}: {value}")
                        return None
                return None
            
            # ===== DEBUG BREAKPOINT START =====
            logger.info("-"*80)
            logger.info("CREATING JOB OBJECT")
            # ===== DEBUG BREAKPOINT END =====
            
            # Create the job
            job = Job()
            job.title = request.POST.get('job_title', '')
            job.job_summary = request.POST.get('job_summary', '')
            job.responsibilities = request.POST.get('responsibilities', '')
            job.qualifications = request.POST.get('qualifications', '')
            
            logger.info(f"Job Title: {job.title}")
            
            # Handle file upload
            if 'company_logo' in request.FILES:
                job.company_logo = request.FILES['company_logo']
                logger.info(f"Company Logo: {job.company_logo.name}")
            
            # Dropdown fields
            job.job_category = get_dropdown_item('job_category')
            job.job_type = get_dropdown_item('job_type')
            job.job_level = get_dropdown_item('job_level')
            job.experience_required = get_dropdown_item('experience')
            job.qualification_required = get_dropdown_item('qualification')
            job.gender_preference = get_dropdown_item('gender')
            job.total_openings = get_dropdown_item('total_openings')
            job.job_fee_type = get_dropdown_item('job_fee_type')
            job.country = get_dropdown_item('country')
            job.state_city = get_dropdown_item('state_city')
            
            # Salary
            min_sal = request.POST.get('min_salary', '').replace('$', '').replace(',', '').strip()
            max_sal = request.POST.get('max_salary', '').replace('$', '').replace(',', '').strip()
            job.min_salary = min_sal if min_sal else None
            job.max_salary = max_sal if max_sal else None
            
            logger.info(f"Salary Range: ${job.min_salary} - ${job.max_salary}")
            
            # Dates
            start_date = request.POST.get('start_date', '').strip()
            deadline = request.POST.get('deadline', '').strip()
            job.start_date = start_date if start_date else None
            job.deadline = deadline if deadline else None
            
            # Other fields
            job.skills = request.POST.get('skills', '')
            job.permanent_address = request.POST.get('permanent_address', '')
            job.temporary_address = request.POST.get('temporary_address', '')
            job.zip_code = request.POST.get('zip_code', '')
            job.video_url = request.POST.get('video_url', '')
            
            # Location coordinates
            lat = request.POST.get('latitude', '').strip()
            lon = request.POST.get('longitude', '').strip()
            job.latitude = lat if lat else None
            job.longitude = lon if lon else None
            
            # Set posted by
            job.posted_by = request.user
            job.is_active = True
            
            # ===== DEBUG BREAKPOINT START =====
            logger.info("-"*80)
            logger.info("SAVING JOB TO DATABASE")
            # ===== DEBUG BREAKPOINT END =====
            
            job.save()
            
            # ===== DEBUG BREAKPOINT START =====
            logger.info(f"✓ JOB SAVED SUCCESSFULLY - ID: {job.id}")
            logger.info("="*80)
            # ===== DEBUG BREAKPOINT END =====
            
            messages.success(request, f'Job "{job.title}" has been posted successfully!')
            return redirect('App:employer_jobs')
            
        except Exception as e:
            # ===== DEBUG BREAKPOINT START =====
            logger.error("-"*80)
            logger.error(f"✗ ERROR OCCURRED: {str(e)}")
            logger.error(f"Exception Type: {type(e).__name__}")
            import traceback
            logger.error(f"Traceback:\n{traceback.format_exc()}")
            logger.error("="*80)
            # ===== DEBUG BREAKPOINT END =====
            messages.error(request, f'Error posting job: {str(e)}')
    
    context = {
        'dropdowns': dropdowns,
    }
    return render(request, 'pages/employer-submit-job.html', context)

def employer_applicants_jobs(request):
    return render(request, 'pages/employer-applicants-jobs.html')

def employer_shortlist_candidates(request):
    return render(request, 'pages/employer-shortlist-candidates.html')

def employer_package(request):
    return render(request, 'pages/employer-package.html')

def employer_messages(request):
    return render(request, 'pages/employer-messages.html')

def employer_change_password(request):
    return render(request, 'pages/employer-change-password.html')

def employer_delete_account(request):
    return render(request, 'pages/employer-delete-account.html')

def about_us(request):
    return render(request, 'pages/about-us.html')

def notFound(request):
    return render(request, 'pages/404.html')

def checkout(request):
    return render(request, 'pages/checkout.html')

def blog(request):
    return render(request, 'pages/blog.html')

def blog_list_or_default(request):
    # Get blogs from the database
    blogs = Blog.objects.all()  # or any filter you need
    return render(request,'pages/blog-detail.html', {'blogs': blogs})

def blog_detail(request, title):
    blog = get_object_or_404(Blog, slug=title)  # Match the blog by title (or slug, depending on how your model is set up)
    return render(request, 'pages/blog-detail.html', {'blog': blog})

def privacy(request):
    return render(request, 'pages/privacy.html')

def pricing(request):
    return render(request, 'pages/pricing.html')

def faq(request):
    return render(request, 'pages/faq.html')

def contact(request):
    return render(request, 'pages/contact.html')

def help(request):
    return render(request, 'pages/help.html')

def job_list_or_default(request):
    # Get jobs from the database
    jobs = Job.objects.all()  # or any filter you need
    return render(request,'pages/job-detail.html', {'jobs': jobs})

def job_detail(request, title):
    job = get_object_or_404(Job, slug=title)  # Match the job by title (or slug, depending on how your model is set up)
    return render(request, 'pages/job-detail.html', {'job': job})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully.')
            return redirect('App:candidate_profile_detail', username=user.username)
    else:
        form = SignUpForm()
    return render(request, 'pages/signup.html', {'form': form})

def slider_home(request):
    return render(request, 'pages/slider-home.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        # Try to use next from POST, fall back to HTTP_REFERER or index
        next_url = request.POST.get('next') or request.META.get('HTTP_REFERER') or reverse('App:index')
        if user is not None:
            login(request, user)
            messages.success(request, 'You are now logged in.')
            # Redirect to the user's profile using their email
            return redirect('App:candidate_profile_detail', username=user.email)
        else:
            messages.error(request, 'Invalid username or password.')
            # On failure, redirect to the same page and open login modal
            # Append ?login=failed so frontend can detect and open modal
            if '?' in next_url:
                return redirect(f"{next_url}&login=failed")
            return redirect(f"{next_url}?login=failed")
    # For GET or other, just redirect to index
    return redirect('App:index')


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('App:index')