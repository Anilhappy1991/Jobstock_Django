"""
Verify active navigation items
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Jobstock.settings')
django.setup()

from App.models import NavigationItem, NavigationGroup

print("\n" + "="*70)
print("  ACTIVE NAVIGATION ITEMS VERIFICATION")
print("="*70)

# Get active groups
active_groups = NavigationGroup.objects.filter(is_active=True)
print(f"\nActive Groups: {active_groups.count()}")
for group in active_groups:
    print(f"  ✓ {group.name} - {group.slug}")

# Get active items
active_items = NavigationItem.objects.filter(is_active=True)
print(f"\nActive Items: {active_items.count()}")
print("\nRPO Admin Navigation:")
for item in active_items:
    if 'rpo_admin' in item.visible_to_roles:
        print(f"  ✓ {item.title}")
        print(f"    - URL: {item.url_name}")
        print(f"    - Group: {item.group.name if item.group else 'None'}")

print("\nHiring Manager Navigation:")
for item in active_items:
    if 'hiring_manager' in item.visible_to_roles:
        print(f"  ✓ {item.title}")
        print(f"    - URL: {item.url_name}")
        print(f"    - Group: {item.group.name if item.group else 'None'}")
        print(f"    - Parent: {item.parent.title if item.parent else 'None (Top Level)'}")

print("\n" + "="*70)
print("  TEST: What will users see?")
print("="*70)

# Test what RPO Admin sees
print("\n1. RPO Admin will see:")
rpo_count = 0
for item in active_items:
    if 'rpo_admin' in item.visible_to_roles:
        print(f"   - {item.title}")
        rpo_count += 1
if rpo_count == 0:
    print("   (No items)")

# Test what Hiring Manager sees
print("\n2. Hiring Manager (or Employee) will see:")
hm_count = 0
for item in active_items:
    if 'hiring_manager' in item.visible_to_roles:
        print(f"   - {item.title}")
        hm_count += 1
if hm_count == 0:
    print("   (No items)")

print("\n" + "="*70 + "\n")
