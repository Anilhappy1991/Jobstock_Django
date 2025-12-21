"""
Setup RPO Admin Navigation
Creates navigation groups and items for RPO Admin role
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Jobstock.settings')
django.setup()

from App.models import NavigationGroup, NavigationItem

def setup_rpo_navigation():
    print("=== Setting up RPO Admin Navigation ===\n")
    
    # Delete existing RPO navigation if exists
    all_groups = NavigationGroup.objects.filter(is_active=True)
    existing_groups = [g for g in all_groups if 'rpo_admin' in (g.visible_to_roles or [])]
    if existing_groups:
        print(f"Removing {len(existing_groups)} existing RPO navigation groups...")
        for group in existing_groups:
            # Only delete if it's RPO-specific (not shared)
            visible_roles = group.visible_to_roles or []
            if visible_roles == ['rpo_admin']:
                group.delete()
            elif 'rpo_admin' in visible_roles and len(visible_roles) > 1:
                print(f"  Skipping shared group: {group.name}")
    
    # Create RPO Admin Dashboard Navigation Group
    dashboard_group, created = NavigationGroup.objects.get_or_create(
        slug='rpo-dashboard',
        defaults={
            'name': 'Dashboard',
            'visible_to_roles': ['rpo_admin'],
            'icon': 'fa-solid fa-home',
            'order': 1,
            'is_active': True
        }
    )
    if not created:
        dashboard_group.visible_to_roles = ['rpo_admin']
        dashboard_group.save()
    
    print(f"✅ Created/Updated: {dashboard_group.name}")
    
    # Dashboard items
    dashboard_items = [
        {'title': 'Dashboard Home', 'url_name': 'App:rpo_dashboard', 'icon': 'fa-solid fa-tachometer-alt', 'order': 1},
    ]
    
    for item_data in dashboard_items:
        item, created = NavigationItem.objects.get_or_create(
            group=dashboard_group,
            title=item_data['title'],
            defaults={
                'url_name': item_data['url_name'],
                'icon': item_data['icon'],
                'order': item_data['order'],
                'is_active': True
            }
        )
        print(f"  {'✅ Created' if created else '✓ Exists'}: {item.title}")
    
    # Create Resume Management Navigation Group
    resume_group, created = NavigationGroup.objects.get_or_create(
        slug='rpo-resume-management',
        defaults={
            'name': 'Resume Management',
            'visible_to_roles': ['rpo_admin'],
            'icon': 'fa-solid fa-file-pdf',
            'order': 2,
            'is_active': True
        }
    )
    if not created:
        resume_group.visible_to_roles = ['rpo_admin']
        resume_group.save()
    
    print(f"\n✅ Created/Updated: {resume_group.name}")
    
    # Resume management items
    resume_items = [
        {'title': 'Upload Resumes', 'url_name': 'App:rpo_resume_upload', 'icon': 'fa-solid fa-upload', 'order': 1},
        {'title': 'All Resumes', 'url_name': 'App:rpo_resume_list', 'icon': 'fa-solid fa-list', 'order': 2},
    ]
    
    for item_data in resume_items:
        item, created = NavigationItem.objects.get_or_create(
            group=resume_group,
            title=item_data['title'],
            defaults={
                'url_name': item_data['url_name'],
                'icon': item_data['icon'],
                'order': item_data['order'],
                'is_active': True
            }
        )
        print(f"  {'✅ Created' if created else '✓ Exists'}: {item.title}")
    
    # Create Candidate Management Navigation Group (shared with employer)
    candidate_group, created = NavigationGroup.objects.get_or_create(
        slug='rpo-candidate-management',
        defaults={
            'name': 'Candidate Management',
            'visible_to_roles': ['rpo_admin', 'hiring_manager'],
            'icon': 'fa-solid fa-users',
            'order': 3,
            'is_active': True
        }
    )
    if not created:
        # Update to include both roles
        visible_roles = candidate_group.visible_to_roles or []
        if 'rpo_admin' not in visible_roles:
            visible_roles.append('rpo_admin')
        if 'hiring_manager' not in visible_roles:
            visible_roles.append('hiring_manager')
        candidate_group.visible_to_roles = visible_roles
        candidate_group.save()
    
    print(f"\n✅ Created/Updated: {candidate_group.name}")
    
    # Candidate management items
    candidate_items = [
        {'title': 'All Candidates', 'url_name': 'App:candidate_grid_1', 'icon': 'fa-solid fa-user-group', 'order': 1},
        {'title': 'Shortlisted', 'url_name': 'App:employer_shortlist_candidates', 'icon': 'fa-solid fa-star', 'order': 2},
    ]
    
    for item_data in candidate_items:
        item, created = NavigationItem.objects.get_or_create(
            group=candidate_group,
            title=item_data['title'],
            defaults={
                'url_name': item_data['url_name'],
                'icon': item_data['icon'],
                'order': item_data['order'],
                'is_active': True
            }
        )
        print(f"  {'✅ Created' if created else '✓ Exists'}: {item.title}")
    
    # Create Settings Navigation Group
    settings_group, created = NavigationGroup.objects.get_or_create(
        slug='rpo-settings',
        defaults={
            'name': 'Settings',
            'visible_to_roles': ['rpo_admin'],
            'icon': 'fa-solid fa-cog',
            'order': 4,
            'is_active': True
        }
    )
    if not created:
        settings_group.visible_to_roles = ['rpo_admin']
        settings_group.save()
    
    print(f"\n✅ Created/Updated: {settings_group.name}")
    
    # Settings items
    settings_items = [
        {'title': 'Profile', 'url_name': 'App:employer_profile', 'icon': 'fa-solid fa-user', 'order': 1},
        {'title': 'Change Password', 'url_name': 'App:employer_change_password', 'icon': 'fa-solid fa-lock', 'order': 2},
    ]
    
    for item_data in settings_items:
        item, created = NavigationItem.objects.get_or_create(
            group=settings_group,
            title=item_data['title'],
            defaults={
                'url_name': item_data['url_name'],
                'icon': item_data['icon'],
                'order': item_data['order'],
                'is_active': True
            }
        )
        print(f"  {'✅ Created' if created else '✓ Exists'}: {item.title}")
    
    print("\n" + "="*60)
    print("RPO Admin Navigation Setup Complete!")
    print("="*60)
    
    # Show summary
    all_groups = NavigationGroup.objects.filter(is_active=True)
    rpo_groups = [g for g in all_groups if 'rpo_admin' in (g.visible_to_roles or [])]
    total_items = sum(g.items.count() for g in rpo_groups)
    
    print(f"\nTotal Navigation Groups for RPO Admin: {len(rpo_groups)}")
    print(f"Total Navigation Items: {total_items}\n")
    
    for group in rpo_groups:
        print(f"📁 {group.name} ({group.items.count()} items)")
        for item in group.items.all().order_by('order'):
            print(f"   └─ {item.title} → {item.url_name}")

if __name__ == '__main__':
    setup_rpo_navigation()
