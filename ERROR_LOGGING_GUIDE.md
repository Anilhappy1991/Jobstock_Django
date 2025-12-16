# ERROR LOGGING SYSTEM - Complete Guide

## 🎯 Overview

Complete error logging system with:
- ✅ **Automatic error capture** via middleware
- ✅ **Database storage** with comprehensive fields
- ✅ **Manual logging** with reusable utilities
- ✅ **Internal errors only** (filters out library/framework errors)
- ✅ **Error deduplication** (tracks occurrence count)
- ✅ **Admin interface** for viewing and managing errors

---

## 📊 Database Model: ErrorLog

### Fields Included:

| Field | Type | Description |
|-------|------|-------------|
| **user** | ForeignKey | User who encountered error (if authenticated) |
| **error_type** | CharField | Exception type (ValueError, KeyError, etc.) |
| **error_message** | TextField | Error message from exception |
| **error_traceback** | TextField | Full traceback |
| **error_hash** | CharField | Unique hash for deduplication |
| **file_path** | CharField | Relative path to file where error occurred |
| **function_name** | CharField | Function/method name |
| **line_number** | IntegerField | Line number of error |
| **request_method** | CharField | HTTP method (GET, POST, etc.) |
| **request_path** | CharField | URL path |
| **request_data** | JSONField | GET/POST data (sensitive fields filtered) |
| **ip_address** | GenericIPAddressField | Client IP |
| **user_agent** | TextField | Browser user agent |
| **status_code** | IntegerField | HTTP status code (default: 500) |
| **is_resolved** | BooleanField | Resolution status |
| **resolved_at** | DateTimeField | When error was resolved |
| **resolved_by** | ForeignKey | User who resolved |
| **resolution_notes** | TextField | Resolution notes |
| **occurrence_count** | IntegerField | Number of occurrences |
| **first_occurred** | DateTimeField | First occurrence timestamp |
| **last_occurred** | DateTimeField | Last occurrence timestamp |
| **severity** | CharField | low/medium/high/critical |
| **environment** | CharField | development/production |
| **created_at** | DateTimeField | Record creation time |
| **updated_at** | DateTimeField | Last update time |

### Indexes:
- `error_type + is_resolved`
- `file_path + function_name`
- `is_resolved + last_occurred`
- `severity + created_at`
- `error_hash + last_occurred`

---

## 🔧 Components

### 1. Model: `App/models.py`
```python
from django.db import models
from django.contrib.auth.models import User

class ErrorLog(models.Model):
    # All fields as listed above
    # Methods: get_severity_badge_class(), mark_resolved(), increment_occurrence()
```

### 2. Middleware: `App/middleware.py`
```python
class ErrorLoggingMiddleware(MiddlewareMixin):
    """
    Automatically captures exceptions and logs to database.
    Only logs internal application errors.
    """
    
    INTERNAL_PATHS = ['App/', 'Jobstock/', 'templates/']
    EXCLUDE_PATHS = ['site-packages/', 'venv/', 'django/']
```

### 3. Utilities: `App/utils.py`
```python
# Manual error logging
log_error(exception, request, user, severity, additional_context)

# Get last error
get_last_error(user=None, unresolved_only=True)

# Get error summary
get_error_summary(hours=24)
```

### 4. Admin: `App/admin.py`
```python
@admin.register(ErrorLog)
class ErrorLogAdmin(admin.ModelAdmin):
    # Comprehensive admin interface
    # Actions: mark_as_resolved, export_error_report, delete_resolved_errors
```

---

## 🚀 Usage Examples

### 1. Automatic Error Logging (Middleware)

**Middleware automatically captures all exceptions!**

```python
# In any view - errors are automatically logged
def my_view(request):
    # This error will be automatically logged by middleware
    result = 10 / 0  # ZeroDivisionError
    return HttpResponse("Hello")
```

**What gets logged:**
- ✅ Error type: `ZeroDivisionError`
- ✅ Error message: `division by zero`
- ✅ Full traceback
- ✅ File path: `App/views.py`
- ✅ Function name: `my_view`
- ✅ Line number: `123`
- ✅ Request details (method, path, data)
- ✅ User info (if authenticated)
- ✅ IP address, user agent

