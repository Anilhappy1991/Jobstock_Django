"""
Management command to populate initial navigation data for all user roles
"""
from django.core.management.base import BaseCommand
from App.models import NavigationGroup, NavigationItem, DashboardWidget, QuickAction


class Command(BaseCommand):
    help = 'Populate initial navigation, widgets, and quick actions for all user roles'

    def handle(self, *args, **options):
        self.stdout.write('Populating navigation data...\n')
        
        # Create navigation data
        self.create_navigation_groups()
        self.create_dashboard_widgets()
        self.create_quick_actions()
        
        self.stdout.write(self.style.SUCCESS('\n✓ Navigation data populated successfully!'))

    def create_navigation_groups(self):
        """Create navigation groups and items for all roles"""
        self.stdout.write('Creating navigation groups and items...')
        
        # ==================== HIRING MANAGER NAVIGATION ====================
        hm_main, _ = NavigationGroup.objects.get_or_create(
            slug='hm-main',
            defaults={
                'name': 'Main Menu',
                'icon': 'fas fa-bars',
                'visible_to_roles': ['hiring_manager'],
                'order': 1,
            }
        )
        
        # Dashboard
        NavigationItem.objects.get_or_create(
            url_name='employer_dashboard',
            defaults={
                'group': hm_main,
                'title': 'Dashboard',
                'icon': 'fas fa-home',
                'visible_to_roles': ['hiring_manager'],
                'order': 1,
            }
        )
        
        # Job Management
        job_mgmt, _ = NavigationItem.objects.get_or_create(
            url_name='#',
            title='Job Management',
            defaults={
                'group': hm_main,
                'icon': 'fas fa-briefcase',
                'visible_to_roles': ['hiring_manager'],
                'order': 2,
            }
        )
        
        NavigationItem.objects.get_or_create(
            url_name='employer_submit_job',
            defaults={
                'group': hm_main,
                'parent': job_mgmt,
                'title': 'Post a Job',
                'icon': 'fas fa-plus-circle',
                'visible_to_roles': ['hiring_manager'],
                'order': 1,
            }
        )
        
        NavigationItem.objects.get_or_create(
            url_name='employer_manage_jobs',
            defaults={
                'group': hm_main,
                'parent': job_mgmt,
                'title': 'Manage Jobs',
                'icon': 'fas fa-tasks',
                'visible_to_roles': ['hiring_manager'],
                'order': 2,
            }
        )
        
        # Applications
        NavigationItem.objects.get_or_create(
            url_name='employer_applications',
            defaults={
                'group': hm_main,
                'title': 'Applications',
                'icon': 'fas fa-users',
                'visible_to_roles': ['hiring_manager'],
                'badge_text': 'New',
                'badge_class': 'badge-danger',
                'order': 3,
            }
        )
        
        # Candidates
        NavigationItem.objects.get_or_create(
            url_name='employer_candidates',
            defaults={
                'group': hm_main,
                'title': 'Candidates',
                'icon': 'fas fa-user-tie',
                'visible_to_roles': ['hiring_manager'],
                'order': 4,
            }
        )
        
        # ==================== CANDIDATE NAVIGATION ====================
        cand_main, _ = NavigationGroup.objects.get_or_create(
            slug='candidate-main',
            defaults={
                'name': 'Main Menu',
                'icon': 'fas fa-bars',
                'visible_to_roles': ['candidate'],
                'order': 1,
            }
        )
        
        # Dashboard
        NavigationItem.objects.get_or_create(
            url_name='candidate_dashboard',
            defaults={
                'group': cand_main,
                'title': 'Dashboard',
                'icon': 'fas fa-home',
                'visible_to_roles': ['candidate'],
                'order': 1,
            }
        )
        
        # Job Search
        NavigationItem.objects.get_or_create(
            url_name='job_list',
            defaults={
                'group': cand_main,
                'title': 'Find Jobs',
                'icon': 'fas fa-search',
                'visible_to_roles': ['candidate'],
                'order': 2,
            }
        )
        
        # My Applications
        NavigationItem.objects.get_or_create(
            url_name='candidate_applications',
            defaults={
                'group': cand_main,
                'title': 'My Applications',
                'icon': 'fas fa-file-alt',
                'visible_to_roles': ['candidate'],
                'order': 3,
            }
        )
        
        # Saved Jobs
        NavigationItem.objects.get_or_create(
            url_name='candidate_saved_jobs',
            defaults={
                'group': cand_main,
                'title': 'Saved Jobs',
                'icon': 'fas fa-bookmark',
                'visible_to_roles': ['candidate'],
                'order': 4,
            }
        )
        
        # Profile
        NavigationItem.objects.get_or_create(
            url_name='candidate_profile',
            defaults={
                'group': cand_main,
                'title': 'My Profile',
                'icon': 'fas fa-user',
                'visible_to_roles': ['candidate'],
                'order': 5,
            }
        )
        
        # ==================== RPO ADMIN NAVIGATION ====================
        rpo_main, _ = NavigationGroup.objects.get_or_create(
            slug='rpo-main',
            defaults={
                'name': 'Main Menu',
                'icon': 'fas fa-bars',
                'visible_to_roles': ['rpo_admin'],
                'order': 1,
            }
        )
        
        # Dashboard
        NavigationItem.objects.get_or_create(
            url_name='rpo_dashboard',
            defaults={
                'group': rpo_main,
                'title': 'Dashboard',
                'icon': 'fas fa-chart-line',
                'visible_to_roles': ['rpo_admin'],
                'order': 1,
            }
        )
        
        # Clients
        NavigationItem.objects.get_or_create(
            url_name='rpo_clients',
            defaults={
                'group': rpo_main,
                'title': 'Clients',
                'icon': 'fas fa-building',
                'visible_to_roles': ['rpo_admin'],
                'order': 2,
            }
        )
        
        # All Jobs
        NavigationItem.objects.get_or_create(
            url_name='rpo_jobs',
            defaults={
                'group': rpo_main,
                'title': 'All Jobs',
                'icon': 'fas fa-briefcase',
                'visible_to_roles': ['rpo_admin'],
                'order': 3,
            }
        )
        
        # Analytics
        NavigationItem.objects.get_or_create(
            url_name='rpo_analytics',
            defaults={
                'group': rpo_main,
                'title': 'Analytics',
                'icon': 'fas fa-chart-bar',
                'visible_to_roles': ['rpo_admin'],
                'order': 4,
            }
        )
        
        # Reports
        NavigationItem.objects.get_or_create(
            url_name='rpo_reports',
            defaults={
                'group': rpo_main,
                'title': 'Reports',
                'icon': 'fas fa-file-invoice',
                'visible_to_roles': ['rpo_admin'],
                'order': 5,
            }
        )
        
        self.stdout.write(self.style.SUCCESS('  ✓ Navigation groups and items created'))

    def create_dashboard_widgets(self):
        """Create dashboard widgets for all roles"""
        self.stdout.write('Creating dashboard widgets...')
        
        # ==================== HIRING MANAGER WIDGETS ====================
        DashboardWidget.objects.get_or_create(
            title='Active Jobs',
            visible_to_roles=['hiring_manager'],
            defaults={
                'widget_type': 'stat_card',
                'icon': 'fas fa-briefcase',
                'description': 'Currently active job postings',
                'data_source': '/api/jobs/count/active/',
                'grid_column': '1',
                'order': 1,
                'color_class': 'bg-primary',
            }
        )
        
        DashboardWidget.objects.get_or_create(
            title='New Applications',
            visible_to_roles=['hiring_manager'],
            defaults={
                'widget_type': 'stat_card',
                'icon': 'fas fa-inbox',
                'description': 'Applications received today',
                'data_source': '/api/applications/count/new/',
                'grid_column': '1',
                'order': 2,
                'color_class': 'bg-success',
            }
        )
        
        DashboardWidget.objects.get_or_create(
            title='Recent Applications',
            visible_to_roles=['hiring_manager'],
            defaults={
                'widget_type': 'table',
                'icon': 'fas fa-list',
                'description': 'Latest job applications',
                'data_source': '/api/applications/recent/',
                'grid_column': 'span 2',
                'order': 3,
            }
        )
        
        # ==================== CANDIDATE WIDGETS ====================
        DashboardWidget.objects.get_or_create(
            title='Jobs Applied',
            visible_to_roles=['candidate'],
            defaults={
                'widget_type': 'stat_card',
                'icon': 'fas fa-paper-plane',
                'description': 'Total applications submitted',
                'data_source': '/api/candidate/applications/count/',
                'grid_column': '1',
                'order': 1,
                'color_class': 'bg-info',
            }
        )
        
        DashboardWidget.objects.get_or_create(
            title='Profile Views',
            visible_to_roles=['candidate'],
            defaults={
                'widget_type': 'stat_card',
                'icon': 'fas fa-eye',
                'description': 'Employers viewed your profile',
                'data_source': '/api/candidate/profile/views/',
                'grid_column': '1',
                'order': 2,
                'color_class': 'bg-warning',
            }
        )
        
        DashboardWidget.objects.get_or_create(
            title='Recommended Jobs',
            visible_to_roles=['candidate'],
            defaults={
                'widget_type': 'list',
                'icon': 'fas fa-star',
                'description': 'Jobs matching your profile',
                'data_source': '/api/jobs/recommended/',
                'grid_column': 'span 2',
                'order': 3,
            }
        )
        
        DashboardWidget.objects.get_or_create(
            title='Application Status',
            visible_to_roles=['candidate'],
            defaults={
                'widget_type': 'chart',
                'icon': 'fas fa-chart-pie',
                'description': 'Your application statuses',
                'data_source': '/api/candidate/applications/stats/',
                'grid_column': '1',
                'order': 4,
            }
        )
        
        # ==================== RPO ADMIN WIDGETS ====================
        DashboardWidget.objects.get_or_create(
            title='Total Clients',
            visible_to_roles=['rpo_admin'],
            defaults={
                'widget_type': 'stat_card',
                'icon': 'fas fa-building',
                'description': 'Active client companies',
                'data_source': '/api/rpo/clients/count/',
                'grid_column': '1',
                'order': 1,
                'color_class': 'bg-primary',
            }
        )
        
        DashboardWidget.objects.get_or_create(
            title='All Jobs',
            visible_to_roles=['rpo_admin'],
            defaults={
                'widget_type': 'stat_card',
                'icon': 'fas fa-briefcase',
                'description': 'Jobs across all clients',
                'data_source': '/api/rpo/jobs/count/',
                'grid_column': '1',
                'order': 2,
                'color_class': 'bg-success',
            }
        )
        
        DashboardWidget.objects.get_or_create(
            title='Placement Rate',
            visible_to_roles=['rpo_admin'],
            defaults={
                'widget_type': 'stat_card',
                'icon': 'fas fa-percentage',
                'description': 'Successful placements this month',
                'data_source': '/api/rpo/placement-rate/',
                'grid_column': '1',
                'order': 3,
                'color_class': 'bg-info',
            }
        )
        
        DashboardWidget.objects.get_or_create(
            title='Client Performance',
            visible_to_roles=['rpo_admin'],
            defaults={
                'widget_type': 'chart',
                'icon': 'fas fa-chart-line',
                'description': 'Performance metrics by client',
                'data_source': '/api/rpo/analytics/clients/',
                'grid_column': 'span 2',
                'order': 4,
            }
        )
        
        self.stdout.write(self.style.SUCCESS('  ✓ Dashboard widgets created'))

    def create_quick_actions(self):
        """Create quick action buttons for all roles"""
        self.stdout.write('Creating quick actions...')
        
        # ==================== HIRING MANAGER QUICK ACTIONS ====================
        QuickAction.objects.get_or_create(
            title='Post New Job',
            visible_to_roles=['hiring_manager'],
            defaults={
                'description': 'Create a new job posting',
                'icon': 'fas fa-plus-circle',
                'url_name': 'employer_submit_job',
                'button_class': 'btn-primary',
                'order': 1,
            }
        )
        
        QuickAction.objects.get_or_create(
            title='Review Applications',
            visible_to_roles=['hiring_manager'],
            defaults={
                'description': 'View pending applications',
                'icon': 'fas fa-clipboard-check',
                'url_name': 'employer_applications',
                'button_class': 'btn-success',
                'order': 2,
            }
        )
        
        QuickAction.objects.get_or_create(
            title='Search Candidates',
            visible_to_roles=['hiring_manager'],
            defaults={
                'description': 'Find qualified candidates',
                'icon': 'fas fa-search',
                'url_name': 'employer_candidates',
                'button_class': 'btn-info',
                'order': 3,
            }
        )
        
        # ==================== CANDIDATE QUICK ACTIONS ====================
        QuickAction.objects.get_or_create(
            title='Find Jobs',
            visible_to_roles=['candidate'],
            defaults={
                'description': 'Search for available positions',
                'icon': 'fas fa-search',
                'url_name': 'job_list',
                'button_class': 'btn-primary',
                'order': 1,
            }
        )
        
        QuickAction.objects.get_or_create(
            title='Update Resume',
            visible_to_roles=['candidate'],
            defaults={
                'description': 'Upload or edit your resume',
                'icon': 'fas fa-file-upload',
                'url_name': 'candidate_profile',
                'button_class': 'btn-success',
                'order': 2,
            }
        )
        
        QuickAction.objects.get_or_create(
            title='Track Applications',
            visible_to_roles=['candidate'],
            defaults={
                'description': 'View application status',
                'icon': 'fas fa-clipboard-list',
                'url_name': 'candidate_applications',
                'button_class': 'btn-info',
                'order': 3,
            }
        )
        
        # ==================== RPO ADMIN QUICK ACTIONS ====================
        QuickAction.objects.get_or_create(
            title='Add Client',
            visible_to_roles=['rpo_admin'],
            defaults={
                'description': 'Register new client company',
                'icon': 'fas fa-building',
                'url_name': 'rpo_clients',
                'button_class': 'btn-primary',
                'order': 1,
            }
        )
        
        QuickAction.objects.get_or_create(
            title='View Analytics',
            visible_to_roles=['rpo_admin'],
            defaults={
                'description': 'Performance analytics',
                'icon': 'fas fa-chart-bar',
                'url_name': 'rpo_analytics',
                'button_class': 'btn-success',
                'order': 2,
            }
        )
        
        QuickAction.objects.get_or_create(
            title='Generate Report',
            visible_to_roles=['rpo_admin'],
            defaults={
                'description': 'Create client reports',
                'icon': 'fas fa-file-pdf',
                'url_name': 'rpo_reports',
                'button_class': 'btn-warning',
                'order': 3,
            }
        )
        
        self.stdout.write(self.style.SUCCESS('  ✓ Quick actions created'))
