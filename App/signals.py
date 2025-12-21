"""
Django Signals for App
Auto-sync user groups when Profile.role changes
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from App.models import Profile
from App.utils.group_utils import sync_user_to_group


@receiver(post_save, sender=Profile)
def sync_user_group_on_role_change(sender, instance, created, **kwargs):
    """
    Automatically sync user to Django Group when Profile.role is created or updated
    
    Args:
        sender: Profile model
        instance: Profile instance
        created: bool, True if this is a new Profile
        **kwargs: Additional arguments
    """
    # Sync user to group based on their role
    sync_user_to_group(instance.user)
