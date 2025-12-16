"""
Generic utility functions and mixins for views
Reusable across all modules
"""
from django.contrib import messages
from django.shortcuts import redirect
from django.http import JsonResponse
from django.db import transaction
import json


class MessageMixin:
    """Mixin for handling messages consistently across views"""
    
    @staticmethod
    def success_message(request, message, extra_tags=''):
        """Add success message"""
        messages.success(request, message, extra_tags=extra_tags)
    
    @staticmethod
    def error_message(request, message, extra_tags=''):
        """Add error message"""
        messages.error(request, message, extra_tags=extra_tags)
    
    @staticmethod
    def info_message(request, message, extra_tags=''):
        """Add info message"""
        messages.info(request, message, extra_tags=extra_tags)
    
    @staticmethod
    def warning_message(request, message, extra_tags=''):
        """Add warning message"""
        messages.warning(request, message, extra_tags=extra_tags)


class FormHandlerMixin:
    """Generic form handling mixin"""
    
    @staticmethod
    def handle_form_save(form, request, success_message_text="Data saved successfully!", 
                        error_message_text="Error saving data. Please check the form.", 
                        return_json=False):
        """
        Generic form save handler
        
        Args:
            form: Django form instance
            request: HTTP request object
            success_message_text: Success message to display
            error_message_text: Error message to display
            return_json: Whether to return JSON response
        
        Returns:
            dict with 'success' boolean and 'message' string
        """
        if form.is_valid():
            try:
                with transaction.atomic():
                    instance = form.save()
                    
                if return_json:
                    return JsonResponse({
                        'success': True,
                        'message': success_message_text,
                        'data': {'id': instance.pk}
                    })
                else:
                    MessageMixin.success_message(request, success_message_text)
                    return {'success': True, 'message': success_message_text, 'instance': instance}
                    
            except Exception as e:
                error_msg = f"{error_message_text}: {str(e)}"
                if return_json:
                    return JsonResponse({
                        'success': False,
                        'message': error_msg
                    }, status=400)
                else:
                    MessageMixin.error_message(request, error_msg)
                    return {'success': False, 'message': error_msg}
        else:
            errors = form.errors.as_json()
            error_msg = f"{error_message_text} Please correct the errors."
            
            if return_json:
                return JsonResponse({
                    'success': False,
                    'message': error_msg,
                    'errors': json.loads(errors)
                }, status=400)
            else:
                MessageMixin.error_message(request, error_msg)
                return {'success': False, 'message': error_msg, 'errors': form.errors}
    
    @staticmethod
    def handle_multiple_forms(forms_dict, request, success_message="All data saved successfully!"):
        """
        Handle multiple forms at once
        
        Args:
            forms_dict: Dictionary of {form_name: form_instance}
            request: HTTP request object
            success_message: Success message to display
        
        Returns:
            dict with 'success' boolean and 'message' string
        """
        all_valid = all(form.is_valid() for form in forms_dict.values())
        
        if all_valid:
            try:
                with transaction.atomic():
                    saved_instances = {}
                    for form_name, form in forms_dict.items():
                        saved_instances[form_name] = form.save()
                    
                MessageMixin.success_message(request, success_message)
                return {
                    'success': True, 
                    'message': success_message,
                    'instances': saved_instances
                }
            except Exception as e:
                error_msg = f"Error saving data: {str(e)}"
                MessageMixin.error_message(request, error_msg)
                return {'success': False, 'message': error_msg}
        else:
            errors = {}
            for form_name, form in forms_dict.items():
                if not form.is_valid():
                    errors[form_name] = form.errors
            
            error_msg = "Please correct the errors in the form."
            MessageMixin.error_message(request, error_msg)
            return {'success': False, 'message': error_msg, 'errors': errors}


def generic_profile_save(request, form_class, profile_instance, success_message="Profile updated successfully!"):
    """
    Generic function to save profile data
    
    Args:
        request: HTTP request object
        form_class: Form class to use
        profile_instance: Profile instance to update
        success_message: Success message to display
    
    Returns:
        Tuple of (form_instance, success_boolean)
    """
    if request.method == 'POST':
        form = form_class(request.POST, request.FILES, instance=profile_instance)
        result = FormHandlerMixin.handle_form_save(
            form, request, 
            success_message_text=success_message
        )
        return form, result['success']
    else:
        form = form_class(instance=profile_instance)
        return form, False


