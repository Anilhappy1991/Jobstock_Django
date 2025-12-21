"""
Debug navigation service for hiring manager
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Jobstock.settings')
django.setup()

from App.models import NavigationItem, NavigationGroup
from django.contrib.auth.models import User

print("\n" + "="*70)
print("  DEBUG: Hiring Manager Navigation Items")
print("="*70)

# Get hiring manager active items
hm_items = NavigationItem.objects.filter(is_active=True)
print(f"\nAll Active Items: {hm_items.count()}")

for item in hm_items:
    if 'hiring_manager' in item.visible_to_roles:
        print(f"\n  Item: {item.title}")
        print(f"    - URL: {item.url_name}")
        print(f"    - Group: {item.group.name if item.group else 'None'}")
        print(f"    - Parent: {item.parent.title if item.parent else 'None (TOP LEVEL)'}")
        print(f"    - Is Top Level: {item.parent is None}")

# Check if "Job Management" parent exists
print("\n" + "-"*70)
print("  Checking Parent Items")
print("-"*70)

parents = NavigationItem.objects.filter(title__icontains='Job Management')
for parent in parents:
    print(f"\n  Parent Item: {parent.title}")
    print(f"    - Active: {parent.is_active}")
    print(f"    - URL: {parent.url_name}")
    print(f"    - Roles: {parent.visible_to_roles}")
    
    children = NavigationItem.objects.filter(parent=parent)
    print(f"    - Children: {children.count()}")
    for child in children:
        print(f"      - {child.title} (Active: {child.is_active})")

print("\n" + "="*70 + "\n")
