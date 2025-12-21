"""
Remove 'Job Templates' navigation item from hiring manager menu.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Jobstock.settings')
django.setup()

from App.models import NavigationItem

print("=" * 70)
print("REMOVE 'JOB TEMPLATES' FROM HIRING MANAGER MENU")
print("=" * 70)

# Find "Job Templates" navigation items
job_templates_items = NavigationItem.objects.filter(title__icontains='Job Templates')

print(f"\nFound {job_templates_items.count()} 'Job Templates' item(s):\n")

for item in job_templates_items:
    print(f"  ID: {item.id}")
    print(f"  Title: {item.title}")
    print(f"  URL Name: {item.url_name}")
    print(f"  Group: {item.group.name if item.group else 'None'}")
    print(f"  Parent: {item.parent.title if item.parent else 'None'}")
    print(f"  Roles: {item.visible_to_roles}")
    print(f"  Active: {item.is_active}")
    print()

if job_templates_items.exists():
    print("=" * 70)
    print("DEACTIVATING 'JOB TEMPLATES'...")
    print("=" * 70)
    
    for item in job_templates_items:
        if item.is_active:
            item.is_active = False
            item.save()
            print(f"✅ Deactivated: ID {item.id} - '{item.title}' (Roles: {item.visible_to_roles})")
        else:
            print(f"⚠️  Already inactive: ID {item.id} - '{item.title}'")
    
    print("\n" + "=" * 70)
    print("VERIFICATION - ACTIVE HIRING MANAGER ITEMS")
    print("=" * 70)
    
    # Get all active items that have 'hiring_manager' in visible_to_roles
    from django.db.models import Q
    hm_items = NavigationItem.objects.filter(
        is_active=True
    ).order_by('group__name', 'parent__title', 'title')
    
    # Filter items that include hiring_manager in their roles
    hm_items_filtered = [item for item in hm_items if 'hiring_manager' in item.visible_to_roles]
    
    print(f"\nActive items for hiring_manager: {len(hm_items_filtered)}\n")
    for item in hm_items_filtered:
        parent_info = f" (under {item.parent.title})" if item.parent else ""
        print(f"  - {item.title}{parent_info}")
    
    print("\n" + "=" * 70)
else:
    print("⚠️  No 'Job Templates' items found")
    print("=" * 70)
