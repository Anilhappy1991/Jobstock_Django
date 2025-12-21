"""
Group and Role Utilities
Helper functions to work with Django Groups and custom roles
"""
from django.contrib.auth.models import User, Group
from App.models import GroupProfile


def sync_user_to_group(user):
    """
    Sync user's Profile.role to their Django Group
    
    Args:
        user: User instance
        
    Returns:
        Group instance or None
    """
    try:
        role = user.profile.role
        
        # Find group with matching role_identifier
        group_profile = GroupProfile.objects.get(role_identifier=role)
        group = group_profile.group
        
        # Clear existing groups and add the correct one
        user.groups.clear()
        user.groups.add(group)
        
        return group
    except (AttributeError, GroupProfile.DoesNotExist):
        return None


def get_role_from_group(group):
    """
    Get role_identifier from a Django Group
    
    Args:
        group: Group instance
        
    Returns:
        str: role_identifier (e.g., 'hiring_manager') or None
    """
    try:
        return group.profile.role_identifier
    except GroupProfile.DoesNotExist:
        return None


def get_group_from_role(role_identifier):
    """
    Get Django Group from role identifier
    
    Args:
        role_identifier: str (e.g., 'hiring_manager')
        
    Returns:
        Group instance or None
    """
    try:
        group_profile = GroupProfile.objects.get(role_identifier=role_identifier)
        return group_profile.group
    except GroupProfile.DoesNotExist:
        return None


def sync_all_users():
    """
    Sync all users' Profile.role to their Django Groups
    Useful for one-time migration or maintenance
    
    Returns:
        dict: Statistics of sync operation
    """
    from App.models import Profile
    
    stats = {
        'synced': 0,
        'skipped': 0,
        'errors': []
    }
    
    for profile in Profile.objects.select_related('user').all():
        try:
            group = sync_user_to_group(profile.user)
            if group:
                stats['synced'] += 1
            else:
                stats['skipped'] += 1
        except Exception as e:
            stats['errors'].append(f"User {profile.user.username}: {str(e)}")
    
    return stats


def get_users_by_role(role_identifier):
    """
    Get all users with a specific role
    
    Args:
        role_identifier: str (e.g., 'hiring_manager')
        
    Returns:
        QuerySet of Users
    """
    group = get_group_from_role(role_identifier)
    if group:
        return User.objects.filter(groups=group)
    return User.objects.none()
