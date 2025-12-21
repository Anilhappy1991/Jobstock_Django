"""
Deactivate all navigation items except Resume Upload and Post a Job
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Jobstock.settings')
django.setup()

from App.models import NavigationItem, NavigationGroup

print("\n" + "="*70)
print("  Deactivating Navigation Items")
print("  KEEPING ONLY: Resume Upload & Post a Job")
print("="*70)

# First, deactivate ALL items
all_items = NavigationItem.objects.all()
total_items = all_items.count()
all_items.update(is_active=False)
print(f"\n✓ Deactivated all {total_items} navigation items")

# Now activate only the two specified items
items_to_keep = [
    'App:rpo_resume_upload',  # Upload Resumes for RPO Admin
    'App:employer_submit_job',  # Post New Job for Hiring Manager
]

activated_count = 0
for url_name in items_to_keep:
    items = NavigationItem.objects.filter(url_name=url_name)
    if items.exists():
        items.update(is_active=True)
        for item in items:
            print(f"\n✓ ACTIVATED: {item.title}")
            print(f"  - URL: {item.url_name}")
            print(f"  - Group: {item.group.name if item.group else 'None'}")
            print(f"  - Roles: {item.visible_to_roles}")
            activated_count += 1
    else:
        print(f"\n✗ NOT FOUND: {url_name}")

# Also activate the parent groups for these items
print("\n" + "-"*70)
print("  Activating Parent Groups")
print("-"*70)

active_items = NavigationItem.objects.filter(is_active=True)
active_groups = set()

for item in active_items:
    if item.group:
        active_groups.add(item.group)

# Deactivate all groups first
NavigationGroup.objects.all().update(is_active=False)

# Activate only groups with active items
for group in active_groups:
    group.is_active = True
    group.save()
    print(f"✓ Activated group: {group.name}")

print("\n" + "="*70)
print("  SUMMARY")
print("="*70)
print(f"  Total items in database: {total_items}")
print(f"  Active items: {activated_count}")
print(f"  Deactivated items: {total_items - activated_count}")
print(f"  Active groups: {len(active_groups)}")
print("\n  Active Items:")
for item in NavigationItem.objects.filter(is_active=True):
    print(f"    - {item.title} ({item.url_name})")
print("="*70 + "\n")