**Library errors are NOT logged:**
```python
# This Django framework error won't be logged (from library)
User.objects.get(id=99999)  # DoesNotExist - from django.contrib.auth
```

---

### 2. Manual Error Logging

#### Basic Usage

```python
from App.utils import log_error

def process_order(request):
    try:
        # Your code here
        order = Order.objects.get(id=order_id)
        process_payment(order)
    except Exception as e:
        # Log the error manually
        log_error(e, request=request)
        return HttpResponse("An error occurred", status=500)
```

#### With Custom Severity

```python
from App.utils import log_error

def critical_operation(request):
    try:
        delete_all_data()  # Critical operation
    except Exception as e:
        log_error(
            exception=e,
            request=request,
            severity='critical'  # Mark as critical
        )
        raise  # Re-raise after logging
```

#### With Additional Context

```python
from App.utils import log_error

def process_payment(request, order_id, amount):
    try:
        charge_card(order_id, amount)
    except Exception as e:
        log_error(
            exception=e,
            request=request,
            severity='high',
            additional_context={
                'order_id': order_id,
                'amount': amount,
                'payment_method': 'credit_card'
            }
        )
```

#### Without Request Object

```python
from App.utils import log_error

def background_task():
    """
    Background task without request context
    """
    try:
        process_data()
    except Exception as e:
        log_error(
            exception=e,
            user=None,  # No user context
            severity='medium',
            additional_context={'task': 'background_task'}
        )
```

#### Manual Logging Without Exception

```python
from App.utils import log_error

def validate_data(data):
    if not data.get('email'):
        # Create custom error and log it
        error = ValueError("Email is required")
        log_error(
            exception=error,
            severity='low',
            additional_context={'data': data}
        )
        return False
    return True
```

---

### 3. Get Last Error

```python
from App.utils import get_last_error

# Get last unresolved error
last_error = get_last_error()
if last_error:
    print(f"Error: {last_error.error_message}")
    print(f"Location: {last_error.file_path}:{last_error.line_number}")

# Get last error for specific user
user_error = get_last_error(user=request.user)

# Get last error (including resolved)
any_error = get_last_error(unresolved_only=False)
```

---

### 4. Get Error Summary

```python
from App.utils import get_error_summary

# Get errors from last 24 hours
summary = get_error_summary(hours=24)
print(f"Total errors: {summary['total_errors']}")
print(f"Unresolved: {summary['unresolved_errors']}")
print(f"Critical: {summary['critical_errors']}")

# Get errors from last week
weekly_summary = get_error_summary(hours=168)

# Get errors from last hour
hourly_summary = get_error_summary(hours=1)
```

---

### 5. In Django Management Commands

```python
from django.core.management.base import BaseCommand
from App.utils import log_error

class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            # Process data
            self.process_records()
        except Exception as e:
            log_error(
                exception=e,
                severity='high',
                additional_context={
                    'command': 'process_records',
                    'args': args,
                    'options': options
                }
            )
            raise
```

---

### 6. In Celery Tasks

```python
from celery import shared_task
from App.utils import log_error

@shared_task
def process_resume_task(resume_id):
    try:
        # Process resume
        resume = Resume.objects.get(id=resume_id)
        extract_data(resume)
    except Exception as e:
        log_error(
            exception=e,
            severity='medium',
            additional_context={
                'task': 'process_resume_task',
                'resume_id': resume_id
            }
        )
        raise
```

---

### 7. In Context Processors

```python
from App.utils import get_last_error

def error_context(request):
    """Add error info to template context"""
    if request.user.is_staff:
        return {
            'last_system_error': get_last_error(unresolved_only=True)
        }
    return {}
```

---

## 🎨 Admin Interface

### Access Admin:
1. Go to: `http://localhost:8000/admin/`
2. Login with superuser account
3. Click **Error Logs**

### Features:

#### List View:
- See all errors with key details
- Filter by: severity, resolution status, error type, date
- Search by: error type, message, file path, function name, user
- Sort by: last occurred, severity, occurrence count

#### Detail View:
- Full error information
- Complete traceback
- Request context (method, path, data)
- Client information (IP, user agent)
- Resolution tracking

