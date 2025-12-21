"""
Find and fix duplicate navigation items in database
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Jobstock.settings')
django.setup()

from App.models import NavigationItem, NavigationGroup
from django.db.models import Count

print("\n" + "="*70)
print("  Finding Duplicate Navigation Items")
print("="*70)

# Find duplicate groups
print("\n1. Checking for Duplicate Groups:")
groups = NavigationGroup.objects.filter(is_active=True)
group_names = {}
for group in groups:
    if group.name not in group_names:
        group_names[group.name] = []
    group_names[group.name].append(group)

duplicates_found = False
for name, group_list in group_names.items():
    if len(group_list) > 1:
        duplicates_found = True
        print(f"\n  ⚠️  DUPLICATE: '{name}' appears {len(group_list)} times")
        for i, group in enumerate(group_list):
            print(f"      {i+1}. ID: {group.id}, Slug: {group.slug}, Active: {group.is_active}")

if not duplicates_found:
    print("  ✓ No duplicate groups found")

# Find duplicate items (same title, same group, same parent)
print("\n2. Checking for Duplicate Items:")
active_items = NavigationItem.objects.filter(is_active=True)
item_signatures = {}

for item in active_items:
    # Create a signature: title + group + parent
    signature = f"{item.title}|{item.group_id}|{item.parent_id}|{item.url_name}"
    if signature not in item_signatures:
        item_signatures[signature] = []
    item_signatures[signature].append(item)

duplicates_found = False
items_to_keep = []
items_to_deactivate = []

for signature, item_list in item_signatures.items():
    if len(item_list) > 1:
        duplicates_found = True
        title = item_list[0].title
        print(f"\n  ⚠️  DUPLICATE: '{title}' appears {len(item_list)} times")
        
        # Keep the first one, deactivate the rest
        items_to_keep.append(item_list[0])
        for i, item in enumerate(item_list):
            group_name = item.group.name if item.group else 'None'
            parent_name = item.parent.title if item.parent else 'None'
            action = "KEEP" if i == 0 else "DEACTIVATE"
            print(f"      {i+1}. ID: {item.id}, Group: {group_name}, Parent: {parent_name} → {action}")
            
            if i > 0:
                items_to_deactivate.append(item)

if not duplicates_found:
    print("  ✓ No duplicate items found")

# Deactivate duplicates
if items_to_deactivate:
    print("\n" + "="*70)
    print("  Deactivating Duplicate Items")
    print("="*70)
    
    for item in items_to_deactivate:
        item.is_active = False
        item.save()
        group_name = item.group.name if item.group else 'None'
        print(f"  ✓ Deactivated: {item.title} (ID: {item.id}, Group: {group_name})")
    
    print(f"\n  Total deactivated: {len(items_to_deactivate)}")

# Also check and deactivate duplicate groups
duplicate_groups_to_deactivate = []
for name, group_list in group_names.items():
    if len(group_list) > 1:
        # Keep the first, deactivate others
        for i, group in enumerate(group_list):
            if i > 0:
                duplicate_groups_to_deactivate.append(group)

if duplicate_groups_to_deactivate:
    print("\n" + "="*70)
    print("  Deactivating Duplicate Groups")
    print("="*70)
    
    for group in duplicate_groups_to_deactivate:
        group.is_active = False
        group.save()
        print(f"  ✓ Deactivated: {group.name} (ID: {group.id}, Slug: {group.slug})")
    
    print(f"\n  Total deactivated: {len(duplicate_groups_to_deactivate)}")

print("\n" + "="*70)
print("  FINAL SUMMARY")
print("="*70)

# Show what's left active
active_groups = NavigationGroup.objects.filter(is_active=True)
active_items = NavigationItem.objects.filter(is_active=True)

print(f"\nActive Groups: {active_groups.count()}")
for group in active_groups:
    print(f"  ✓ {group.name} (ID: {group.id})")

print(f"\nActive Items by Role:")
print("\nHiring Manager Items:")
for item in active_items:
    if 'hiring_manager' in item.visible_to_roles:
        group_name = item.group.name if item.group else 'None'
        parent_name = item.parent.title if item.parent else 'Top Level'
        print(f"  ✓ {item.title} (Group: {group_name}, Parent: {parent_name})")

print("\nRPO Admin Items:")
for item in active_items:
    if 'rpo_admin' in item.visible_to_roles:
        group_name = item.group.name if item.group else 'None'
        print(f"  ✓ {item.title} (Group: {group_name})")

print("="*70 + "\n")
