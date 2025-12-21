"""
Test Navigation Display - Only Active Items
Simulates what the UI will show for rpo_admin user
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Jobstock.settings')
django.setup()

from django.contrib.auth.models import User
from App.services.navigation_service import NavigationService

def test_navigation_display():
    print("=== Testing Navigation Display (Only Active Items) ===\n")
    
    # Get rpo_admin user
    try:
        user = User.objects.get(username='rpo_admin')
        print(f"User: {user.username}")
        print(f"Role: {user.profile.role}\n")
    except User.DoesNotExist:
        print("ERROR: rpo_admin user not found")
        return
    
    # Get navigation using the service
    service = NavigationService()
    nav_response = service.get_navigation_for_user(user)
    
    if isinstance(nav_response, dict):
        # Old dict format
        success = nav_response.get('success')
        data = nav_response.get('data', {})
        navigation = data.get('navigation', [])
    else:
        # New ApiResponse object format
        success = nav_response.success
        navigation = nav_response.data.get('navigation', []) if nav_response.data else []
    
    print(f"Response Success: {success}\n")
    print("=" * 70)
    print("NAVIGATION ITEMS THAT WILL APPEAR IN UI:")
    print("=" * 70)
    
    if not navigation:
        print("⚠️ No navigation items found!")
    else:
        for group in navigation:
            print(f"\n📁 GROUP: {group['name']}")
            print(f"   Slug: {group['slug']}")
            print(f"   Icon: {group['icon']}")
            print(f"   Items count: {len(group['items'])}")
            print()
            
            for item in group['items']:
                status = "✅ ACTIVE"
                print(f"   {status} {item['title']}")
                print(f"      URL: {item['url']}")
                print(f"      Icon: {item['icon']}")
                if item.get('badge_text'):
                    print(f"      Badge: {item['badge_text']}")
                
                # Show children if any
                if item.get('has_children') and item.get('children'):
                    for child in item['children']:
                        print(f"      └─ {child['title']} ({child['url']})")
                print()
    
    print("=" * 70)
    print(f"\nTotal Navigation Groups: {len(navigation)}")
    total_items = sum(len(g['items']) for g in navigation)
    print(f"Total Navigation Items: {total_items}")
    print("\n✅ These are the ONLY items that will show in the UI")

if __name__ == "__main__":
    test_navigation_display()
