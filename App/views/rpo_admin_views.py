"""
RPO Admin Dashboard Views
Following MVT pattern with service layer integration
"""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from App.services.resume_upload_service import ResumeUploadService
from App.utils.response import ApiResponse


@login_required
@require_http_methods(["GET", "POST"])
def rpo_resume_upload(request):
    """
    RPO Admin Resume Upload Page
    GET: Display upload form with statistics
    POST: Handle multiple resume uploads
    """
    # Check if user is RPO Admin
    user_role = request.user.profile.role if hasattr(request.user, 'profile') else 'unknown'
    is_rpo_admin = user_role == 'rpo_admin' or request.user.groups.filter(name='rpo_admin').exists()
    
    if not is_rpo_admin and not request.user.is_superuser:
        messages.error(request, 'Access denied. RPO Admin role required.')
        return redirect('App:index')
    
    if request.method == 'POST':
        # Handle file upload
        files = request.FILES.getlist('resumes')
        
        if not files:
            messages.error(request, 'Please select at least one resume file to upload')
            return redirect('App:rpo_resume_upload')
        
        # Use service to upload resumes
        result = ResumeUploadService.upload_resumes(files, request.user)
        
        if result.success:
            messages.success(request, result.message)
            if result.data['failed_count'] > 0:
                for failed in result.data['failed']:
                    messages.warning(request, f"{failed['filename']}: {failed['error']}")
        else:
            messages.error(request, result.message)
            if hasattr(result, 'error_details') and result.error_details:
                for failed in result.error_details.get('failed', []):
                    messages.error(request, f"{failed['filename']}: {failed['error']}")
        
        return redirect('App:rpo_resume_upload')
    
    # GET request - show upload form
    # Get user's resume statistics
    stats_response = ResumeUploadService.get_upload_statistics(request.user)
    stats = stats_response.data if stats_response.success else {}
    
    # Get recent uploads
    resumes_response = ResumeUploadService.get_user_resumes(request.user, limit=10)
    resumes = resumes_response.data.get('resumes', []) if resumes_response.success else []
    
    context = {
        'page_title': 'Resume Upload',
        'stats': stats,
        'recent_uploads': resumes,
        'allowed_extensions': ', '.join(ResumeUploadService.ALLOWED_EXTENSIONS),
        'max_file_size_mb': ResumeUploadService.MAX_FILE_SIZE / (1024 * 1024)
    }
    
    return render(request, 'Pages/RPO-Admin/resume_upload.html', context)


@login_required
def rpo_dashboard(request):
    """
    RPO Admin Dashboard
    Main dashboard page for RPO administrators
    """
    # Check if user is RPO Admin
    user_role = request.user.profile.role if hasattr(request.user, 'profile') else 'unknown'
    is_rpo_admin = user_role == 'rpo_admin' or request.user.groups.filter(name='rpo_admin').exists()
    
    if not is_rpo_admin and not request.user.is_superuser:
        messages.error(request, 'Access denied. RPO Admin role required.')
        return redirect('App:index')
    
    # Get dashboard statistics
    stats_response = ResumeUploadService.get_upload_statistics(request.user)
    stats = stats_response.data if stats_response.success else {}
    
    # Get recent uploads
    resumes_response = ResumeUploadService.get_user_resumes(request.user, limit=5)
    recent_resumes = resumes_response.data.get('resumes', []) if resumes_response.success else []
    
    context = {
        'page_title': 'RPO Admin Dashboard',
        'stats': stats,
        'recent_resumes': recent_resumes
    }
    
    return render(request, 'Pages/RPO-Admin/dashboard.html', context)


@login_required
def rpo_resume_list(request):
    """
    RPO Admin Resume List
    View all uploaded resumes with pagination
    """
    # Check if user is RPO Admin
    user_role = request.user.profile.role if hasattr(request.user, 'profile') else 'unknown'
    is_rpo_admin = user_role == 'rpo_admin' or request.user.groups.filter(name='rpo_admin').exists()
    
    if not is_rpo_admin and not request.user.is_superuser:
        messages.error(request, 'Access denied. RPO Admin role required.')
        return redirect('App:index')
    
    # Get pagination parameters
    limit = int(request.GET.get('limit', 20))
    offset = int(request.GET.get('offset', 0))
    
    # Get resumes from service
    resumes_response = ResumeUploadService.get_user_resumes(request.user, limit=limit, offset=offset)
    
    if resumes_response.success:
        resumes_data = resumes_response.data
        context = {
            'page_title': 'My Uploaded Resumes',
            'resumes': resumes_data.get('resumes', []),
            'total': resumes_data.get('total', 0),
            'limit': limit,
            'offset': offset,
            'has_next': (offset + limit) < resumes_data.get('total', 0),
            'has_prev': offset > 0,
            'next_offset': offset + limit,
            'prev_offset': max(0, offset - limit)
        }
    else:
        messages.error(request, resumes_response.message)
        context = {
            'page_title': 'My Uploaded Resumes',
            'resumes': [],
            'total': 0
        }
    
    return render(request, 'Pages/RPO-Admin/resume_list.html', context)


