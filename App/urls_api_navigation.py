"""
API URL Configuration for Navigation System
"""
from django.urls import path
from App.views.api_navigation_views import (
    get_user_navigation,
    get_dashboard_widgets,
    get_quick_actions,
    update_dashboard_preferences,
    get_navigation_json,
    get_navigation_stats,
)

app_name = 'navigation_api'

urlpatterns = [
    # Navigation endpoints
    path('navigation/', get_user_navigation, name='user_navigation'),
    path('navigation/stats/', get_navigation_stats, name='navigation_stats'),
    path('navigation/json/', get_navigation_json, name='navigation_json'),
    
    # Dashboard endpoints
    path('dashboard/widgets/', get_dashboard_widgets, name='dashboard_widgets'),
    path('dashboard/quick-actions/', get_quick_actions, name='quick_actions'),
    path('dashboard/preferences/', update_dashboard_preferences, name='update_preferences'),
]
