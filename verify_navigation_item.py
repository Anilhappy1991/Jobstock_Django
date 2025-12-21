"""
Verify Navigation Item in Database
Shows the Upload Resumes navigation item details
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Jobstock.settings')
django.setup()

from App.models import NavigationGroup, NavigationItem

def verify_navigation():
    print("=== Verifying Navigation Item ===\n")
    
    # Find the active item
    active_items = NavigationItem.objects.filter(is_active=True)
    
    print(f"Total Active Navigation Items: {active_items.count()}\n")
    
    for item in active_items:
        print("=" * 60)
        print(f"ID: {item.id}")
        print(f"Title: {item.title}")
        print(f"URL Name: {item.url_name}")
        print(f"URL (resolved): /rpo-resume-upload/")
        print(f"Full URL: http://127.0.0.1:8000/rpo-resume-upload/")
        print(f"Icon: {item.icon}")
        print(f"Order: {item.order}")
        print(f"Is Active: {item.is_active}")
        print(f"Badge Text: {item.badge_text}")
        print(f"Badge Class: {item.badge_class}")
        print(f"\nGroup Information:")
        print(f"  Group Name: {item.group.name}")
        print(f"  Group Slug: {item.group.slug}")
        print(f"  Visible to Roles: {item.group.visible_to_roles}")
        print(f"  Group Active: {item.group.is_active}")
        print(f"  Group Order: {item.group.order}")
        print("=" * 60)
    
    print("\n=== All Navigation Items (Active Status) ===\n")
    all_items = NavigationItem.objects.all().order_by('group__order', 'order')
    
    for item in all_items:
        status = "✅ ACTIVE" if item.is_active else "⚪ INACTIVE"
        print(f"{status} | {item.group.name:20} | {item.title:30} | {item.url_name}")

if __name__ == "__main__":
    verify_navigation()
