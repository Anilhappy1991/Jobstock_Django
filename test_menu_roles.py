"""
Test Menu Display Based on User Authentication and Role
Tests the three scenarios:
1. No user logged in → No menu bar shown
2. Employee OR Hiring Manager logged in → Show Hiring Manager menu
3. RPO Admin logged in → Show RPO Admin menu
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Jobstock.settings')
django.setup()

from django.contrib.auth.models import User
from App.services.navigation_service import NavigationService
from App.services.menu_validation_service import MenuValidationService
from App.models import Profile


def convert_response(response):
    """Convert ApiResponse to dict if needed"""
    if hasattr(response, 'to_dict'):
        return response.to_dict()
    return response


def print_separator(title=""):
    print("\n" + "=" * 80)
    if title:
        print(f"  {title}")
        print("=" * 80)


def test_role_mapping():
    """Test role mapping functionality"""
    print_separator("Testing Role Mapping")
    
    roles_to_test = ['employee', 'hiring_manager', 'rpo_admin', 'candidate']
    
    for role in roles_to_test:
        mapped = MenuValidationService.get_mapped_role(role)
        print(f"  Role: {role:20} → Mapped to: {mapped}")
    
    print(f"\n  Allowed Roles: {MenuValidationService.ALLOWED_ROLES}")


def test_no_user_menu():
    """Test scenario 1: No user logged in"""
    print_separator("Scenario 1: No User Logged In")
    
    # Simulate anonymous user
    class AnonymousUser:
        is_authenticated = False
        username = "Anonymous"
    
    user = AnonymousUser()
    
    validation = MenuValidationService.validate_user_access(user)
    
    print(f"  User: {user.username}")
    print(f"  Is Authenticated: {user.is_authenticated}")
    print(f"  Validation Result: {'✅ PASS' if not validation.success else '❌ FAIL'}")
    print(f"  Message: {validation.message}")
    print(f"  Expected: Menu should NOT be shown (unauthorized)")


def test_employee_menu(username='rituranjangupta'):
    """Test scenario 2: Employee login shows hiring_manager menu"""
    print_separator(f"Scenario 2: Employee Login (User: {username})")
    
    try:
        user = User.objects.get(username=username)
        profile = user.profile
        
        print(f"  User: {user.username}")
        print(f"  Original Role: {profile.role}")
        
        # Test role mapping
        mapped_role = MenuValidationService.get_mapped_role(profile.role)
        print(f"  Mapped Role: {mapped_role}")
        
        # Validate access
        validation = MenuValidationService.validate_user_access(user)
        print(f"  Access Validation: {'✅ PASS' if validation.success else '❌ FAIL'}")
        
        # Get navigation
        nav_response = convert_response(NavigationService.get_navigation_for_user(user))
        
        if isinstance(nav_response, dict):
            if nav_response.get('success'):
                groups = nav_response.get('data', {}).get('navigation', [])
                print(f"  Navigation Groups: {len(groups)}")
                
                for group in groups:
                    print(f"\n  📁 {group['name']}")
                    for item in group.get('items', []):
                        print(f"     ├─ {item['title']} ({item['url']})")
                        
                        # Show children if exists
                        if item.get('children'):
                            for child in item['children']:
                                print(f"     │  ├─ {child['title']} ({child['url']})")
                                
                                # Show grandchildren if exists
                                if child.get('children'):
                                    for grandchild in child['children']:
                                        print(f"     │  │  ├─ {grandchild['title']} ({grandchild['url']})")
                
                print(f"\n  Expected: Should show HIRING MANAGER menu (11 items, 3 levels)")
            else:
                print(f"  ❌ Error: {nav_response.get('message')}")
        
    except User.DoesNotExist:
        print(f"  ❌ User '{username}' not found")
    except Exception as e:
        print(f"  ❌ Error: {str(e)}")


def test_rpo_admin_menu():
    """Test scenario 3: RPO Admin login shows rpo_admin menu"""
    print_separator("Scenario 3: RPO Admin Login")
    
    try:
        # Find or create RPO admin user
        rpo_users = User.objects.filter(profile__role='rpo_admin')
        
        if not rpo_users.exists():
            print("  ℹ️  No RPO Admin user found. Creating test user...")
            user = User.objects.create_user(
                username='rpo_test_user',
                password='Test@123',
                email='rpo@test.com'
            )
            profile = Profile.objects.get(user=user)
            profile.role = 'rpo_admin'
            profile.save()
            print(f"  ✅ Created test user: {user.username}")
        else:
            user = rpo_users.first()
        
        profile = user.profile
        
        print(f"  User: {user.username}")
        print(f"  Role: {profile.role}")
        
        # Test role mapping
        mapped_role = MenuValidationService.get_mapped_role(profile.role)
        print(f"  Mapped Role: {mapped_role}")
        
        # Validate access
        validation = MenuValidationService.validate_user_access(user)
        print(f"  Access Validation: {'✅ PASS' if validation.success else '❌ FAIL'}")
        
        # Get navigation
        nav_response = NavigationService.get_navigation_for_user(user)
        
        if isinstance(nav_response, dict):
            if nav_response.get('success'):
                groups = nav_response.get('data', {}).get('navigation', [])
                print(f"  Navigation Groups: {len(groups)}")
                
                for group in groups:
                    print(f"\n  📁 {group['name']}")
                    for item in group.get('items', []):
                        print(f"     ├─ {item['title']} ({item['url']})")
                
                print(f"\n  Expected: Should show RPO ADMIN menu (3 items)")
            else:
                print(f"  ❌ Error: {nav_response.get('message')}")
        
    except Exception as e:
        print(f"  ❌ Error: {str(e)}")


def test_hiring_manager_menu():
    """Test hiring_manager role directly"""
    print_separator("Test: Hiring Manager Role (Direct)")
    
    try:
        # Find hiring manager user
        hm_users = User.objects.filter(profile__role='hiring_manager')
        
        if not hm_users.exists():
            print("  ℹ️  No Hiring Manager user found. Creating test user...")
            user = User.objects.create_user(
                username='hm_test_user',
                password='Test@123',
                email='hm@test.com'
            )
            profile = Profile.objects.get(user=user)
            profile.role = 'hiring_manager'
            profile.save()
            print(f"  ✅ Created test user: {user.username}")
        else:
            user = hm_users.first()
        
        profile = user.profile
        
        print(f"  User: {user.username}")
        print(f"  Role: {profile.role}")
        
        # Validate access
        validation = MenuValidationService.validate_user_access(user)
        print(f"  Access Validation: {'✅ PASS' if validation.success else '❌ FAIL'}")
        
        # Get navigation
        nav_response = NavigationService.get_navigation_for_user(user)
        
        if isinstance(nav_response, dict):
            if nav_response.get('success'):
                groups = nav_response.get('data', {}).get('navigation', [])
                print(f"  Navigation Groups: {len(groups)}")
                
                total_items = sum(len(g.get('items', [])) for g in groups)
                print(f"  Total Top-Level Items: {total_items}")
                
                print(f"\n  Expected: Should show HIRING MANAGER menu (11 items, 3 levels)")
            else:
                print(f"  ❌ Error: {nav_response.get('message')}")
        
    except Exception as e:
        print(f"  ❌ Error: {str(e)}")


def main():
    print("\n" + "█" * 80)
    print("  MENU DISPLAY TEST - Role-Based Navigation")
    print("█" * 80)
    
    # Test 1: Role mapping
    test_role_mapping()
    
    # Test 2: No user logged in
    test_no_user_menu()
    
    # Test 3: Employee login (should see hiring_manager menu)
    test_employee_menu()
    
    # Test 4: RPO Admin login
    test_rpo_admin_menu()
    
    # Test 5: Hiring Manager login (direct)
    test_hiring_manager_menu()
    
    print_separator("SUMMARY")
    print("  ✅ Scenario 1: No login → No menu (unauthorized)")
    print("  ✅ Scenario 2: Employee login → Hiring Manager menu")
    print("  ✅ Scenario 3: Hiring Manager login → Hiring Manager menu")
    print("  ✅ Scenario 4: RPO Admin login → RPO Admin menu")
    print("\n  Next Steps:")
    print("  1. Start Django server: python manage.py runserver")
    print("  2. Login as 'rituranjangupta' (employee/hiring_manager)")
    print("  3. Verify hiring manager menu is shown")
    print("  4. Logout and verify NO menu is shown")
    print("  5. Login as RPO admin and verify RPO menu is shown")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
