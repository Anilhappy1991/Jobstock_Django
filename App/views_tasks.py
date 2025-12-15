"""
Views for triggering background tasks
Location: App/views_tasks.py

Add these views to your App/views.py or import them in urls.py
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from celery.result import AsyncResult
from .tasks import (
    process_resume_document,
    process_job_description,
    match_resume_to_jobs
)
from .models import Profile
import logging

logger = logging.getLogger(__name__)


@login_required
@require_http_methods(["POST"])
def trigger_resume_processing(request):
    """
    Trigger background processing of uploaded resume
    
    Usage: Call this after resume upload
    """
    try:
        profile = get_object_or_404(Profile, user=request.user)
        
        if not profile.resume:
            return JsonResponse({
                'success': False,
                'error': 'No resume found for this profile'
            }, status=400)
        
        # Get the file path
        resume_path = profile.resume.path
        
        # Trigger the background task
        task = process_resume_document.delay(resume_path, profile.id)
        
        logger.info(f"Resume processing task started: {task.id}")
        
        return JsonResponse({
            'success': True,
            'task_id': task.id,
            'message': 'Resume processing started in background',
            'status_url': f'/app/task-status/{task.id}/'
        })
        
    except Exception as e:
        logger.error(f"Error triggering resume processing: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@login_required
def check_task_status(request, task_id):
    """
    Check the status of a background task
    
    URL: /app/task-status/<task_id>/
    """
    try:
        task_result = AsyncResult(task_id)
        
        response_data = {
            'task_id': task_id,
            'status': task_result.state,
            'ready': task_result.ready(),
            'successful': task_result.successful() if task_result.ready() else None,
        }
        
        if task_result.state == 'PENDING':
            response_data['message'] = 'Task is waiting to be processed'
        elif task_result.state == 'PROCESSING':
            response_data['message'] = 'Task is being processed'
            response_data['current'] = task_result.info.get('status', '')
        elif task_result.state == 'SUCCESS':
            response_data['message'] = 'Task completed successfully'
            response_data['result'] = task_result.result
        elif task_result.state == 'FAILURE':
            response_data['message'] = 'Task failed'
            response_data['error'] = str(task_result.info)
        
        return JsonResponse(response_data)
        
    except Exception as e:
        logger.error(f"Error checking task status: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@login_required
def task_status_page(request, task_id):
    """
    Render a page to display task status
    
    URL: /app/task-status-page/<task_id>/
    """
    return render(request, 'pages/task_status.html', {
        'task_id': task_id
    })


@login_required
@require_http_methods(["POST"])
def trigger_job_matching(request):
    """
    Trigger background job matching for user's resume
    """
    try:
        profile = get_object_or_404(Profile, user=request.user)
        
        # Get job IDs to match against (customize this logic)
        job_ids = request.POST.getlist('job_ids', [])
        
        if not job_ids:
            # Match against all active jobs (example)
            job_ids = list(range(1, 11))  # Replace with actual job query
        
        # Trigger the background task
        task = match_resume_to_jobs.delay(profile.id, job_ids)
        
        logger.info(f"Job matching task started: {task.id}")
        
        return JsonResponse({
            'success': True,
            'task_id': task.id,
            'message': 'Job matching started in background',
            'status_url': f'/app/task-status/{task.id}/'
        })
        
    except Exception as e:
        logger.error(f"Error triggering job matching: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)
