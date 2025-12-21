"""
Management command to sync all users to their Django Groups based on Profile.role
Usage: python manage.py sync_user_groups
"""
from django.core.management.base import BaseCommand
from App.utils.group_utils import sync_all_users


class Command(BaseCommand):
    help = 'Sync all users to Django Groups based on their Profile.role'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Syncing all users to their Django Groups...\n'))
        
        # Run the sync
        stats = sync_all_users()
        
        # Display results
        self.stdout.write(
            self.style.SUCCESS(f'✓ Synced: {stats["synced"]} users')
        )
        self.stdout.write(
            self.style.WARNING(f'⚠ Skipped: {stats["skipped"]} users (no profile or invalid role)')
        )
        
        if stats['errors']:
            self.stdout.write(self.style.ERROR(f'\n✗ Errors ({len(stats["errors"])}):'))
            for error in stats['errors']:
                self.stdout.write(self.style.ERROR(f'  - {error}'))
        
        self.stdout.write(
            self.style.SUCCESS(f'\n✓ Complete! Synced {stats["synced"]} users to groups')
        )
