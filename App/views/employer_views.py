"""
Employer-related views - Profile, jobs, applications, etc.
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from App.models import Employer, Job, DropdownGroup, DropdownMaster


def employer_grid_1(request):
    """Employer grid view 1"""
    return render(request, 'pages/employer-grid-1.html')


def employer_grid_2(request):
    """Employer grid view 2"""
    return render(request, 'pages/employer-grid-2.html')


def employer_list_1(request):
    """Employer list view 1"""
    return render(request, 'pages/employer-list-1.html')


def employer_half_map(request):
    """Employer half map view"""
    return render(request, 'pages/employer-half-map.html')


def employer_half_map_list(request):
    """Employer half map list view"""
    return render(request, 'pages/employer-half-map-list.html')


def employer_list_or_default(request):
    """Employer list or default view"""
    employers = Employer.objects.all()
    return render(request, 'pages/employer-detail.html', {'employers': employers})


def employer_detail(request, title):
    """Employer detail page by title/slug"""
    employer = get_object_or_404(Employer, slug=title)
    return render(request, 'pages/employer-detail.html', {'employer': employer})


def employer_detail_2(request):
    """Employer detail layout 2"""
    return render(request, 'pages/employer-detail-2.html')


def employer_dashboard(request):
    """Employer dashboard"""
    return render(request, 'pages/employer-dashboard.html')


def employer_profile(request):
    """Employer profile"""
    return render(request, 'pages/employer-profile.html')


def employer_jobs(request):
    """Employer jobs listing"""
    return render(request, 'pages/employer-jobs.html')


@login_required
def employer_submit_job(request):
    """Submit a new job posting"""
    # Fetch all dropdown groups with their items
    dropdown_groups = DropdownGroup.objects.filter(is_active=True).prefetch_related('items')
    
    # Create a dictionary of dropdowns for easy access in template
    dropdowns = {}
    for group in dropdown_groups:
        dropdowns[group.value] = group.items.filter(is_active=True).order_by('sort_order', 'text')
    
    if request.method == 'POST':
        try:
            def get_dropdown_item(field_name):
                """Helper function to get dropdown item"""
                value = request.POST.get(field_name)
                if value:
                    try:
                        return DropdownMaster.objects.get(value=value)
                    except DropdownMaster.DoesNotExist:
                        return None
                return None
            
            # Create the job
            job = Job()
            job.title = request.POST.get('job_title', '')
            job.job_summary = request.POST.get('job_summary', '')
            job.responsibilities = request.POST.get('responsibilities', '')
            job.qualifications = request.POST.get('qualifications', '')
            
            # Handle file upload
            if 'company_logo' in request.FILES:
                job.company_logo = request.FILES['company_logo']
            
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
            
            job.save()
            
            messages.success(request, f'Job "{job.title}" has been posted successfully!')
            return redirect('App:employer_jobs')
            
        except Exception as e:
            messages.error(request, f'Error posting job: {str(e)}')
    
    context = {
        'dropdowns': dropdowns,
    }
    return render(request, 'pages/employer-submit-job.html', context)


def employer_applicants_jobs(request):
    """Employer applicants for jobs"""
    return render(request, 'pages/employer-applicants-jobs.html')


def employer_shortlist_candidates(request):
    """Employer shortlisted candidates"""
    return render(request, 'pages/employer-shortlist-candidates.html')


def employer_package(request):
    """Employer packages"""
    return render(request, 'pages/employer-package.html')


def employer_messages(request):
    """Employer messages"""
    return render(request, 'pages/employer-messages.html')


def employer_change_password(request):
    """Employer change password"""
    return render(request, 'pages/employer-change-password.html')


def employer_delete_account(request):
    """Employer delete account"""
    return render(request, 'pages/employer-delete-account.html')