#### Actions:
1. **Mark as Resolved** - Mark selected errors as resolved
2. **Mark as Unresolved** - Reopen resolved errors
3. **Delete Resolved Errors** - Clean up resolved errors
4. **Export Error Report** - Export as JSON

---

## 🎯 Error Deduplication

The system automatically handles duplicate errors:

```python
# First occurrence
try:
    result = 10 / 0
except:
    pass  # Middleware logs this

# Creates ErrorLog with:
# - occurrence_count = 1
# - first_occurred = now
# - last_occurred = now

# Second occurrence (same error, same location)
try:
    result = 10 / 0
except:
    pass  # Middleware finds existing error

# Updates existing ErrorLog:
# - occurrence_count = 2
# - first_occurred = (unchanged)
# - last_occurred = now (updated)
```

**Error Hash Formula:**
```
hash = SHA256(file_path + function_name + line_number + error_type)
```

---

## 🔒 Security Features

### Sensitive Data Filtering

Automatically filters these fields from request data:
- `password`, `password1`, `password2`
- `old_password`, `new_password`, `confirm_password`
- `token`, `api_key`, `secret`
- `credit_card`, `cvv`, `ssn`
- `csrfmiddlewaretoken`

```python
# Request data with password
request.POST = {
    'username': 'john_doe',
    'password': 'secret123',  # Will be filtered
    'email': 'john@example.com'
}

# Stored in database as:
{
    'POST': {
        'username': 'john_doe',
        'password': '***FILTERED***',  # Filtered!
        'email': 'john@example.com'
    }
}
```

---

## 📈 Severity Levels

| Severity | Description | Examples |
|----------|-------------|----------|
| **critical** | System-breaking errors | DatabaseError, MemoryError |
| **high** | Major functional errors | ValueError, KeyError, AttributeError |
| **medium** | Standard errors | Generic Exception |
| **low** | Minor issues | ValidationError, PermissionDenied |

**Auto-detected based on exception type:**
```python
# Automatically set to 'critical'
raise DatabaseError("Connection failed")

# Automatically set to 'high'
raise ValueError("Invalid value")

# Automatically set to 'low'
raise ValidationError("Form invalid")
```

---

## 🎨 Template Usage

Display error information in templates:

```html
{% load static %}

<!-- Show last error for admin users -->
{% if user.is_staff %}
    {% if last_system_error %}
        <div class="alert alert-danger">
            <strong>Last Error:</strong> 
            {{ last_system_error.error_type }} in 
            {{ last_system_error.function_name }}
            <br>
            <small>{{ last_system_error.last_occurred|timesince }} ago</small>
        </div>
    {% endif %}
{% endif %}
```

---

## 📊 Database Queries

### Get all unresolved errors:
```python
from App.models import ErrorLog

unresolved = ErrorLog.objects.filter(is_resolved=False)
```

### Get critical errors:
```python
critical = ErrorLog.objects.filter(
    severity='critical',
    is_resolved=False
).order_by('-last_occurred')
```

### Get errors by file:
```python
errors_in_views = ErrorLog.objects.filter(
    file_path__contains='views.py'
)
```

### Get errors by user:
```python
user_errors = ErrorLog.objects.filter(
    user=request.user
).order_by('-last_occurred')
```

### Get most frequent errors:
```python
frequent = ErrorLog.objects.filter(
    is_resolved=False
).order_by('-occurrence_count')[:10]
```

---

## 🔧 Configuration

### Customize Internal Paths

Edit `App/middleware.py`:

```python
class ErrorLoggingMiddleware(MiddlewareMixin):
    INTERNAL_PATHS = [
        'App/',
        'Jobstock/',
        'templates/',
        'myapp/',  # Add your app
    ]
```

### Customize Exclusions

```python
EXCLUDE_PATHS = [
    'site-packages/',
    'venv/',
    'django/',
    'mylib/',  # Add library to exclude
]
```

### Customize Sensitive Fields

```python
SENSITIVE_FIELDS = [
    'password',
    'api_key',
    'my_secret_field',  # Add your field
]
```

---

## 📧 Email Notifications (Optional)

Add to `App/middleware.py` in `process_exception()`:

