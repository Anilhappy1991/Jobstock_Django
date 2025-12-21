"""
Update RPO Admin Navigation - Set Upload Resumes as Active
Ensures Upload Resumes navigation item exists and is the only active item
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Jobstock.settings')
django.setup()

from App.models import NavigationGroup, NavigationItem

def update_navigation():
    print("=== Updating RPO Admin Navigation ===\n")
    
    # Step 1: Get or create the Resume Management group
    resume_group, group_created = NavigationGroup.objects.get_or_create(
        slug='rpo-resume-management',
        defaults={
            'name': 'Resume Management',
            'visible_to_roles': ['rpo_admin'],
            'icon': 'fa-solid fa-file-pdf',
            'order': 2,
            'is_active': True
        }
    )
    
    if group_created:
        print(f"✅ Created new group: {resume_group.name}")
    else:
        print(f"✓ Found existing group: {resume_group.name}")
        # Ensure group is active
        if not resume_group.is_active:
            resume_group.is_active = True
            resume_group.save()
            print("  ✅ Activated group")
    
    # Step 2: Deactivate ALL navigation items first
    all_items = NavigationItem.objects.all()
    deactivated_count = 0
    for item in all_items:
        if item.is_active:
            item.is_active = False
            item.save()
            deactivated_count += 1
            print(f"  ⚪ Deactivated: {item.title} ({item.url_name})")
    
    print(f"\n✅ Deactivated {deactivated_count} navigation items")
    
    # Step 3: Get or create Upload Resumes navigation item
    upload_item, item_created = NavigationItem.objects.get_or_create(
        group=resume_group,
        url_name='App:rpo_resume_upload',
        defaults={
            'title': 'Upload Resumes',
            'icon': 'fa-solid fa-upload',
            'order': 1,
            'is_active': True,
            'badge_text': None,
            'badge_color': None
        }
    )
    
    if item_created:
        print(f"\n✅ Created new item: {upload_item.title}")
    else:
        print(f"\n✓ Found existing item: {upload_item.title}")
        # Ensure this item is active
        if not upload_item.is_active:
            upload_item.is_active = True
            upload_item.save()
            print("  ✅ Activated this item")
        else:
            print("  ✓ Already active")
    
    # Step 4: Display summary
    print("\n=== Summary ===")
    print(f"Group: {resume_group.name} (slug: {resume_group.slug})")
    print(f"Item: {upload_item.title}")
    print(f"URL Name: {upload_item.url_name}")
    print(f"Icon: {upload_item.icon}")
    print(f"Order: {upload_item.order}")
    print(f"Active: {upload_item.is_active}")
    print(f"Visible to roles: {resume_group.visible_to_roles}")
    
    # Step 5: Show all active items (should be only one)
    active_items = NavigationItem.objects.filter(is_active=True)
    print(f"\n✅ Total active navigation items: {active_items.count()}")
    for item in active_items:
        print(f"  ✓ {item.title} ({item.url_name}) - Group: {item.group.name}")
    
    print("\n✅ Navigation update complete!")

if __name__ == "__main__":
    update_navigation()