def ajax_form_handler(request, form_class, instance=None, success_message="Data saved successfully!"):
    """
    Generic AJAX form handler
    
    Args:
        request: HTTP request object
        form_class: Form class to use
        instance: Model instance (for updates)
        success_message: Success message
    
    Returns:
        JsonResponse
    """
    if request.method == 'POST':
        form = form_class(request.POST, request.FILES, instance=instance)
        return FormHandlerMixin.handle_form_save(
            form, request,
            success_message_text=success_message,
            return_json=True
        )
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)


# ============================================================================
# ERROR LOGGING UTILITIES
# ============================================================================

import sys
import traceback
import hashlib
from django.conf import settings
from django.utils import timezone


def log_error(exception=None, request=None, user=None, severity='medium', 
              additional_context=None, file_path=None, function_name=None, line_number=None):
    """
    Generic error logging utility function.
    Can be called manually from any view or function to log errors.
    
    Args:
        exception: Exception object (optional, uses sys.exc_info() if not provided)
        request: HTTP request object (optional)
        user: User object (optional, overrides request.user)
        severity: Error severity ('low', 'medium', 'high', 'critical')
        additional_context: Dict with additional context to include
        file_path: Override file path (optional, auto-detected if not provided)
        function_name: Override function name (optional, auto-detected if not provided)
        line_number: Override line number (optional, auto-detected if not provided)
    
    Returns:
        ErrorLog instance if successful, None otherwise
    
    Example Usage:
        # Basic usage in try-except
        try:
            some_operation()
        except Exception as e:
            log_error(e, request=request)
        
        # With custom severity
        try:
            critical_operation()
        except Exception as e:
            log_error(e, request=request, severity='critical')
        
        # Manual logging without exception
        log_error(
            exception=ValueError("Custom error message"),
            user=request.user,
            severity='high',
            additional_context={'order_id': 123}
        )
    """
    try:
        # Import here to avoid circular imports
        from App.models import ErrorLog
        
        # Get exception information
        if exception is None:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            if exc_type is None:
                return None
        else:
            exc_type = type(exception)
            exc_value = exception
            exc_traceback = exception.__traceback__ if hasattr(exception, '__traceback__') else sys.exc_info()[2]
        
        # Get error details
        error_type = exc_type.__name__ if exc_type else 'UnknownError'
        error_message = str(exc_value) if exc_value else 'No error message'
        
        # Get traceback
        if exc_traceback:
            tb_lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
            error_traceback = ''.join(tb_lines)
            
            # Extract internal frame if not provided
            if not all([file_path, function_name, line_number]):
                internal_frame = _get_internal_frame_from_traceback(exc_traceback)
                if internal_frame:
                    if not file_path:
                        file_path = _get_relative_path(internal_frame.f_code.co_filename)
                    if not function_name:
                        function_name = internal_frame.f_code.co_name
                    if not line_number:
                        line_number = internal_frame.f_lineno
        else:
            error_traceback = f"{error_type}: {error_message}"
        
        # Set defaults if still not set
        if not function_name:
            function_name = 'unknown'
        if not file_path:
            file_path = 'unknown'
        if not line_number:
            line_number = 0
        
        # Generate error hash
        error_hash = _generate_error_hash(file_path, function_name, line_number, error_type)
        
        # Get user
        if not user and request and hasattr(request, 'user') and request.user.is_authenticated:
            user = request.user
        
        # Get request information
        request_data = {}
        request_method = None
        request_path = None
        ip_address = None
        user_agent = None
        
        if request:
            request_method = request.method
            request_path = request.path[:2000]
            ip_address = _get_client_ip(request)
            user_agent = request.META.get('HTTP_USER_AGENT', '')[:2000]
            request_data = _get_safe_request_data(request)
        
        # Add additional context
        if additional_context:
            request_data['additional_context'] = additional_context
        
        # Check for existing error
        existing_error = ErrorLog.objects.filter(error_hash=error_hash).first()
        
        if existing_error:
            # Increment occurrence count
            existing_error.increment_occurrence()
            return existing_error
        else:
            # Create new error log
            error_log = ErrorLog.objects.create(
                user=user,
                error_type=error_type[:255],
                error_message=error_message[:5000],
                error_traceback=error_traceback[:10000],
                error_hash=error_hash,
                file_path=file_path[:500],
                function_name=function_name[:255],
                line_number=line_number,
                request_method=request_method,
                request_path=request_path,
                request_data=request_data,
                ip_address=ip_address,
                user_agent=user_agent,
                status_code=500,
                severity=severity,
                environment='production' if not settings.DEBUG else 'development',
            )
            return error_log
    
    except Exception as e:
        # If error logging fails, print to console
        print(f"Error logging utility failed: {e}")
        traceback.print_exc()
        return None


