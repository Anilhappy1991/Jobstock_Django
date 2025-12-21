"""Debug navigation issue"""
import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Jobstock.settings')
django.setup()

from django.contrib.auth import get_user_model
from App.services.navigation_service import NavigationService
from App.models import NavigationGroup

User = get_user_model()

print("=== Navigation Debug ===\n")

# Get user
user = User.objects.filter(username='rituranjangupta').first()
if not user:
    print("❌ User not found!")
    sys.exit(1)

print(f"✓ User: {user.username}")
print(f"  Is Superuser: {user.is_superuser}")
print(f"  Groups: {', '.join([g.name for g in user.groups.all()])}")

# Check user profile role
try:
    profile_role = user.profile.role
    print(f"  Profile Role: {profile_role}")
except Exception as e:
    print(f"  Profile Role: ERROR - {e}")
    profile_role = None

# Test navigation service
print("\n=== Testing NavigationService ===")
service = NavigationService()
result = service.get_navigation_for_user(user)

print(f"Success: {result.get('success')}")
print(f"Message: {result.get('message')}")

if result.get('success'):
    navigation = result.get('data', {}).get('navigation', [])
    print(f"Navigation Groups Returned: {len(navigation)}")
    
    for group in navigation:
        print(f"\n  Group: {group.get('name')}")
        items = group.get('items', [])
        print(f"  Items: {len(items)}")
        for item in items[:3]:
            print(f"    - {item.get('title')} → {item.get('url')}")
else:
    print(f"Error: {result.get('error')}")
    print(f"Details: {result.get('error_details')}")

# Check navigation groups in DB
print("\n=== Database Check ===")
all_groups = NavigationGroup.objects.filter(is_active=True)
print(f"Total Active Groups: {all_groups.count()}")

for group in all_groups:
    print(f"\nGroup: {group.name}")
    print(f"  Visible to roles: {group.visible_to_roles}")
    print(f"  Total items: {group.items.filter(is_active=True).count()}")
