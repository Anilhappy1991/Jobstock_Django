"""
Menu API Views
REST API endpoints for hierarchical navigation menu
"""
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from App.services.navigation_service import NavigationService
from App.services.menu_validation_service import MenuValidationService
from App.utils.response import ApiResponse
import logging

logger = logging.getLogger(__name__)


@login_required
@require_http_methods(["GET"])
def api_get_hierarchical_menu(request):
    """
    Get hierarchical multilevel menu for authenticated user
    
    GET /api/menu/hierarchical/
    
    Returns:
        JSON response with menu structure
    """
    try:
        # Validate user access
        validation_result = MenuValidationService.validate_user_access(request.user)
        
        if isinstance(validation_result, ApiResponse):
            if not validation_result.success:
                return JsonResponse(
                    validation_result.to_dict(),
                    status=validation_result.status_code
                )
        elif isinstance(validation_result, dict):
            if not validation_result.get('success'):
                return JsonResponse(
                    validation_result,
                    status=validation_result.get('status_code', 403)
                )
        
        # Get navigation
        service = NavigationService()
        nav_response = service.get_navigation_for_user(request.user)
        
        # Handle both ApiResponse object and dict
        if isinstance(nav_response, ApiResponse):
            return JsonResponse(
                nav_response.to_dict(),
                status=nav_response.status_code
            )
        else:
            # Dict format
            return JsonResponse(
                nav_response,
                status=nav_response.get('status_code', 200)
            )
        
    except Exception as e:
        logger.error(f"Error getting hierarchical menu: {str(e)}")
        error_response = ApiResponse.server_error(
            message="Failed to retrieve menu",
            error_details=str(e)
        )
        return JsonResponse(
            error_response.to_dict(),
            status=error_response.status_code
        )


@login_required
@require_http_methods(["GET"])
def api_validate_menu_structure(request):
    """
    Validate menu structure for circular references and depth
    
    GET /api/menu/validate/
    
    Query Parameters:
        - group_id: Optional group ID to validate
    
    Returns:
        JSON response with validation results
    """
    try:
        group_id = request.GET.get('group_id')
        if group_id:
            try:
                group_id = int(group_id)
            except ValueError:
                error_response = ApiResponse.bad_request(
                    message="Invalid group_id parameter"
                )
                return JsonResponse(
                    error_response.to_dict(),
                    status=error_response.status_code
                )
        
        validation_result = MenuValidationService.validate_menu_structure(group_id)
        
        if isinstance(validation_result, ApiResponse):
            return JsonResponse(
                validation_result.to_dict(),
                status=validation_result.status_code
            )
        else:
            return JsonResponse(
                validation_result,
                status=validation_result.get('status_code', 200)
            )
        
    except Exception as e:
        logger.error(f"Error validating menu structure: {str(e)}")
        error_response = ApiResponse.server_error(
            message="Failed to validate menu",
            error_details=str(e)
        )
        return JsonResponse(
            error_response.to_dict(),
            status=error_response.status_code
        )


@login_required
@require_http_methods(["GET"])
def api_get_allowed_roles(request):
    """
    Get list of roles allowed to access menu
    
    GET /api/menu/allowed-roles/
    
    Returns:
        JSON response with allowed roles list
    """
    try:
        result = MenuValidationService.get_allowed_roles()
        
        if isinstance(result, ApiResponse):
            return JsonResponse(
                result.to_dict(),
                status=result.status_code
            )
        else:
            return JsonResponse(
                result,
                status=result.get('status_code', 200)
            )
        
    except Exception as e:
        logger.error(f"Error getting allowed roles: {str(e)}")
        error_response = ApiResponse.server_error(
            message="Failed to get allowed roles",
            error_details=str(e)
        )
        return JsonResponse(
            error_response.to_dict(),
            status=error_response.status_code
        )


@login_required
@require_http_methods(["GET"])
def api_check_user_menu_access(request):
    """
    Check if current user has access to menu
    
    GET /api/menu/check-access/
    
    Returns:
        JSON response with access status
    """
    try:
        validation_result = MenuValidationService.validate_user_access(request.user)
        
        if isinstance(validation_result, ApiResponse):
            return JsonResponse(
                validation_result.to_dict(),
                status=validation_result.status_code
            )
        else:
            return JsonResponse(
                validation_result,
                status=validation_result.get('status_code', 200)
            )
        
    except Exception as e:
        logger.error(f"Error checking user access: {str(e)}")
        error_response = ApiResponse.server_error(
            message="Failed to check user access",
            error_details=str(e)
        )
        return JsonResponse(
            error_response.to_dict(),
            status=error_response.status_code
        )
