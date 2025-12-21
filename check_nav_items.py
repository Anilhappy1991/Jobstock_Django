"""Check navigation items in database"""
import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Jobstock.settings')
django.setup()

from App.models import NavigationGroup, NavigationItem
from django.urls import reverse, NoReverseMatch

print("=== Navigation Items for hiring_manager ===\n")

# Get all groups - filter in Python since SQLite doesn't support contains on JSON
all_groups = NavigationGroup.objects.filter(is_active=True).prefetch_related('items')

groups = [g for g in all_groups if 'hiring_manager' in (g.visible_to_roles or [])]

for group in groups:
    print(f"\nGroup: {group.name}")
    print("-" * 50)
    
    items = group.items.filter(is_active=True, parent__isnull=True).order_by('order')
    
    for item in items:
        # Try to resolve URL
        try:
            url = reverse(item.url_name)
            url_status = "✓ OK"
        except NoReverseMatch:
            url = "#"
            url_status = "✗ NOT FOUND"
        
        print(f"  {item.title}")
        print(f"    URL Name: {item.url_name}")
        print(f"    URL: {url} ({url_status})")
        print(f"    Roles: {item.visible_to_roles}")
        
        # Check children
        if item.children.filter(is_active=True).exists():
            print(f"    Children:")
            for child in item.children.filter(is_active=True).order_by('order'):
                try:
                    child_url = reverse(child.url_name)
                    child_status = "✓"
                except NoReverseMatch:
                    child_url = "#"
                    child_status = "✗"
                print(f"      - {child.title} ({child.url_name}) {child_status}")
        print()

print("\n=== Summary ===")
print(f"Total Groups: {groups.count()}")
print(f"Total Items: {NavigationItem.objects.filter(is_active=True).count()}")
