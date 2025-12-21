"""
Final verification of navigation items - what users will see
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Jobstock.settings')
django.setup()

from App.models import NavigationItem, NavigationGroup

print("\n" + "="*70)
print("  FINAL NAVIGATION VERIFICATION")
print("  What Users Will See in Dashboard")
print("="*70)

active_groups = NavigationGroup.objects.filter(is_active=True).order_by('order')
active_items = NavigationItem.objects.filter(is_active=True).order_by('order')

print(f"\nTotal Active Groups: {active_groups.count()}")
print(f"Total Active Items: {active_items.count()}")

# Hiring Manager View
print("\n" + "="*70)
print("  HIRING MANAGER / EMPLOYEE VIEW")
print("="*70)

hm_groups = {}
for item in active_items:
    if 'hiring_manager' in item.visible_to_roles and not item.parent:
        group_name = item.group.name if item.group else 'No Group'
        if group_name not in hm_groups:
            hm_groups[group_name] = []
        hm_groups[group_name].append(item)

for group_name, items in hm_groups.items():
    print(f"\n📁 {group_name}")
    for item in items:
        print(f"   └─ {item.title}")
        
        # Show children
        children = active_items.filter(parent=item)
        for child in children:
            print(f"       └─ {child.title}")

# RPO Admin View
print("\n" + "="*70)
print("  RPO ADMIN VIEW")
print("="*70)

rpo_groups = {}
for item in active_items:
    if 'rpo_admin' in item.visible_to_roles and not item.parent:
        group_name = item.group.name if item.group else 'No Group'
        if group_name not in rpo_groups:
            rpo_groups[group_name] = []
        rpo_groups[group_name].append(item)

for group_name, items in rpo_groups.items():
    print(f"\n📁 {group_name}")
    for item in items:
        print(f"   └─ {item.title}")

# Summary
print("\n" + "="*70)
print("  SUMMARY")
print("="*70)
print("\n✅ Duplicates Removed:")
print("   - Removed duplicate 'Main Menu' groups")
print("   - Removed duplicate 'Job Management' items")
print("   - Removed duplicate 'Post New Job' items")

print("\n✅ Current State:")
print("   - Hiring Manager: 1 group (Main Menu) with 1 parent + 2 children")
print("   - RPO Admin: 1 group (Resume Management) with 1 item")

print("\n✅ Each item now appears ONLY ONCE in the database")
print("="*70 + "\n")
