"""
Menu API URL Configuration
"""
from django.urls import path
from App.views import api_menu_views

urlpatterns = [
    # Get hierarchical menu for authenticated user
    path('hierarchical/', api_menu_views.api_get_hierarchical_menu, name='api_get_hierarchical_menu'),
    
    # Validate menu structure
    path('validate/', api_menu_views.api_validate_menu_structure, name='api_validate_menu_structure'),
    
    # Get allowed roles
    path('allowed-roles/', api_menu_views.api_get_allowed_roles, name='api_get_allowed_roles'),
    
    # Check user menu access
    path('check-access/', api_menu_views.api_check_user_menu_access, name='api_check_user_menu_access'),
]
