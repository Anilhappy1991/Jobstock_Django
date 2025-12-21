"""
Navigation Service
Handles all navigation and dashboard logic for all user groups
"""
from typing import Dict, Any, Optional, List
from django.contrib.auth.models import User
from django.urls import reverse, NoReverseMatch
from App.models import (
    NavigationGroup, NavigationItem, DashboardWidget, 
    QuickAction, UserDashboardPreference
)
from App.services.base_service import BaseService
from App.utils.response import ApiResponse
import logging

logger = logging.getLogger(__name__)


class NavigationService(BaseService):
    """Service for navigation operations"""
    
    model = NavigationItem
    
    @classmethod
    def get_navigation_for_user(cls, user: User) -> Dict[str, Any]:
        """
        Get navigation menu items for a specific user based on their role
        
        Args:
            user: User object
            
        Returns:
            ApiResponse dict with navigation structure
        """
        try:
            # Get user role
            try:
                user_role = user.profile.role
            except:
                user_role = 'candidate'  # Default role
            
            # Get active navigation groups visible to this role
            nav_groups = NavigationGroup.objects.filter(
                is_active=True
            ).prefetch_related('items')
            
            navigation = []
            
            for group in nav_groups:
                # Check if user role can see this group
                if not cls._is_visible_to_role(group.visible_to_roles, user_role):
                    continue
                
                # Get items for this group
                items = cls._get_items_for_role(group, user_role, user)
                
                if items:  # Only include groups that have visible items
                    navigation.append({
                        'id': group.id,
                        'name': group.name,
                        'slug': group.slug,
                        'icon': group.icon,
                        'items': items
                    })
            
            return ApiResponse.success(
                data={'navigation': navigation},
                message="Navigation retrieved successfully"
            )
            
        except Exception as e:
            logger.error(f"Error getting navigation: {str(e)}")
            return ApiResponse.server_error(
                message="Failed to retrieve navigation",
                error_details=str(e)
            )
    
    @classmethod
    def _get_items_for_role(cls, group, user_role: str, user: User) -> List[Dict]:
        """Get navigation items for a specific role - ONLY ACTIVE ITEMS"""
        items = []
        
        # Get top-level items (no parent) - ONLY ACTIVE
        top_items = group.items.filter(
            is_active=True,
            parent__isnull=True
        ).order_by('order')
        
        for item in top_items:
            # Check role visibility
            if not cls._is_visible_to_role(item.visible_to_roles, user_role):
                continue
            
            # Check permissions
            if item.requires_permission and not user.has_perm(item.requires_permission):
                continue
            
            # Get URL
            try:
                url = reverse(item.url_name)
            except NoReverseMatch:
                url = '#'
                logger.warning(f"URL name '{item.url_name}' not found for nav item '{item.title}'")
            
            # Build item data
            item_data = {
                'id': item.id,
                'title': item.title,
                'url': url,
                'url_name': item.url_name,
                'icon': item.icon,
                'badge_text': item.badge_text,
                'badge_class': item.badge_class,
                'has_children': item.has_children(),
            }
            
            # Get children if any
            if item.has_children():
                children = []
                for child in item.children.filter(is_active=True).order_by('order'):
                    if cls._is_visible_to_role(child.visible_to_roles, user_role):
                        try:
                            child_url = reverse(child.url_name)
                        except NoReverseMatch:
                            child_url = '#'
                        
                        children.append({
                            'id': child.id,
                            'title': child.title,
                            'url': child_url,
                            'url_name': child.url_name,
                            'icon': child.icon,
                            'badge_text': child.badge_text,
                            'badge_class': child.badge_class,
                        })
                
                item_data['children'] = children
            
            items.append(item_data)
        
        return items
    
    @classmethod
    def _is_visible_to_role(cls, visible_to_roles: List[str], user_role: str) -> bool:
        """Check if item is visible to user role"""
        if not visible_to_roles or 'all' in visible_to_roles:
            return True
        return user_role in visible_to_roles
    
    @classmethod
    def get_dashboard_widgets(cls, user: User) -> Dict[str, Any]:
        """
        Get dashboard widgets for user based on role
        
        Args:
            user: User object
            
        Returns:
            ApiResponse dict with widgets
        """
        try:
            # Get user role
            try:
                user_role = user.profile.role
            except:
                user_role = 'candidate'
            
            # Get user preferences
            preferences, _ = UserDashboardPreference.objects.get_or_create(user=user)
            hidden_widget_ids = preferences.hidden_widgets
            custom_order = preferences.widget_order
            
            # Get active widgets for this role
            widgets = DashboardWidget.objects.filter(is_active=True)
            
            widget_list = []
            
            for widget in widgets:
                # Check role visibility
                if not cls._is_visible_to_role(widget.visible_to_roles, user_role):
                    continue
                
                # Check if user has hidden this widget
                if widget.id in hidden_widget_ids:
                    continue
                
                # Get custom order or default
                order = custom_order.get(str(widget.id), widget.order)
                
                widget_data = {
                    'id': widget.id,
                    'title': widget.title,
                    'type': widget.widget_type,
                    'icon': widget.icon,
                    'description': widget.description,
                    'data_source': widget.data_source,
                    'grid_column': widget.grid_column,
                    'order': order,
                    'css_class': widget.css_class,
                    'color_class': widget.color_class,
                }
                
                widget_list.append(widget_data)
            
            # Sort by order
            widget_list.sort(key=lambda x: x['order'])
            
            return ApiResponse.success(
                data={'widgets': widget_list},
                message="Widgets retrieved successfully"
            )
            
        except Exception as e:
            logger.error(f"Error getting dashboard widgets: {str(e)}")
            return ApiResponse.server_error(
                message="Failed to retrieve widgets",
                error_details=str(e)
            )
    
    @classmethod
    def get_quick_actions(cls, user: User) -> Dict[str, Any]:
        """
        Get quick action buttons for user
        
        Args:
            user: User object
            
        Returns:
            ApiResponse dict with quick actions
        """
        try:
            # Get user role
            try:
                user_role = user.profile.role
            except:
                user_role = 'candidate'
            
            # Get active quick actions
            actions = QuickAction.objects.filter(is_active=True).order_by('order')
            
            action_list = []
            
            for action in actions:
                # Check role visibility
                if not cls._is_visible_to_role(action.visible_to_roles, user_role):
                    continue
                
                try:
                    url = reverse(action.url_name)
                except NoReverseMatch:
                    url = '#'
                
                action_list.append({
                    'id': action.id,
                    'title': action.title,
                    'description': action.description,
                    'icon': action.icon,
                    'url': url,
                    'button_class': action.button_class,
                })
            
            return ApiResponse.success(
                data={'quick_actions': action_list},
                message="Quick actions retrieved successfully"
            )
            
        except Exception as e:
            logger.error(f"Error getting quick actions: {str(e)}")
            return ApiResponse.server_error(
                message="Failed to retrieve quick actions",
                error_details=str(e)
            )
    
    @classmethod
    def update_user_preferences(cls, user: User, preferences_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update user dashboard preferences
        
        Args:
            user: User object
            preferences_data: Dictionary of preferences
            
        Returns:
            ApiResponse dict
        """
        try:
            preferences, created = UserDashboardPreference.objects.get_or_create(user=user)
            
            # Update fields
            if 'hidden_widgets' in preferences_data:
                preferences.hidden_widgets = preferences_data['hidden_widgets']
            
            if 'widget_order' in preferences_data:
                preferences.widget_order = preferences_data['widget_order']
            
            if 'theme' in preferences_data:
                preferences.theme = preferences_data['theme']
            
            if 'sidebar_collapsed' in preferences_data:
                preferences.sidebar_collapsed = preferences_data['sidebar_collapsed']
            
            preferences.save()
            
            return ApiResponse.success(
                data={'preferences_id': preferences.id},
                message="Preferences updated successfully"
            )
            
        except Exception as e:
            logger.error(f"Error updating preferences: {str(e)}")
            return ApiResponse.server_error(
                message="Failed to update preferences",
                error_details=str(e)
            )
    
    @classmethod
    def get_complete_dashboard_data(cls, user: User) -> Dict[str, Any]:
        """
        Get all dashboard data in one call (navigation, widgets, quick actions)
        
        Args:
            user: User object
            
        Returns:
            ApiResponse dict with complete dashboard data
        """
        try:
            # Get all dashboard components
            nav_response = cls.get_navigation_for_user(user)
            widgets_response = cls.get_dashboard_widgets(user)
            actions_response = cls.get_quick_actions(user)
            
            # Combine data
            dashboard_data = {
                'navigation': nav_response.get('data', {}).get('navigation', []),
                'widgets': widgets_response.get('data', {}).get('widgets', []),
                'quick_actions': actions_response.get('data', {}).get('quick_actions', []),
                'user': {
                    'username': user.username,
                    'role': user.profile.role if hasattr(user, 'profile') else 'candidate',
                    'full_name': user.profile.full_name if hasattr(user, 'profile') else user.get_full_name(),
                }
            }
            
            return ApiResponse.success(
                data=dashboard_data,
                message="Dashboard data retrieved successfully"
            )
            
        except Exception as e:
            logger.error(f"Error getting complete dashboard data: {str(e)}")
            return ApiResponse.server_error(
                message="Failed to retrieve dashboard data",
                error_details=str(e)
            )
    
    @classmethod
    def get_navigation_stats(cls, user: User) -> Dict[str, Any]:
        """
        Get navigation statistics (badge counts, notifications, etc.)
        
        Args:
            user: User object
            
        Returns:
            ApiResponse dict with stats
        """
        try:
            from App.models import JobApplication, Job, Message
            
            # Get user role
            try:
                user_role = user.profile.role
            except:
                user_role = 'candidate'
            
            stats = {}
            
            # Role-specific stats
            if user_role == 'hiring_manager':
                stats = {
                    'new_applications': JobApplication.objects.filter(
                        job__posted_by=user,
                        status='pending'
                    ).count(),
                    'active_jobs': Job.objects.filter(
                        posted_by=user,
                        is_active=True
                    ).count(),
                    'unread_messages': 0,  # Implement message counting
                    'total_candidates': JobApplication.objects.filter(
                        job__posted_by=user
                    ).values('candidate').distinct().count(),
                }
            elif user_role == 'candidate':
                stats = {
                    'applications_count': JobApplication.objects.filter(
                        candidate=user
                    ).count(),
                    'saved_jobs': 0,  # Implement saved jobs counting
                    'profile_views': 0,  # Implement profile views
                    'unread_messages': 0,
                }
            elif user_role == 'rpo_admin':
                stats = {
                    'total_jobs': Job.objects.count(),
                    'total_applications': JobApplication.objects.count(),
                    'pending_approvals': Job.objects.filter(status='pending').count(),
                    'active_clients': 0,  # Implement client counting
                }
            
            return ApiResponse.success(
                data={'stats': stats},
                message="Navigation stats retrieved successfully"
            )
            
        except Exception as e:
            logger.error(f"Error getting navigation stats: {str(e)}")
            return ApiResponse.server_error(
                message="Failed to retrieve navigation stats",
                error_details=str(e)
            )
