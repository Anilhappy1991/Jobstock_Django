"""
Menu Validation Service
Validates navigation menu structure, roles, and permissions
"""
from typing import Dict, Any, List, Optional
from django.contrib.auth.models import User
from django.urls import reverse, NoReverseMatch
from App.models import NavigationGroup, NavigationItem
from App.utils.response import ApiResponse
import logging

logger = logging.getLogger(__name__)


class MenuValidationService:
    """Service for validating menu structure and access"""
    
    # Allowed user roles (employee treated as hiring_manager)
    ALLOWED_ROLES = ['hiring_manager', 'rpo_admin', 'employee']
    
    # Role mapping: employee uses hiring_manager menu
    ROLE_MAPPING = {
        'employee': 'hiring_manager',
        'hiring_manager': 'hiring_manager',
        'rpo_admin': 'rpo_admin'
    }
    
    # Maximum menu depth to prevent infinite recursion
    MAX_MENU_DEPTH = 10
    
    @classmethod
    def get_mapped_role(cls, user_role: str) -> str:
        """
        Get the mapped role for menu display
        Employee role is mapped to hiring_manager
        
        Args:
            user_role: Original user role
            
        Returns:
            Mapped role string
        """
        return cls.ROLE_MAPPING.get(user_role, user_role)
    
    @classmethod
    def validate_user_access(cls, user: User) -> ApiResponse:
        """
        Validate if user has access to navigation menu
        
        Args:
            user: User object
            
        Returns:
            ApiResponse object
        """
        try:
            # Check if user is authenticated
            if not user or not user.is_authenticated:
                return ApiResponse.unauthorized(
                    message="User must be authenticated to access menu"
                )
            
            # Get user role
            try:
                user_role = user.profile.role
            except Exception as e:
                logger.error(f"Error getting user role: {str(e)}")
                return ApiResponse.bad_request(
                    message="User profile not found or invalid",
                    error_details=str(e)
                )
            
            # Validate role is in allowed list
            if user_role not in cls.ALLOWED_ROLES:
                return ApiResponse.forbidden(
                    message=f"User role '{user_role}' is not authorized to access menu",
                    error_details=f"Allowed roles: {', '.join(cls.ALLOWED_ROLES)}"
                )
            
            return ApiResponse.success(
                data={'user_role': user_role, 'has_access': True},
                message="User has valid access"
            )
            
        except Exception as e:
            logger.error(f"Error validating user access: {str(e)}")
            return ApiResponse.server_error(
                message="Failed to validate user access",
                error_details=str(e)
            )
    
    @classmethod
    def validate_menu_structure(cls, group_id: Optional[int] = None) -> ApiResponse:
        """
        Validate menu structure for circular references and depth
        
        Args:
            group_id: Optional specific group to validate, or all if None
            
        Returns:
            ApiResponse object with validation results
        """
        try:
            # Get groups to validate
            if group_id:
                groups = NavigationGroup.objects.filter(id=group_id, is_active=True)
            else:
                groups = NavigationGroup.objects.filter(is_active=True)
            
            validation_results = {
                'groups_checked': 0,
                'items_checked': 0,
                'errors': [],
                'warnings': [],
                'circular_references': [],
                'depth_violations': [],
                'invalid_urls': []
            }
            
            for group in groups:
                validation_results['groups_checked'] += 1
                
                # Validate each item in group
                items = group.items.filter(is_active=True, parent__isnull=True)
                
                for item in items:
                    cls._validate_item_recursive(
                        item, 
                        validation_results, 
                        visited_ids=set(),
                        current_depth=0
                    )
            
            # Determine if validation passed
            has_errors = (
                len(validation_results['errors']) > 0 or
                len(validation_results['circular_references']) > 0 or
                len(validation_results['depth_violations']) > 0
            )
            
            if has_errors:
                return ApiResponse.bad_request(
                    message="Menu structure validation failed",
                    data=validation_results
                )
            else:
                return ApiResponse.success(
                    data=validation_results,
                    message="Menu structure validation passed"
                )
            
        except Exception as e:
            logger.error(f"Error validating menu structure: {str(e)}")
            return ApiResponse.server_error(
                message="Failed to validate menu structure",
                error_details=str(e)
            )
    
    @classmethod
    def _validate_item_recursive(
        cls, 
        item: NavigationItem, 
        results: Dict, 
        visited_ids: set,
        current_depth: int
    ):
        """
        Recursively validate menu item
        
        Args:
            item: NavigationItem to validate
            results: Dict to store validation results
            visited_ids: Set of already visited item IDs
            current_depth: Current recursion depth
        """
        results['items_checked'] += 1
        
        # Check for circular reference
        if item.id in visited_ids:
            results['circular_references'].append({
                'item_id': item.id,
                'item_title': item.title,
                'depth': current_depth
            })
            return
        
        # Check depth limit
        if current_depth >= cls.MAX_MENU_DEPTH:
            results['depth_violations'].append({
                'item_id': item.id,
                'item_title': item.title,
                'depth': current_depth,
                'max_allowed': cls.MAX_MENU_DEPTH
            })
            return
        
        # Validate URL
        if item.url_name and item.url_name != '#' and item.url_name != 'javascript:void(0)':
            try:
                reverse(item.url_name)
            except NoReverseMatch:
                results['invalid_urls'].append({
                    'item_id': item.id,
                    'item_title': item.title,
                    'url_name': item.url_name
                })
                results['warnings'].append(
                    f"Invalid URL name '{item.url_name}' for item '{item.title}'"
                )
        
        # Validate role assignment
        if not item.visible_to_roles or len(item.visible_to_roles) == 0:
            results['warnings'].append(
                f"Item '{item.title}' has no roles assigned, will be visible to all"
            )
        
        # Add to visited set
        visited_ids.add(item.id)
        
        # Validate children recursively
        if item.has_children():
            children = item.children.filter(is_active=True)
            for child in children:
                cls._validate_item_recursive(
                    child,
                    results,
                    visited_ids.copy(),  # New copy for each branch
                    current_depth + 1
                )
    
    @classmethod
    def validate_role_permissions(cls, role: str) -> ApiResponse:
        """
        Validate if a role exists and is allowed
        
        Args:
            role: Role string to validate
            
        Returns:
            ApiResponse object
        """
        try:
            if not role:
                return ApiResponse.bad_request(
                    message="Role cannot be empty"
                )
            
            if role not in cls.ALLOWED_ROLES:
                return ApiResponse.forbidden(
                    message=f"Role '{role}' is not allowed",
                    data={
                        'provided_role': role,
                        'allowed_roles': cls.ALLOWED_ROLES
                    }
                )
            
            return ApiResponse.success(
                data={'role': role, 'is_valid': True},
                message="Role is valid"
            )
            
        except Exception as e:
            logger.error(f"Error validating role: {str(e)}")
            return ApiResponse.server_error(
                message="Failed to validate role",
                error_details=str(e)
            )
    
    @classmethod
    def get_allowed_roles(cls) -> ApiResponse:
        """
        Get list of roles allowed to access navigation
        
        Returns:
            ApiResponse object with allowed roles
        """
        try:
            return ApiResponse.success(
                data={
                    'allowed_roles': cls.ALLOWED_ROLES,
                    'count': len(cls.ALLOWED_ROLES)
                },
                message="Allowed roles retrieved successfully"
            )
        except Exception as e:
            logger.error(f"Error getting allowed roles: {str(e)}")
            return ApiResponse.server_error(
                message="Failed to get allowed roles",
                error_details=str(e)
            )
