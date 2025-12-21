"""
API Views for Navigation System
Provides REST endpoints for navigation data
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required

from App.services.navigation_service import NavigationService
from App.utils.response import ApiResponse


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_navigation(request):
    """
    Get navigation menu for the authenticated user
    
    Returns:
        JSON response with navigation structure based on user role
    
    Example Response:
        {
            "success": true,
            "status_code": 200,
            "message": "Navigation retrieved successfully",
            "data": {
                "navigation": [
                    {
                        "id": 1,
                        "name": "Main Menu",
                        "slug": "hm-main-menu",
                        "icon": "fas fa-bars",
                        "items": [...]
                    }
                ]
            }
        }
    """
    result = NavigationService.get_navigation_for_user(request.user)
    return JsonResponse(result, status=result['status_code'])


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_dashboard_widgets(request):
    """
    Get dashboard widgets for the authenticated user
    
    Returns:
        JSON response with widget configuration
    """
    result = NavigationService.get_dashboard_widgets(request.user)
    return JsonResponse(result, status=result['status_code'])


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_quick_actions(request):
    """
    Get quick action buttons for the authenticated user
    
    Returns:
        JSON response with quick actions
    """
    result = NavigationService.get_quick_actions(request.user)
    return JsonResponse(result, status=result['status_code'])


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_dashboard_preferences(request):
    """
    Update user's dashboard preferences
    
    Request Body:
        {
            "hidden_widgets": [1, 2, 3],
            "widget_order": {"1": 0, "2": 1}
        }
    
    Returns:
        JSON response with updated preferences
    """
    result = NavigationService.update_user_preferences(
        request.user,
        request.data
    )
    return JsonResponse(result, status=result['status_code'])


@login_required
@require_http_methods(["GET"])
def get_navigation_json(request):
    """
    Non-DRF endpoint for navigation (for templates without DRF setup)
    """
    result = NavigationService.get_navigation_for_user(request.user)
    return JsonResponse(result, status=result.get('status_code', 200))


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_navigation_stats(request):
    """
    Get navigation statistics for the user
    
    Returns:
        JSON with badge counts, notifications, etc.
    """
    result = NavigationService.get_navigation_stats(request.user)
    return JsonResponse(result, status=result['status_code'])
