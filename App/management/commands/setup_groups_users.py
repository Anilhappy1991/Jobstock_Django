"""
Management command to set up user groups and sample users for the Jobstock application.

This command creates:
- Hiring Manager group with permissions
- RPO Admin group with permissions
- System Admin group (superuser equivalent)
- Sample users for each group type

Usage:
    python manage.py setup_groups_users
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType
from App.models import Job, Profile


class Command(BaseCommand):
    help = 'Sets up user groups with permissions and creates sample users'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Setting up groups and users...'))
        
        # Create groups
        hiring_manager_group = self.create_hiring_manager_group()
        rpo_admin_group = self.create_rpo_admin_group()
        system_admin_group = self.create_system_admin_group()
        
        # Create sample users
        self.create_sample_users(hiring_manager_group, rpo_admin_group, system_admin_group)
        
        self.stdout.write(self.style.SUCCESS('Successfully set up groups and users!'))
        self.display_user_credentials()

    def create_hiring_manager_group(self):
        """
        Create Hiring Manager group with permissions:
        - Can create/view/edit job postings
        - Can view candidate profiles
        - Can view applications
        """
        self.stdout.write('Creating Hiring Manager group...')
        group, created = Group.objects.get_or_create(name='Hiring Manager')
        
        if created:
            self.stdout.write(self.style.SUCCESS('  ✓ Created Hiring Manager group'))
        else:
            self.stdout.write(self.style.WARNING('  - Hiring Manager group already exists'))
        
        # Clear existing permissions
        group.permissions.clear()
        
        # Job permissions
        job_ct = ContentType.objects.get_for_model(Job)
        job_permissions = Permission.objects.filter(
            content_type=job_ct,
            codename__in=['add_job', 'view_job', 'change_job']
        )
        group.permissions.add(*job_permissions)
        
        # Profile viewing permissions
        profile_ct = ContentType.objects.get_for_model(Profile)
        profile_view = Permission.objects.filter(
            content_type=profile_ct,
            codename='view_profile'
        )
        group.permissions.add(*profile_view)
        
        self.stdout.write(self.style.SUCCESS(f'  ✓ Assigned {group.permissions.count()} permissions'))
        return group

    def create_rpo_admin_group(self):
        """
        Create RPO Admin group with permissions:
        - Full CRUD on job postings
        - Can view/edit candidate profiles
        - Can view/manage applications
        - Can access analytics and benchmarking data
        - Can tune AI-generated profiles
        """
        self.stdout.write('Creating RPO Admin group...')
        group, created = Group.objects.get_or_create(name='RPO Admin')
        
        if created:
            self.stdout.write(self.style.SUCCESS('  ✓ Created RPO Admin group'))
        else:
            self.stdout.write(self.style.WARNING('  - RPO Admin group already exists'))
        
        # Clear existing permissions
        group.permissions.clear()
        
        # Full Job permissions
        job_ct = ContentType.objects.get_for_model(Job)
        job_permissions = Permission.objects.filter(content_type=job_ct)
        group.permissions.add(*job_permissions)
        
        # Full Profile permissions
        profile_ct = ContentType.objects.get_for_model(Profile)
        profile_permissions = Permission.objects.filter(content_type=profile_ct)
        group.permissions.add(*profile_permissions)
        
        self.stdout.write(self.style.SUCCESS(f'  ✓ Assigned {group.permissions.count()} permissions'))
        return group

    def create_system_admin_group(self):
        """
        Create System Admin group with permissions:
        - All permissions (equivalent to superuser)
        - Can manage users and groups
        - Can access all system features
        """
        self.stdout.write('Creating System Admin group...')
        group, created = Group.objects.get_or_create(name='System Admin')
        
        if created:
            self.stdout.write(self.style.SUCCESS('  ✓ Created System Admin group'))
        else:
            self.stdout.write(self.style.WARNING('  - System Admin group already exists'))
        
        # Clear existing permissions
        group.permissions.clear()
        
        # Assign ALL permissions
        all_permissions = Permission.objects.all()
        group.permissions.add(*all_permissions)
        
        self.stdout.write(self.style.SUCCESS(f'  ✓ Assigned {group.permissions.count()} permissions (all)'))
        return group

    def create_sample_users(self, hiring_manager_group, rpo_admin_group, system_admin_group):
        """Create sample users for each group type"""
        self.stdout.write('\nCreating sample users...')
        
        # Hiring Manager User
        hm_user, created = User.objects.get_or_create(
            username='hiring_manager',
            defaults={
                'email': 'hiring_manager@jobstock.com',
                'first_name': 'John',
                'last_name': 'Manager',
                'is_staff': True,
            }
        )
        if created:
            hm_user.set_password('manager123')
            hm_user.save()
            self.stdout.write(self.style.SUCCESS('  ✓ Created hiring_manager user'))
        else:
            self.stdout.write(self.style.WARNING('  - hiring_manager user already exists'))
        
        hm_user.groups.add(hiring_manager_group)
        
        # RPO Admin User
        rpo_user, created = User.objects.get_or_create(
            username='rpo_admin',
            defaults={
                'email': 'rpo_admin@jobstock.com',
                'first_name': 'Sarah',
                'last_name': 'RPO',
                'is_staff': True,
            }
        )
        if created:
            rpo_user.set_password('rpo123')
            rpo_user.save()
            self.stdout.write(self.style.SUCCESS('  ✓ Created rpo_admin user'))
        else:
            self.stdout.write(self.style.WARNING('  - rpo_admin user already exists'))
        
        rpo_user.groups.add(rpo_admin_group)
        
        # System Admin User
        sys_user, created = User.objects.get_or_create(
            username='system_admin',
            defaults={
                'email': 'system_admin@jobstock.com',
                'first_name': 'Admin',
                'last_name': 'System',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            sys_user.set_password('admin123')
            sys_user.save()
            self.stdout.write(self.style.SUCCESS('  ✓ Created system_admin user'))
        else:
            self.stdout.write(self.style.WARNING('  - system_admin user already exists'))
        
        sys_user.groups.add(system_admin_group)

    def display_user_credentials(self):
        """Display login credentials for created users"""
        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.SUCCESS('USER CREDENTIALS'))
        self.stdout.write('='*60)
        
        credentials = [
            {
                'role': 'Hiring Manager',
                'username': 'hiring_manager',
                'password': 'manager123',
                'email': 'hiring_manager@jobstock.com'
            },
            {
                'role': 'RPO Admin',
                'username': 'rpo_admin',
                'password': 'rpo123',
                'email': 'rpo_admin@jobstock.com'
            },
            {
                'role': 'System Admin',
                'username': 'system_admin',
                'password': 'admin123',
                'email': 'system_admin@jobstock.com'
            }
        ]
        
        for cred in credentials:
            self.stdout.write(f"\n{cred['role']}:")
            self.stdout.write(f"  Username: {cred['username']}")
            self.stdout.write(f"  Password: {cred['password']}")
            self.stdout.write(f"  Email:    {cred['email']}")
        
        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.WARNING('\nNOTE: Change these passwords in production!'))
        self.stdout.write('='*60 + '\n')
