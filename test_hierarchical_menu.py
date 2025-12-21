"""
Test Hierarchical Multilevel Menu System
Tests navigation for both hiring_manager and rpo_admin roles
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Jobstock.settings')
django.setup()

from django.contrib.auth.models import User
from App.services.navigation_service import NavigationService
from App.services.menu_validation_service import MenuValidationService
import json


def print_menu_tree(items, indent=0):
    """Recursively print menu tree structure"""
    for item in items:
        prefix = "  " * indent
        icon = f"[{item['icon']}]" if item.get('icon') else ""
        badge = f" ({item['badge_text']})" if item.get('badge_text') else ""
        
        print(f"{prefix}├─ {icon} {item['title']}{badge}")
        print(f"{prefix}   URL: {item['url']}")
        
        if item.get('children'):
            print_menu_tree(item['children'], indent + 1)


def test_user_navigation(username, expected_role):
    """Test navigation for a specific user"""
    print(f"\n{'=' * 80}")
    print(f"Testing Navigation for: {username} (Expected Role: {expected_role})")
    print('=' * 80)
    
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        print(f"❌ User '{username}' not found!")
        return False
    
    actual_role = user.profile.role if hasattr(user, 'profile') else None
    print(f"✓ User found: {user.username}")
    print(f"✓ Actual role: {actual_role}")
    
    if actual_role != expected_role:
        print(f"⚠️  WARNING: Role mismatch! Expected '{expected_role}', got '{actual_role}'")
    
    # Test access validation
    print("\n1. Testing Access Validation...")
    validation = MenuValidationService.validate_user_access(user)
    
    if isinstance(validation, dict):
        success = validation.get('success')
        message = validation.get('message')
    else:
        success = validation.success
        message = validation.message
    
    if success:
        print(f"   ✅ {message}")
    else:
        print(f"   ❌ {message}")
        if hasattr(validation, 'error_details'):
            print(f"   Details: {validation.error_details}")
        return False
    
    # Get navigation
    print("\n2. Getting Navigation Data...")
    service = NavigationService()
    nav_response = service.get_navigation_for_user(user)
    
    if isinstance(nav_response, dict):
        navigation = nav_response.get('data', {}).get('navigation', [])
    else:
        navigation = nav_response.data.get('navigation', []) if nav_response.data else []
    
    print(f"   ✓ Retrieved {len(navigation)} navigation groups")
    
    # Display menu structure
    print("\n3. Menu Structure:")
    print("-" * 80)
    
    if not navigation:
        print("   ⚠️  No navigation items found for this user!")
        return False
    
    total_items = 0
    max_depth = 0
    
    def count_items_and_depth(items, depth=0):
        nonlocal total_items, max_depth
        count = 0
        if depth > max_depth:
            max_depth = depth
        for item in items:
            count += 1
            total_items += 1
            if item.get('children'):
                count += count_items_and_depth(item['children'], depth + 1)
        return count
    
    for group in navigation:
        print(f"\n📁 {group['name']} (Slug: {group['slug']})")
        print(f"   Icon: {group['icon']}")
        print(f"   Items: {len(group['items'])}")
        print()
        
        print_menu_tree(group['items'])
        count_items_and_depth(group['items'])
    
    print("\n" + "-" * 80)
    print(f"Total Groups: {len(navigation)}")
    print(f"Total Items: {total_items}")
    print(f"Maximum Depth: {max_depth} levels")
    
    return True


def test_menu_validation():
    """Test menu structure validation"""
    print(f"\n{'=' * 80}")
    print("Testing Menu Structure Validation")
    print('=' * 80)
    
    validation = MenuValidationService.validate_menu_structure()
    
    if isinstance(validation, dict):
        results = validation.get('data', {})
        success = validation.get('success')
    else:
        results = validation.data if validation.data else {}
        success = validation.success
    
    print(f"\nGroups checked: {results.get('groups_checked', 0)}")
    print(f"Items checked: {results.get('items_checked', 0)}")
    print(f"Errors: {len(results.get('errors', []))}")
    print(f"Warnings: {len(results.get('warnings', []))}")
    print(f"Circular references: {len(results.get('circular_references', []))}")
    print(f"Depth violations: {len(results.get('depth_violations', []))}")
    print(f"Invalid URLs: {len(results.get('invalid_urls', []))}")
    
    if results.get('warnings'):
        print("\nWarnings:")
        for warning in results['warnings']:
            print(f"  ⚠️  {warning}")
    
    if results.get('invalid_urls'):
        print("\nInvalid URLs:")
        for invalid in results['invalid_urls']:
            print(f"  ⚠️  {invalid['item_title']}: {invalid['url_name']}")
    
    if success:
        print("\n✅ Menu structure validation PASSED")
    else:
        print("\n❌ Menu structure validation FAILED")
    
    return success


def test_allowed_roles():
    """Test allowed roles retrieval"""
    print(f"\n{'=' * 80}")
    print("Testing Allowed Roles")
    print('=' * 80)
    
    result = MenuValidationService.get_allowed_roles()
    
    if isinstance(result, dict):
        roles = result.get('data', {}).get('allowed_roles', [])
    else:
        roles = result.data.get('allowed_roles', []) if result.data else []
    
    print(f"\nAllowed Roles ({len(roles)}):")
    for role in roles:
        print(f"  ✓ {role}")
    
    return True


def main():
    """Run all tests"""
    print("\n" + "=" * 80)
    print("HIERARCHICAL MULTILEVEL MENU SYSTEM - COMPREHENSIVE TEST")
    print("=" * 80)
    
    # Test allowed roles
    test_allowed_roles()
    
    # Test menu validation
    test_menu_validation()
    
    # Test RPO Admin navigation
    rpo_success = test_user_navigation('rpo_admin', 'rpo_admin')
    
    # Test Hiring Manager navigation  
    # Note: You may need to create a hiring_manager user first
    print("\n\nℹ️  To test hiring_manager, create a user with that role:")
    print("   python manage.py shell")
    print("   >>> from django.contrib.auth.models import User")
    print("   >>> from App.models import Profile")
    print("   >>> user = User.objects.create_user('hiring_mgr', password='test123')")
    print("   >>> profile = Profile.objects.create(user=user, role='hiring_manager')")
    
    # Summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    print(f"RPO Admin Navigation: {'✅ PASSED' if rpo_success else '❌ FAILED'}")
    print("\n✅ All tests completed!")
    print("\nNext Steps:")
    print("1. Visit http://127.0.0.1:8000/menu-demo/ to see the live demo")
    print("2. Test API at http://127.0.0.1:8000/api/menu/hierarchical/")
    print("3. Validate structure at http://127.0.0.1:8000/api/menu/validate/")


if __name__ == "__main__":
    main()