def _get_internal_frame_from_traceback(tb):
    """Extract first frame from internal application code"""
    internal_paths = ['App/', 'Jobstock/', 'templates/']
    exclude_paths = ['site-packages/', 'lib/python', 'venv/', 'venv0/', '__pycache__/']
    
    while tb is not None:
        frame = tb.tb_frame
        filename = frame.f_code.co_filename.replace('\\', '/')
        
        is_internal = any(path in filename for path in internal_paths)
        is_excluded = any(path in filename for path in exclude_paths)
        
        if is_internal and not is_excluded:
            return frame
        
        tb = tb.tb_next
    
    return None


def _get_relative_path(absolute_path):
    """Get path relative to project root"""
    try:
        base_dir = str(settings.BASE_DIR).replace('\\', '/')
        absolute_path = absolute_path.replace('\\', '/')
        
        if absolute_path.startswith(base_dir):
            return absolute_path[len(base_dir):].lstrip('/')
        return absolute_path
    except:
        return absolute_path


def _generate_error_hash(file_path, function_name, line_number, error_type):
    """Generate unique hash for error deduplication"""
    hash_string = f"{file_path}:{function_name}:{line_number}:{error_type}"
    return hashlib.sha256(hash_string.encode()).hexdigest()[:64]


def _get_safe_request_data(request):
    """Get request data with sensitive fields filtered"""
    sensitive_fields = [
        'password', 'password1', 'password2', 'old_password',
        'new_password', 'confirm_password', 'token', 'api_key',
        'secret', 'credit_card', 'cvv', 'ssn', 'csrfmiddlewaretoken'
    ]
    
    data = {}
    try:
        if request.GET:
            data['GET'] = {
                k: '***FILTERED***' if k.lower() in sensitive_fields else v
                for k, v in request.GET.items()
            }
        
        if request.POST:
            data['POST'] = {
                k: '***FILTERED***' if k.lower() in sensitive_fields else v
                for k, v in request.POST.items()
            }
        
        # Limit data size
        data_str = str(data)
        if len(data_str) > 5000:
            data = {'_truncated': True, 'size': len(data_str)}
    except:
        data = {'_error': 'Could not extract request data'}
    
    return data


def _get_client_ip(request):
    """Get client IP address from request"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_last_error(user=None, unresolved_only=True):
    """
    Get the last error from the database.
    
    Args:
        user: Filter by user (optional)
        unresolved_only: Only get unresolved errors (default: True)
    
    Returns:
        ErrorLog instance or None
    """
    try:
        from App.models import ErrorLog
        
        queryset = ErrorLog.objects.all()
        
        if user:
            queryset = queryset.filter(user=user)
        
        if unresolved_only:
            queryset = queryset.filter(is_resolved=False)
        
        return queryset.first()
    except:
        return None


def get_error_summary(hours=24):
    """
    Get summary of errors in the last N hours.
    
    Args:
        hours: Number of hours to look back (default: 24)
    
    Returns:
        Dict with error statistics
    """
    try:
        from App.models import ErrorLog
        from django.utils import timezone
        from datetime import timedelta
        
        since = timezone.now() - timedelta(hours=hours)
        errors = ErrorLog.objects.filter(last_occurred__gte=since)
        
        return {
            'total_errors': errors.count(),
            'unresolved_errors': errors.filter(is_resolved=False).count(),
            'critical_errors': errors.filter(severity='critical').count(),
            'high_severity_errors': errors.filter(severity='high').count(),
            'unique_errors': errors.values('error_hash').distinct().count(),
            'most_common_error': errors.order_by('-occurrence_count').first(),
        }
    except:
        return None

