"""
Clean up orphaned navigation items (items with inactive parents)
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Jobstock.settings')
django.setup()

from App.models import NavigationItem

print("\n" + "="*70)
print("  Cleaning Up Orphaned Items")
print("="*70)

# Find items with inactive parents
active_items = NavigationItem.objects.filter(is_active=True, parent__isnull=False)

orphaned_items = []

print("\nChecking for items with inactive parents:\n")

for item in active_items:
    if item.parent and not item.parent.is_active:
        orphaned_items.append(item)
        print(f"  ⚠️  ORPHANED: {item.title} (ID: {item.id})")
        print(f"      Parent: {item.parent.title} (ID: {item.parent_id}) is INACTIVE")

if orphaned_items:
    print("\n" + "-"*70)
    print("  Deactivating Orphaned Items")
    print("-"*70)
    
    for item in orphaned_items:
        print(f"  ✓ Deactivating: {item.title} (ID: {item.id})")
        item.is_active = False
        item.save()
    
    print(f"\n  Total deactivated: {len(orphaned_items)}")
else:
    print("\n  ✓ No orphaned items found")

print("\n" + "="*70)
print("  FINAL ACTIVE NAVIGATION")
print("="*70)

active_items = NavigationItem.objects.filter(is_active=True)

print("\nHiring Manager Navigation:")
count = 0
for item in active_items:
    if 'hiring_manager' in item.visible_to_roles:
        parent_name = item.parent.title if item.parent else 'TOP LEVEL'
        print(f"  {count+1}. {item.title} (Parent: {parent_name})")
        count += 1

print(f"\n  Total: {count} items")

print("\nRPO Admin Navigation:")
count = 0
for item in active_items:
    if 'rpo_admin' in item.visible_to_roles:
        print(f"  {count+1}. {item.title}")
        count += 1

print(f"\n  Total: {count} items")

print("="*70 + "\n")