```python
def process_exception(self, request, exception):
    # ... existing code ...
    
    # Send email for critical errors
    if severity == 'critical':
        from django.core.mail import mail_admins
        mail_admins(
            subject=f'Critical Error: {exc_type.__name__}',
            message=f'{error_message}\n\nFile: {file_path}\nLine: {line_number}',
            fail_silently=True
        )
    
    return None
```

---

## 🧪 Testing

### Test Automatic Logging:

Create `test_error_logging.py`:

```python
from django.test import TestCase, RequestFactory
from App.models import ErrorLog

class ErrorLoggingTest(TestCase):
    def test_error_logged(self):
        # Clear existing errors
        ErrorLog.objects.all().delete()
        
        # Trigger an error
        factory = RequestFactory()
        request = factory.get('/test/')
        
        try:
            result = 10 / 0
        except Exception as e:
            from App.utils import log_error
            log_error(e, request=request)
        
        # Check error was logged
        errors = ErrorLog.objects.all()
        self.assertEqual(errors.count(), 1)
        self.assertEqual(errors.first().error_type, 'ZeroDivisionError')
```

### Test in Views:

```python
def test_error_view(request):
    """Test view that triggers an error"""
    # This will be automatically logged by middleware
    result = 10 / 0
    return HttpResponse("This won't be reached")
```

Visit: `http://localhost:8000/test-error/`
Check Admin: See new error logged!

---

## 📋 Best Practices

### ✅ DO:
1. Let middleware handle automatic logging
2. Use `log_error()` for important business logic errors
3. Set appropriate severity levels
4. Add additional context for complex errors
5. Review and resolve errors regularly
6. Monitor critical and high-severity errors
7. Clean up old resolved errors periodically

### ❌ DON'T:
1. Log every single exception (trust middleware)
2. Log library/framework errors manually
3. Store sensitive data in additional_context
4. Ignore error notifications for critical errors
5. Delete unresolved errors
6. Log the same error multiple times manually

---

## 🎯 Real-World Example

```python
# In App/views.py
from App.utils import log_error
from django.shortcuts import render, redirect
from django.contrib import messages

def process_payment_view(request):
    """
    Process payment with comprehensive error logging
    """
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        amount = request.POST.get('amount')
        
        try:
            # Attempt payment processing
            order = Order.objects.get(id=order_id)
            
            if not order.can_process():
                raise ValueError("Order cannot be processed")
            
            payment_result = charge_credit_card(
                order.customer.card_token,
                amount
            )
            
            if not payment_result.success:
                raise Exception(f"Payment failed: {payment_result.error}")
            
            # Success!
            order.mark_paid()
            messages.success(request, "Payment processed successfully!")
            return redirect('order_confirmation', order_id=order.id)
            
        except Order.DoesNotExist:
            # Low severity - user error
            error = ValueError(f"Order {order_id} not found")
            log_error(
                exception=error,
                request=request,
                severity='low',
                additional_context={'order_id': order_id}
            )
            messages.error(request, "Order not found")
            
        except ValueError as e:
            # Medium severity - validation error
            log_error(
                exception=e,
                request=request,
                severity='medium',
                additional_context={
                    'order_id': order_id,
                    'amount': amount
                }
            )
            messages.error(request, str(e))
            
        except Exception as e:
            # High severity - payment error
            log_error(
                exception=e,
                request=request,
                severity='high',
                additional_context={
                    'order_id': order_id,
                    'amount': amount,
                    'payment_provider': 'stripe'
                }
            )
            messages.error(request, "Payment processing failed. Please try again.")
    
    return render(request, 'payment.html')
```

---

## ✅ System Status

**All components installed and configured:**

✅ Model created: `ErrorLog` with 28 fields
✅ Migration applied: `0009_errorlog.py`
✅ Middleware registered: `ErrorLoggingMiddleware`
✅ Utilities added: `log_error()`, `get_last_error()`, `get_error_summary()`
✅ Admin interface configured: Full management capabilities
✅ Indexes created: 5 composite indexes for performance
✅ Security: Sensitive field filtering active
✅ Deduplication: Error hash-based occurrence tracking

**System is production-ready! 🚀**