@login_required
def rpo_resume_view(request, resume_id):
    """
    View resume details
    """
    from App.models import ResumeProcessing
    from django.http import HttpResponseForbidden
    
    # Check if user is RPO Admin
    user_role = request.user.profile.role if hasattr(request.user, 'profile') else 'unknown'
    is_rpo_admin = user_role == 'rpo_admin' or request.user.groups.filter(name='rpo_admin').exists()
    
    if not is_rpo_admin and not request.user.is_superuser:
        return HttpResponseForbidden('Access denied. RPO Admin role required.')
    
    try:
        resume = ResumeProcessing.objects.get(id=resume_id, user=request.user)
        context = {
            'page_title': 'View Resume',
            'resume': resume
        }
        return render(request, 'Pages/RPO-Admin/resume_view.html', context)
    except ResumeProcessing.DoesNotExist:
        messages.error(request, 'Resume not found.')
        return redirect('App:rpo_resume_list')


@login_required
def rpo_resume_download(request, resume_id):
    """
    Download resume file
    """
    from App.models import ResumeProcessing
    from django.http import FileResponse, Http404, HttpResponseForbidden
    from django.conf import settings
    import os
    
    # Check if user is RPO Admin
    user_role = request.user.profile.role if hasattr(request.user, 'profile') else 'unknown'
    is_rpo_admin = user_role == 'rpo_admin' or request.user.groups.filter(name='rpo_admin').exists()
    
    if not is_rpo_admin and not request.user.is_superuser:
        return HttpResponseForbidden('Access denied. RPO Admin role required.')
    
    try:
        resume = ResumeProcessing.objects.get(id=resume_id, user=request.user)
        
        # Build absolute path from relative path stored in database
        if resume.resume_path.startswith('/') or resume.resume_path.startswith('\\'):
            # Remove leading slash if present
            resume.resume_path = resume.resume_path.lstrip('/\\')
        
        absolute_path = os.path.join(settings.BASE_DIR, resume.resume_path)
        
        if not os.path.exists(absolute_path):
            messages.error(request, 'Resume file not found.')
            return redirect('App:rpo_resume_list')
        
        # Open and return the file
        response = FileResponse(open(absolute_path, 'rb'))
        response['Content-Disposition'] = f'attachment; filename="{resume.original_filename}"'
        return response
        
    except ResumeProcessing.DoesNotExist:
        raise Http404("Resume not found")


@login_required
@require_http_methods(["POST"])
def rpo_process_resumes(request):
    """
    Process pending resumes (extract data, analyze, store in database)
    POST: Trigger processing for pending resumes
    """
    # Check if user is RPO Admin
    user_role = request.user.profile.role if hasattr(request.user, 'profile') else 'unknown'
    is_rpo_admin = user_role == 'rpo_admin' or request.user.groups.filter(name='rpo_admin').exists()
    
    if not is_rpo_admin and not request.user.is_superuser:
        messages.error(request, 'Access denied. RPO Admin role required.')
        return redirect('App:index')
    
    # Get specific resume IDs from request or process all pending
    resume_ids_str = request.POST.get('resume_ids', '')
    resume_ids = None
    
    if resume_ids_str:
        try:
            resume_ids = [int(id.strip()) for id in resume_ids_str.split(',') if id.strip()]
        except ValueError:
            messages.error(request, 'Invalid resume IDs format')
            return redirect(request.META.get('HTTP_REFERER', 'App:rpo_dashboard'))
    
    # Use service to process resumes
    result = ResumeUploadService.process_pending_resumes(request.user, resume_ids)
    
    if result.success:
        messages.success(request, result.message)
        
        # Show details of processing
        if result.data['failed'] > 0:
            messages.warning(
                request, 
                f"{result.data['failed']} resume(s) failed to process. Check resume list for details."
            )
    else:
        messages.error(request, result.message)
    
    # Redirect back to referring page or dashboard
    return redirect(request.META.get('HTTP_REFERER', 'App:rpo_dashboard'))


@login_required
@require_http_methods(["POST"])
def rpo_process_single_resume(request, resume_id):
    """
    Process a single resume
    POST: Trigger processing for one specific resume
    """
    # Check if user is RPO Admin
    user_role = request.user.profile.role if hasattr(request.user, 'profile') else 'unknown'
    is_rpo_admin = user_role == 'rpo_admin' or request.user.groups.filter(name='rpo_admin').exists()
    
    if not is_rpo_admin and not request.user.is_superuser:
        messages.error(request, 'Access denied. RPO Admin role required.')
        return redirect('App:index')
    
    # Use service to process single resume
    result = ResumeUploadService.process_single_resume(resume_id, request.user)
    
    if result.success:
        messages.success(request, result.message)
    else:
        messages.error(request, result.message)
    
    # Redirect back to referring page or resume view
    return redirect(request.META.get('HTTP_REFERER', 'App:rpo_resume_view', kwargs={'resume_id': resume_id}))
