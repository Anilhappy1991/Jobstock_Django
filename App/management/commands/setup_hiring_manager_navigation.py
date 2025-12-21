"""
Management command to setup/update complete navigation for Hiring Manager role
Usage: python manage.py setup_hiring_manager_navigation
"""
from django.core.management.base import BaseCommand
from App.models import NavigationGroup, NavigationItem


class Command(BaseCommand):
    help = 'Setup/Update complete navigation structure for Hiring Manager role'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Setting up Hiring Manager navigation...'))
        
        # Note: We don't delete existing navigation, we just create/update
        self.stdout.write('Creating or updating navigation items...')
        
        self.create_hiring_manager_navigation()
        
        self.stdout.write(self.style.SUCCESS('\n✓ Hiring Manager navigation setup complete!'))
        self.stdout.write(self.style.SUCCESS('All navigation groups and items have been created/updated.'))

    def create_hiring_manager_navigation(self):
        """Create complete navigation structure for Hiring Managers"""
        
        # ==================== MAIN MENU GROUP ====================
        main_group, created = NavigationGroup.objects.get_or_create(
            slug='hm-main-menu',
            defaults={
                'name': 'Main Menu',
                'icon': 'fas fa-bars',
                'visible_to_roles': ['hiring_manager'],
                'order': 1,
                'is_active': True,
            }
        )
        if created:
            self.stdout.write(f'  ✓ Created group: {main_group.name}')
        else:
            self.stdout.write(f'  • Updated group: {main_group.name}')
        
        # Dashboard
        nav_item, created = NavigationItem.objects.get_or_create(
            url_name='App:employer_dashboard',
            group=main_group,
            defaults={
                'title': 'Dashboard',
                'icon': 'fas fa-tachometer-alt',
                'visible_to_roles': ['hiring_manager'],
                'order': 1,
                'is_active': True,
            }
        )
        self.stdout.write(f'    {"✓" if created else "•"} {nav_item.title}')
        
        # Job Management (Parent)
        job_mgmt, created = NavigationItem.objects.get_or_create(
            url_name='#job-management',
            group=main_group,
            defaults={
                'title': 'Job Management',
                'icon': 'fas fa-briefcase',
                'visible_to_roles': ['hiring_manager'],
                'order': 2,
                'is_active': True,
            }
        )
        self.stdout.write(f'    {"✓" if created else "•"} {job_mgmt.title} (Parent)')
        
        # Job Management - Post New Job
        nav_item, created = NavigationItem.objects.get_or_create(
            url_name='App:employer_submit_job',
            group=main_group,
            parent=job_mgmt,
            defaults={
                'title': 'Post New Job',
                'icon': 'fas fa-plus-circle',
                'visible_to_roles': ['hiring_manager'],
                'order': 1,
                'is_active': True,
            }
        )
        self.stdout.write(f'      {"✓" if created else "•"} {nav_item.title}')
        
        # Job Management - Manage Jobs
        nav_item, created = NavigationItem.objects.get_or_create(
            url_name='App:employer_manage_jobs',
            group=main_group,
            parent=job_mgmt,
            defaults={
                'title': 'Manage Jobs',
                'icon': 'fas fa-tasks',
                'visible_to_roles': ['hiring_manager'],
                'order': 2,
                'is_active': True,
            }
        )
        self.stdout.write(f'      {"✓" if created else "•"} {nav_item.title}')
        
        # Job Management - Job Templates
        nav_item, created = NavigationItem.objects.get_or_create(
            url_name='App:employer_job_templates',
            group=main_group,
            parent=job_mgmt,
            defaults={
                'title': 'Job Templates',
                'icon': 'fas fa-copy',
                'visible_to_roles': ['hiring_manager'],
                'order': 3,
                'is_active': True,
            }
        )
        self.stdout.write(f'      {"✓" if created else "•"} {nav_item.title}')
        
        # Applications
        nav_item, created = NavigationItem.objects.get_or_create(
            url_name='App:employer_applications',
            group=main_group,
            defaults={
                'title': 'Applications',
                'icon': 'fas fa-inbox',
                'visible_to_roles': ['hiring_manager'],
                'badge_text': 'New',
                'badge_class': 'badge-danger',
                'order': 3,
                'is_active': True,
            }
        )
        self.stdout.write(f'    {"✓" if created else "•"} {nav_item.title}')
        
        # Candidates
        nav_item, created = NavigationItem.objects.get_or_create(
            url_name='App:employer_candidates',
            group=main_group,
            defaults={
                'title': 'Candidates',
                'icon': 'fas fa-user-tie',
                'visible_to_roles': ['hiring_manager'],
                'order': 4,
                'is_active': True,
            }
        )
        self.stdout.write(f'    {"✓" if created else "•"} {nav_item.title}')
        
        # Interviews
        nav_item, created = NavigationItem.objects.get_or_create(
            url_name='App:employer_interviews',
            group=main_group,
            defaults={
                'title': 'Interviews',
                'icon': 'fas fa-calendar-check',
                'visible_to_roles': ['hiring_manager'],
                'order': 5,
                'is_active': True,
            }
        )
        self.stdout.write(f'    {"✓" if created else "•"} {nav_item.title}')
        
        # ==================== REPORTS & ANALYTICS GROUP ====================
        reports_group, created = NavigationGroup.objects.get_or_create(
            slug='hm-reports-analytics',
            defaults={
                'name': 'Reports & Analytics',
                'icon': 'fas fa-chart-bar',
                'visible_to_roles': ['hiring_manager'],
                'order': 2,
                'is_active': True,
            }
        )
        if created:
            self.stdout.write(f'  ✓ Created group: {reports_group.name}')
        else:
            self.stdout.write(f'  • Updated group: {reports_group.name}')
        
        # Pipeline View
        nav_item, created = NavigationItem.objects.get_or_create(
            url_name='App:employer_pipeline',
            group=reports_group,
            defaults={
                'title': 'Hiring Pipeline',
                'icon': 'fas fa-stream',
                'visible_to_roles': ['hiring_manager'],
                'order': 1,
                'is_active': True,
            }
        )
        self.stdout.write(f'    {"✓" if created else "•"} {nav_item.title}')
        
        # Analytics Dashboard
        nav_item, created = NavigationItem.objects.get_or_create(
            url_name='App:employer_analytics',
            group=reports_group,
            defaults={
                'title': 'Analytics',
                'icon': 'fas fa-chart-line',
                'visible_to_roles': ['hiring_manager'],
                'order': 2,
                'is_active': True,
            }
        )
        self.stdout.write(f'    {"✓" if created else "•"} {nav_item.title}')
        
        # Reports
        nav_item, created = NavigationItem.objects.get_or_create(
            url_name='App:employer_reports',
            group=reports_group,
            defaults={
                'title': 'Reports',
                'icon': 'fas fa-file-invoice',
                'visible_to_roles': ['hiring_manager'],
                'order': 3,
                'is_active': True,
            }
        )
        self.stdout.write(f'    {"✓" if created else "•"} {nav_item.title}')
        
        # ==================== SETTINGS GROUP ====================
        settings_group, created = NavigationGroup.objects.get_or_create(
            slug='hm-settings',
            defaults={
                'name': 'Settings',
                'icon': 'fas fa-cog',
                'visible_to_roles': ['hiring_manager'],
                'order': 3,
                'is_active': True,
            }
        )
        if created:
            self.stdout.write(f'  ✓ Created group: {settings_group.name}')
        else:
            self.stdout.write(f'  • Updated group: {settings_group.name}')
        
        # Company Profile
        nav_item, created = NavigationItem.objects.get_or_create(
            url_name='App:employer_profile',
            group=settings_group,
            defaults={
                'title': 'Company Profile',
                'icon': 'fas fa-building',
                'visible_to_roles': ['hiring_manager'],
                'order': 1,
                'is_active': True,
            }
        )
        self.stdout.write(f'    {"✓" if created else "•"} {nav_item.title}')
        
        # Team Members
        nav_item, created = NavigationItem.objects.get_or_create(
            url_name='App:employer_team',
            group=settings_group,
            defaults={
                'title': 'Team Members',
                'icon': 'fas fa-users-cog',
                'visible_to_roles': ['hiring_manager'],
                'order': 2,
                'is_active': True,
            }
        )
        self.stdout.write(f'    {"✓" if created else "•"} {nav_item.title}')
        
        # Notifications
        nav_item, created = NavigationItem.objects.get_or_create(
            url_name='App:employer_notifications',
            group=settings_group,
            defaults={
                'title': 'Notifications',
                'icon': 'fas fa-bell',
                'visible_to_roles': ['hiring_manager'],
                'order': 3,
                'is_active': True,
            }
        )
        self.stdout.write(f'    {"✓" if created else "•"} {nav_item.title}')
        
        # Account Settings
        nav_item, created = NavigationItem.objects.get_or_create(
            url_name='App:employer_settings',
            group=settings_group,
            defaults={
                'title': 'Account Settings',
                'icon': 'fas fa-user-cog',
                'visible_to_roles': ['hiring_manager'],
                'order': 4,
                'is_active': True,
            }
        )
        self.stdout.write(f'    {"✓" if created else "•"} {nav_item.title}')
        
        # ==================== ADDITIONAL FEATURES GROUP ====================
        features_group, created = NavigationGroup.objects.get_or_create(
            slug='hm-features',
            defaults={
                'name': 'Features',
                'icon': 'fas fa-star',
                'visible_to_roles': ['hiring_manager'],
                'order': 4,
                'is_active': True,
            }
        )
        if created:
            self.stdout.write(f'  ✓ Created group: {features_group.name}')
        else:
            self.stdout.write(f'  • Updated group: {features_group.name}')
        
        # Messages
        nav_item, created = NavigationItem.objects.get_or_create(
            url_name='App:employer_messages',
            group=features_group,
            defaults={
                'title': 'Messages',
                'icon': 'fas fa-envelope',
                'visible_to_roles': ['hiring_manager'],
                'badge_text': '5',
                'badge_class': 'badge-info',
                'order': 1,
                'is_active': True,
            }
        )
        self.stdout.write(f'    {"✓" if created else "•"} {nav_item.title}')
        
        # Saved Candidates
        nav_item, created = NavigationItem.objects.get_or_create(
            url_name='App:employer_saved_candidates',
            group=features_group,
            defaults={
                'title': 'Saved Candidates',
                'icon': 'fas fa-bookmark',
                'visible_to_roles': ['hiring_manager'],
                'order': 2,
                'is_active': True,
            }
        )
        self.stdout.write(f'    {"✓" if created else "•"} {nav_item.title}')
        
        # AI Screening
        nav_item, created = NavigationItem.objects.get_or_create(
            url_name='App:employer_ai_screening',
            group=features_group,
            defaults={
                'title': 'AI Screening',
                'icon': 'fas fa-robot',
                'visible_to_roles': ['hiring_manager'],
                'badge_text': 'Beta',
                'badge_class': 'badge-warning',
                'order': 3,
                'is_active': True,
            }
        )
        self.stdout.write(f'    {"✓" if created else "•"} {nav_item.title}')
        
        # Help & Support
        nav_item, created = NavigationItem.objects.get_or_create(
            url_name='App:employer_help',
            group=features_group,
            defaults={
                'title': 'Help & Support',
                'icon': 'fas fa-question-circle',
                'visible_to_roles': ['hiring_manager'],
                'order': 4,
                'is_active': True,
            }
        )
        self.stdout.write(f'    {"✓" if created else "•"} {nav_item.title}')
        
        self.stdout.write(self.style.SUCCESS('\nNavigation Summary:'))
        total_groups = sum(1 for group in NavigationGroup.objects.all() if 'hiring_manager' in group.visible_to_roles)
        total_items = sum(1 for item in NavigationItem.objects.all() if 'hiring_manager' in item.visible_to_roles)
        self.stdout.write(f'  • Total Groups: {total_groups}')
        self.stdout.write(f'  • Total Items: {total_items}')
