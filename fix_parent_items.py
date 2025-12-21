"""
Fix navigation: Activate parent items for active children
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Jobstock.settings')
django.setup()

from App.models import NavigationItem

print("\n" + "="*70)
print("  Activating Parent Items for Active Children")
print("="*70)

# Get all active items that have parents
active_items_with_parents = NavigationItem.objects.filter(
    is_active=True,
    parent__isnull=False
)

print(f"\nActive items with parents: {active_items_with_parents.count()}")

parents_to_activate = set()

for item in active_items_with_parents:
    if item.parent:
        parents_to_activate.add(item.parent)
        print(f"  ✓ {item.title} → needs parent: {item.parent.title}")

print(f"\n{'-'*70}")
print(f"  Parents to activate: {len(parents_to_activate)}")
print(f"{'-'*70}")

for parent in parents_to_activate:
    parent.is_active = True
    parent.save()
    print(f"  ✓ ACTIVATED: {parent.title}")
    
    # Also check if this parent has a parent
    if parent.parent and not parent.parent.is_active:
        parent.parent.is_active = True
        parent.parent.save()
        print(f"    ✓ ACTIVATED grandparent: {parent.parent.title}")

print("\n" + "="*70)
print("  SUMMARY")
print("="*70)

# Show current active items hierarchy
active_items = NavigationItem.objects.filter(is_active=True).order_by('group__name', 'order')
print(f"\nTotal active items: {active_items.count()}")

groups = {}
for item in active_items:
    group_name = item.group.name if item.group else 'No Group'
    if group_name not in groups:
        groups[group_name] = []
    groups[group_name].append(item)

for group_name, items in groups.items():
    print(f"\n📁 {group_name}")
    for item in items:
        indent = "  "
        if item.parent:
            indent = "    "
        if item.parent and item.parent.parent:
            indent = "      "
        print(f"{indent}✓ {item.title}")

print("="*70 + "\n")
