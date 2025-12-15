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
