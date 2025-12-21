"""
Setup Hierarchical Multilevel Navigation
Creates navigation for hiring_manager and rpo_admin only
Deactivates all other user navigation items
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Jobstock.settings')
django.setup()

from App.models import NavigationGroup, NavigationItem

def setup_hierarchical_navigation():
    print("=== Setting up Hierarchical Multilevel Navigation ===\n")
    print("Allowed Roles: hiring_manager, rpo_admin\n")
    
    # Step 1: Deactivate ALL existing navigation items
    print("Step 1: Deactivating all existing navigation items...")
    all_items = NavigationItem.objects.all()
    deactivated_count = all_items.update(is_active=False)
    print(f"  ✅ Deactivated {deactivated_count} navigation items\n")
    
    # Step 2: Deactivate all groups
    print("Step 2: Deactivating all navigation groups...")
    all_groups = NavigationGroup.objects.all()
    deactivated_groups = all_groups.update(is_active=False)
    print(f"  ✅ Deactivated {deactivated_groups} navigation groups\n")
    
    # Step 3: Create RPO Admin Navigation (already exists, just activate)
    print("Step 3: Setting up RPO Admin Navigation...")
    rpo_resume_group, _ = NavigationGroup.objects.update_or_create(
        slug='rpo-resume-management',
        defaults={
            'name': 'Resume Management',
            'visible_to_roles': ['rpo_admin'],
            'icon': 'fa-solid fa-file-pdf',
            'order': 1,
            'is_active': True
        }
    )
    print(f"  ✅ {rpo_resume_group.name} group activated")
    
    # RPO Resume Management Items
    rpo_upload, _ = NavigationItem.objects.update_or_create(
        group=rpo_resume_group,
        url_name='App:rpo_resume_upload',
        defaults={
            'title': 'Upload Resumes',
            'icon': 'fa-solid fa-upload',
            'order': 1,
            'is_active': True,
            'visible_to_roles': ['rpo_admin'],
            'parent': None
        }
    )
    print(f"    ✅ {rpo_upload.title}")
    
    rpo_list, _ = NavigationItem.objects.update_or_create(
        group=rpo_resume_group,
        url_name='App:rpo_resume_list',
        defaults={
            'title': 'All Resumes',
            'icon': 'fa-solid fa-list',
            'order': 2,
            'is_active': True,
            'visible_to_roles': ['rpo_admin'],
            'parent': None
        }
    )
    print(f"    ✅ {rpo_list.title}")
    
    rpo_dashboard, _ = NavigationItem.objects.update_or_create(
        group=rpo_resume_group,
        url_name='App:rpo_dashboard',
        defaults={
            'title': 'Dashboard',
            'icon': 'fa-solid fa-tachometer-alt',
            'order': 3,
            'is_active': True,
            'visible_to_roles': ['rpo_admin'],
            'parent': None
        }
    )
    print(f"    ✅ {rpo_dashboard.title}\n")
    
    # Step 4: Create Hiring Manager Navigation with multilevel hierarchy
    print("Step 4: Setting up Hiring Manager Navigation...")
    
    # Main Menu Group
    hiring_main_group, _ = NavigationGroup.objects.update_or_create(
        slug='hiring-manager-main',
        defaults={
            'name': 'Main Menu',
            'visible_to_roles': ['hiring_manager'],
            'icon': 'fa-solid fa-bars',
            'order': 1,
            'is_active': True
        }
    )
    print(f"  ✅ {hiring_main_group.name} group activated")
    
    # Dashboard (top level)
    hm_dashboard, _ = NavigationItem.objects.update_or_create(
        group=hiring_main_group,
        url_name='App:employer_dashboard',
        parent=None,
        defaults={
            'title': 'Dashboard',
            'icon': 'fa-solid fa-home',
            'order': 1,
            'is_active': True,
            'visible_to_roles': ['hiring_manager'],
        }
    )
    print(f"    ✅ {hm_dashboard.title}")
    
    # Job Management (top level with children)
    hm_jobs, _ = NavigationItem.objects.update_or_create(
        group=hiring_main_group,
        url_name='#',
        title='Job Management',
        parent=None,
        defaults={
            'icon': 'fa-solid fa-briefcase',
            'order': 2,
            'is_active': True,
            'visible_to_roles': ['hiring_manager'],
        }
    )
    print(f"    ✅ {hm_jobs.title} (Parent)")
    
    # Job Management > Post New Job (level 1 child)
    hm_post_job, _ = NavigationItem.objects.update_or_create(
        group=hiring_main_group,
        url_name='App:employer_submit_job',
        title='Post New Job',
        defaults={
            'icon': 'fa-solid fa-plus-circle',
            'order': 1,
            'is_active': True,
            'visible_to_roles': ['hiring_manager'],
            'parent': hm_jobs
        }
    )
    print(f"      └─ {hm_post_job.title}")
    
    # Job Management > Manage Jobs (level 1 child)
    hm_manage_jobs, _ = NavigationItem.objects.update_or_create(
        group=hiring_main_group,
        url_name='App:employer_jobs',
        title='Manage Jobs',
        defaults={
            'icon': 'fa-solid fa-tasks',
            'order': 2,
            'is_active': True,
            'visible_to_roles': ['hiring_manager'],
            'parent': hm_jobs
        }
    )
    print(f"      └─ {hm_manage_jobs.title}")
    
    # Job Management > Applications (level 1 child with sub-children)
    hm_applications, _ = NavigationItem.objects.update_or_create(
        group=hiring_main_group,
        url_name='#',
        title='Applications',
        defaults={
            'icon': 'fa-solid fa-file-alt',
            'order': 3,
            'is_active': True,
            'visible_to_roles': ['hiring_manager'],
            'parent': hm_jobs
        }
    )
    print(f"      └─ {hm_applications.title} (Sub-parent)")
    
    # Job Management > Applications > All Applications (level 2 child)
    hm_all_apps, _ = NavigationItem.objects.update_or_create(
        group=hiring_main_group,
        url_name='App:employer_applicants_jobs',
        title='All Applications',
        defaults={
            'icon': 'fa-solid fa-list',
            'order': 1,
            'is_active': True,
            'visible_to_roles': ['hiring_manager'],
            'parent': hm_applications
        }
    )
    print(f"         └─ {hm_all_apps.title}")
    
    # Job Management > Applications > Shortlisted (level 2 child)
    hm_shortlist, _ = NavigationItem.objects.update_or_create(
        group=hiring_main_group,
        url_name='App:employer_shortlist_candidates',
        title='Shortlisted',
        defaults={
            'icon': 'fa-solid fa-star',
            'order': 2,
            'is_active': True,
            'visible_to_roles': ['hiring_manager'],
            'parent': hm_applications
        }
    )
    print(f"         └─ {hm_shortlist.title}")
    
    # Candidates (top level)
    hm_candidates, _ = NavigationItem.objects.update_or_create(
        group=hiring_main_group,
        url_name='App:candidate_grid_1',
        title='Candidates',
        parent=None,
        defaults={
            'icon': 'fa-solid fa-users',
            'order': 3,
            'is_active': True,
            'visible_to_roles': ['hiring_manager'],
        }
    )
    print(f"    ✅ {hm_candidates.title}")
    
    # Messages (top level)
    hm_messages, _ = NavigationItem.objects.update_or_create(
        group=hiring_main_group,
        url_name='App:employer_messages',
        title='Messages',
        parent=None,
        defaults={
            'icon': 'fa-solid fa-envelope',
            'order': 4,
            'is_active': True,
            'visible_to_roles': ['hiring_manager'],
            'badge_text': 'New',
            'badge_class': 'badge-danger'
        }
    )
    print(f"    ✅ {hm_messages.title}")
    
    # Settings Group for Hiring Manager
    hiring_settings_group, _ = NavigationGroup.objects.update_or_create(
        slug='hiring-manager-settings',
        defaults={
            'name': 'Settings',
            'visible_to_roles': ['hiring_manager'],
            'icon': 'fa-solid fa-cog',
            'order': 2,
            'is_active': True
        }
    )
    print(f"\n  ✅ {hiring_settings_group.name} group activated")
    
    # Profile
    hm_profile, _ = NavigationItem.objects.update_or_create(
        group=hiring_settings_group,
        url_name='App:employer_profile',
        defaults={
            'title': 'Company Profile',
            'icon': 'fa-solid fa-building',
            'order': 1,
            'is_active': True,
            'visible_to_roles': ['hiring_manager'],
            'parent': None
        }
    )
    print(f"    ✅ {hm_profile.title}")
    
    # Change Password
    hm_password, _ = NavigationItem.objects.update_or_create(
        group=hiring_settings_group,
        url_name='App:employer_change_password',
        defaults={
            'title': 'Change Password',
            'icon': 'fa-solid fa-key',
            'order': 2,
            'is_active': True,
            'visible_to_roles': ['hiring_manager'],
            'parent': None
        }
    )
    print(f"    ✅ {hm_password.title}")
    
    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    
    # Count active items per role (SQLite compatible)
    all_active_items = NavigationItem.objects.filter(is_active=True)
    
    rpo_items = 0
    hiring_items = 0
    
    for item in all_active_items:
        roles = item.visible_to_roles or []
        if 'rpo_admin' in roles:
            rpo_items += 1
        if 'hiring_manager' in roles:
            hiring_items += 1
    
    print(f"\n✅ RPO Admin Navigation:")
    print(f"   - Groups: 1")
    print(f"   - Items: {rpo_items}")
    
    print(f"\n✅ Hiring Manager Navigation:")
    print(f"   - Groups: 2")
    print(f"   - Items: {hiring_items}")
    print(f"   - Includes multilevel hierarchy (3 levels deep)")
    
    print(f"\n⚪ All other user roles: DEACTIVATED")
    print("\n✅ Setup complete!")

if __name__ == "__main__":
    setup_hierarchical_navigation()
