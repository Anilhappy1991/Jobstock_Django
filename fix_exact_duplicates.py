"""
Find exact duplicate items and deactivate them
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Jobstock.settings')
django.setup()

from App.models import NavigationItem

print("\n" + "="*70)
print("  Finding Exact Duplicate Items")
print("="*70)

# Get all active items for hiring_manager
active_items = NavigationItem.objects.filter(is_active=True)

print("\nAll Active Items:")
for item in active_items:
    if 'hiring_manager' in item.visible_to_roles:
        print(f"  ID: {item.id:3} | {item.title:20} | Parent: {item.parent.title if item.parent else 'None':20} | URL: {item.url_name}")

# Find duplicates by title and parent
print("\n" + "-"*70)
print("  Finding Duplicates by Title + Parent")
print("-"*70)

seen = {}
duplicates = []

for item in active_items:
    if 'hiring_manager' in item.visible_to_roles:
        key = f"{item.title}|{item.parent_id if item.parent else 'None'}"
        
        if key in seen:
            # This is a duplicate
            duplicates.append(item)
            print(f"\n  DUPLICATE FOUND: {item.title}")
            print(f"    First:  ID {seen[key].id}")
            print(f"    Duplicate: ID {item.id} (will deactivate)")
        else:
            seen[key] = item

# Deactivate duplicates
if duplicates:
    print("\n" + "="*70)
    print("  Deactivating Duplicates")
    print("="*70)
    
    for item in duplicates:
        print(f"  ✓ Deactivating: {item.title} (ID: {item.id})")
        item.is_active = False
        item.save()
    
    print(f"\n  Total deactivated: {len(duplicates)}")
else:
    print("\n  ✓ No duplicates found to deactivate")

# Show final result
print("\n" + "="*70)
print("  FINAL ACTIVE ITEMS")
print("="*70)

active_items = NavigationItem.objects.filter(is_active=True)

print("\nHiring Manager Navigation:")
for item in active_items:
    if 'hiring_manager' in item.visible_to_roles:
        parent_name = item.parent.title if item.parent else 'TOP LEVEL'
        print(f"  ✓ {item.title:20} (Parent: {parent_name})")

print("\nRPO Admin Navigation:")
for item in active_items:
    if 'rpo_admin' in item.visible_to_roles:
        print(f"  ✓ {item.title}")

print("="*70 + "\n")
