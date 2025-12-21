"""Show complete navigation menu"""
import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Jobstock.settings')
django.setup()

from django.contrib.auth import get_user_model
from App.services.navigation_service import NavigationService

User = get_user_model()

user = User.objects.filter(username='rituranjangupta').first()
service = NavigationService()
result = service.get_navigation_for_user(user)

if result.get('success'):
    navigation = result.get('data', {}).get('navigation', [])
    
    print("=== COMPLETE NAVIGATION MENU ===\n")
    
    for group in navigation:
        print(f"📁 {group.get('name')}")
        print("=" * 60)
        
        for item in group.get('items', []):
            icon = item.get('icon', '')
            title = item.get('title', '')
            url = item.get('url', '#')
            has_children = item.get('has_children', False)
            
            if has_children:
                print(f"  📂 {title}")
                print(f"     URL: {url}")
                
                # Show children
                children = item.get('children', [])
                for child in children:
                    child_title = child.get('title', '')
                    child_url = child.get('url', '#')
                    status = "✅" if child_url != '#' else "❌"
                    print(f"     └─ {status} {child_title} → {child_url}")
            else:
                status = "✅" if url != '#' else "❌"
                print(f"  {status} {title} → {url}")
        
        print()
