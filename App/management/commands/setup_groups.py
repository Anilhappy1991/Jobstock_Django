"""
Management command to create Django Groups and link them to role identifiers
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from App.models import GroupProfile


class Command(BaseCommand):
    help = 'Create Django Groups and associate them with role identifiers'

    def handle(self, *args, **options):
        self.stdout.write('Creating Django Groups and linking to roles...\n')
        
        # Define groups with their role identifiers
        groups_data = [
            {
                'name': 'Candidates',
                'role_identifier': 'candidate',
                'description': 'Job seekers looking for employment opportunities'
            },
            {
                'name': 'Hiring Managers',
                'role_identifier': 'hiring_manager',
                'description': 'Employers who post jobs and review applications'
            },
            {
                'name': 'RPO Admins',
                'role_identifier': 'rpo_admin',
                'description': 'RPO administrators managing multiple clients'
            },
        ]
        
        created_count = 0
        updated_count = 0
        
        for group_data in groups_data:
            # Create or get Django Group
            group, group_created = Group.objects.get_or_create(
                name=group_data['name']
            )
            
            if group_created:
                self.stdout.write(f"  ✓ Created group: {group.name}")
            else:
                self.stdout.write(f"  → Group already exists: {group.name}")
            
            # Create or update GroupProfile
            profile, profile_created = GroupProfile.objects.update_or_create(
                group=group,
                defaults={
                    'role_identifier': group_data['role_identifier'],
                    'description': group_data['description']
                }
            )
            
            if profile_created:
                self.stdout.write(f"     ✓ Linked to role: {profile.role_identifier}")
                created_count += 1
            else:
                self.stdout.write(f"     → Updated role link: {profile.role_identifier}")
                updated_count += 1
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\n✓ Complete! Created {created_count} new links, updated {updated_count} existing links'
            )
        )
        
        # Display summary
        self.stdout.write('\n' + '='*60)
        self.stdout.write('Group to Role Mapping:')
        self.stdout.write('='*60)
        
        for profile in GroupProfile.objects.all():
            self.stdout.write(
                f"  Group: {profile.group.name:20} → Role: {profile.role_identifier}"
            )
        
        self.stdout.write('='*60 + '\n')
