"""
Error Logging Middleware for Django Application
Automatically captures and logs internal errors to the database.
Filters out library/framework errors to focus on application code.
"""

import sys
import traceback
import hashlib
import os
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse, HttpResponse
from django.utils import timezone


class ErrorLoggingMiddleware(MiddlewareMixin):
    """
    Middleware to automatically log exceptions to the database.
    Only logs errors from internal application code (filters out library errors).
    """
    
    # Directories to consider as "internal" (application code)
    INTERNAL_PATHS = [
        'App/',
        'Jobstock/',
        'templates/',
    ]
    
    # Directories to exclude (library/framework code)
    EXCLUDE_PATHS = [
        'site-packages/',
        'lib/python',
        'venv/',
        'venv0/',
        'django/',
        'jazzmin/',
        'celery/',
        'rest_framework/',
        '__pycache__/',
    ]
    
    # Sensitive fields to filter from request data
    SENSITIVE_FIELDS = [
        'password',
        'password1',
        'password2',
        'old_password',
        'new_password',
        'confirm_password',
        'csrfmiddlewaretoken',
        'token',
        'api_key',
        'secret',
        'credit_card',
        'cvv',
        'ssn',
    ]
    
    def process_exception(self, request, exception):
        """
        Called when a view raises an exception.
        Logs the error if it's from internal application code.
        """
        try:
            # Get error details
            exc_type, exc_value, exc_traceback = sys.exc_info()
            
            # Extract internal frame from traceback
            internal_frame = self._get_internal_frame(exc_traceback)
            
            if not internal_frame:
                # Not an internal error, skip logging
                return None
            
            # Extract location details
            file_path = self._get_relative_path(internal_frame.f_code.co_filename)
            function_name = internal_frame.f_code.co_name
            line_number = internal_frame.f_lineno
            
            # Generate error hash for deduplication
            error_hash = self._generate_error_hash(
                file_path, function_name, line_number, exc_type.__name__
            )
            
            # Get full traceback
            tb_lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
            error_traceback = ''.join(tb_lines)
            
            # Extract request information
            request_data = self._get_safe_request_data(request)
            ip_address = self._get_client_ip(request)
            user_agent = request.META.get('HTTP_USER_AGENT', '')[:2000]
            
            # Determine severity based on exception type
            severity = self._determine_severity(exc_type)
            
            # Import here to avoid circular imports
            from App.models import ErrorLog
            
            # Check if this exact error already exists
            existing_error = ErrorLog.objects.filter(error_hash=error_hash).first()
            
            if existing_error:
                # Increment occurrence count
                existing_error.increment_occurrence()
            else:
                # Create new error log
                ErrorLog.objects.create(
                    user=request.user if request.user.is_authenticated else None,
                    error_type=exc_type.__name__,
                    error_message=str(exc_value)[:5000],
                    error_traceback=error_traceback[:10000],
                    error_hash=error_hash,
                    file_path=file_path,
                    function_name=function_name,
                    line_number=line_number,
                    request_method=request.method,
                    request_path=request.path[:2000],
                    request_data=request_data,
                    ip_address=ip_address,
                    user_agent=user_agent,
                    status_code=500,
                    severity=severity,
                    environment=self._get_environment(),
                )
            
        except Exception as e:
            # If error logging itself fails, print to console
            print(f"Error logging middleware failed: {e}")
            traceback.print_exc()
        
        # Return None to continue with normal exception handling
        return None
    
    def _get_internal_frame(self, tb):
        """
        Extract the first frame from internal application code.
        Skip frames from libraries and framework code.
        """
        while tb is not None:
            frame = tb.tb_frame
            filename = frame.f_code.co_filename
            
            # Normalize path separators
            filename = filename.replace('\\', '/')
            
            # Check if this is internal code
            is_internal = any(path in filename for path in self.INTERNAL_PATHS)
            is_excluded = any(path in filename for path in self.EXCLUDE_PATHS)
            
            if is_internal and not is_excluded:
                return frame
            
            tb = tb.tb_next
        
        return None
    
    def _get_relative_path(self, absolute_path):
        """Get path relative to project root"""
        try:
            base_dir = str(settings.BASE_DIR)
            absolute_path = absolute_path.replace('\\', '/')
            base_dir = base_dir.replace('\\', '/')
            
            if absolute_path.startswith(base_dir):
                return absolute_path[len(base_dir):].lstrip('/')
            return absolute_path
        except:
            return absolute_path
    
    def _generate_error_hash(self, file_path, function_name, line_number, error_type):
        """Generate unique hash for error deduplication"""
        hash_string = f"{file_path}:{function_name}:{line_number}:{error_type}"
        return hashlib.sha256(hash_string.encode()).hexdigest()[:64]
    
    def _get_safe_request_data(self, request):
        """Get request data with sensitive fields filtered"""
        data = {}
        
        try:
            # Get GET parameters
            if request.GET:
                data['GET'] = {
                    k: '***FILTERED***' if k.lower() in self.SENSITIVE_FIELDS else v
                    for k, v in request.GET.items()
                }
            
            # Get POST parameters
            if request.POST:
                data['POST'] = {
                    k: '***FILTERED***' if k.lower() in self.SENSITIVE_FIELDS else v
                    for k, v in request.POST.items()
                }
            
            # Limit data size
            data_str = str(data)
            if len(data_str) > 5000:
                data = {'_truncated': True, 'size': len(data_str)}
        
        except Exception:
            data = {'_error': 'Could not extract request data'}
        
        return data
    
    def _get_client_ip(self, request):
        """Get client IP address from request"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def _determine_severity(self, exc_type):
        """Determine error severity based on exception type"""
        critical_errors = [
            'DatabaseError',
            'OperationalError',
            'IntegrityError',
            'SystemError',
            'MemoryError',
        ]
        
        high_errors = [
            'ValueError',
            'KeyError',
            'AttributeError',
            'TypeError',
            'IndexError',
        ]
        
        low_errors = [
            'ValidationError',
            'PermissionDenied',
            'Http404',
        ]
        
        exc_name = exc_type.__name__
        
        if exc_name in critical_errors:
            return 'critical'
        elif exc_name in high_errors:
            return 'high'
        elif exc_name in low_errors:
            return 'low'
        else:
            return 'medium'
    
    def _get_environment(self):
        """Get current environment"""
        return 'production' if not settings.DEBUG else 'development'
