"""
Test employer dashboard navigation items
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Jobstock.settings')
django.setup()

from django.contrib.auth.models import User
from App.services.navigation_service import NavigationService

print("\n" + "="*70)
print("  EMPLOYER DASHBOARD - Navigation Items Test")
print("="*70)

# Test for hiring_manager user
try:
    hm_user = User.objects.filter(profile__role='hiring_manager').first()
    if hm_user:
        print(f"\n1. Hiring Manager User: {hm_user.username}")
        print(f"   Role: {hm_user.profile.role}")
        
        nav_response = NavigationService.get_navigation_for_user(hm_user)
        if hasattr(nav_response, 'to_dict'):
            nav_response = nav_response.to_dict()
        
        if nav_response.get('success'):
            groups = nav_response.get('data', {}).get('navigation', [])
            print(f"   Navigation Groups: {len(groups)}")
            
            for group in groups:
                print(f"\n   📁 {group['name']}")
                for item in group.get('items', []):
                    print(f"      ✓ {item['title']} → {item['url']}")
        else:
            print(f"   ❌ Error: {nav_response.get('message')}")
    else:
        print("\n1. No hiring_manager user found")
except Exception as e:
    print(f"\n1. Error: {str(e)}")

# Test for rpo_admin user
try:
    rpo_user = User.objects.filter(profile__role='rpo_admin').first()
    if rpo_user:
        print(f"\n2. RPO Admin User: {rpo_user.username}")
        print(f"   Role: {rpo_user.profile.role}")
        
        nav_response = NavigationService.get_navigation_for_user(rpo_user)
        if hasattr(nav_response, 'to_dict'):
            nav_response = nav_response.to_dict()
        
        if nav_response.get('success'):
            groups = nav_response.get('data', {}).get('navigation', [])
            print(f"   Navigation Groups: {len(groups)}")
            
            for group in groups:
                print(f"\n   📁 {group['name']}")
                for item in group.get('items', []):
                    print(f"      ✓ {item['title']} → {item['url']}")
        else:
            print(f"   ❌ Error: {nav_response.get('message')}")
    else:
        print("\n2. No rpo_admin user found")
except Exception as e:
    print(f"\n2. Error: {str(e)}")

print("\n" + "="*70)
print("  Next Steps:")
print("="*70)
print("  1. Start server: python manage.py runserver")
print("  2. Login as hiring_manager or rpo_admin")
print("  3. Visit: http://127.0.0.1:8000/employer-dashboard/")
print("  4. Check 'Quick Navigation' section for role-based items")
print("="*70 + "\n")
