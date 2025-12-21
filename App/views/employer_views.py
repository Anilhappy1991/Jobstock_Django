"""
Employer-related views - Profile, jobs, applications, etc.
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

from App.models import Employer, Job, DropdownGroup, DropdownMaster
from App.services import JobService


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


@login_required
def employer_jobs(request):
    """Employer jobs listing with search and pagination"""
    # 🔴 BREAKPOINT: Set VSCode breakpoint on the line below to debug when employer-jobs page is accessed
    # Get search query from request
    search_query = request.GET.get('search', '').strip()
    
    # DEBUG: Print current user
    print(f"🔍 DEBUG - Current User: {request.user.username}")
    
    # Get all jobs - superusers see ALL jobs, regular users see only THEIR jobs
    if request.user.is_superuser or request.user.is_staff:
        # Admins and staff see ALL jobs
        jobs = Job.objects.select_related(
            'job_category', 'job_type', 'job_level', 
            'experience_required', 'qualification_required', 'posted_by'
        ).order_by('-created_at')
        print(f"🔍 DEBUG - ADMIN VIEW: Showing ALL jobs")
    else:
        # Regular employers see only THEIR jobs
        jobs = Job.objects.filter(posted_by=request.user).select_related(
            'job_category', 'job_type', 'job_level', 
            'experience_required', 'qualification_required'
        ).order_by('-created_at')
        print(f"🔍 DEBUG - EMPLOYER VIEW: Showing only user's jobs")
    
    # DEBUG: Print query results
    print(f"🔍 DEBUG - Total Jobs Found: {jobs.count()}")
    print(f"🔍 DEBUG - Search Query: '{search_query}'")
    
    # Apply search filter if search query exists
    if search_query:
        jobs = jobs.filter(
            Q(title__icontains=search_query) |
            Q(job_category__text__icontains=search_query) |
            Q(job_type__text__icontains=search_query) |
            Q(job_level__text__icontains=search_query) |
            Q(skills__icontains=search_query) |
            Q(permanent_address__icontains=search_query) |
            Q(state_city__text__icontains=search_query)
        )
    
    # Get statistics
    stats = JobService.get_job_statistics(user=request.user)
    
    # Pagination - 10 jobs per page
    paginator = Paginator(jobs, 10)
    page = request.GET.get('page', 1)
    
    try:
        jobs_page = paginator.page(page)
    except PageNotAnInteger:
        jobs_page = paginator.page(1)
    except EmptyPage:
        jobs_page = paginator.page(paginator.num_pages)
    
    context = {
        'jobs': jobs_page,
        'stats': stats,
        'search_query': search_query,
        'total_jobs': paginator.count,
    }
    return render(request, 'pages/employer-jobs.html', context)


@login_required
def employer_submit_job(request, job_id=None):
    """Submit a new job posting or edit existing one"""
    # Get dropdown data
    dropdowns = JobService.get_dropdown_data()
    
    # Check if editing existing job
    job = None
    if job_id:
        try:
            job = JobService.get_job_by_id(job_id, user=request.user)
        except:
            messages.error(request, 'Job not found or you do not have permission to edit it.')
            return redirect('App:employer_jobs')
    
    if request.method == 'POST':
        try:
            # Prepare data dictionary
            data = {
                'job_title': request.POST.get('job_title', ''),
                'job_summary': request.POST.get('job_summary', ''),
                'responsibilities': request.POST.get('responsibilities', ''),
                'qualifications': request.POST.get('qualifications', ''),
                'job_category': request.POST.get('job_category'),
                'job_type': request.POST.get('job_type'),
                'job_level': request.POST.get('job_level'),
                'experience': request.POST.get('experience'),
                'qualification': request.POST.get('qualification'),
                'gender': request.POST.get('gender'),
                'total_openings': request.POST.get('total_openings'),
                'job_fee_type': request.POST.get('job_fee_type'),
                'country': request.POST.get('country'),
                'state_city': request.POST.get('state_city'),
                'min_salary': request.POST.get('min_salary', ''),
                'max_salary': request.POST.get('max_salary', ''),
                'start_date': request.POST.get('start_date', ''),
                'deadline': request.POST.get('deadline', ''),
                'skills': request.POST.get('skills', ''),
                'permanent_address': request.POST.get('permanent_address', ''),
                'temporary_address': request.POST.get('temporary_address', ''),
                'zip_code': request.POST.get('zip_code', ''),
                'video_url': request.POST.get('video_url', ''),
                'latitude': request.POST.get('latitude', ''),
                'longitude': request.POST.get('longitude', ''),
                'is_active': True,
            }
            
            # Handle file upload
            if 'company_logo' in request.FILES:
                data['company_logo'] = request.FILES['company_logo']
            
            # Create or update job using service layer
            if job_id:
                job = JobService.update_job(job_id, data, request.user)
                messages.success(request, f'Job "{job.title}" has been updated successfully!')
            else:
                job = JobService.create_job(data, request.user)
                messages.success(request, f'Job "{job.title}" has been posted successfully!')
            
            return redirect('App:employer_jobs')
            
        except Exception as e:
            messages.error(request, f'Error saving job: {str(e)}')
    
    context = {
        'dropdowns': dropdowns,
        'job': job,
        'is_edit': job is not None,
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


@login_required
@require_http_methods(["POST", "DELETE"])
def employer_delete_job(request, job_id):
    """Delete a job posting"""
    try:
        JobService.delete_job(job_id, request.user)
        messages.success(request, 'Job has been deleted successfully!')
        return JsonResponse({'success': True, 'message': 'Job deleted successfully'})
    except Exception as e:
        messages.error(request, f'Error deleting job: {str(e)}')
        return JsonResponse({'success': False, 'error': str(e)}, status=400)
