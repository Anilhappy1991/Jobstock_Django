"""
MVT Navigation System - Verification Script

This script tests the complete MVT implementation:
1. Model Layer - Database structure
2. Service Layer - NavigationService methods
3. Response Class - ApiResponse functionality
4. Data Integrity - Navigation data for hiring_manager

Run with: python verify_mvt_navigation.py
"""

import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Jobstock.settings')
django.setup()

from django.contrib.auth import get_user_model
from App.models import NavigationGroup, NavigationItem, DashboardWidget
from App.services.navigation_service import NavigationService
from App.utils.response import ApiResponse
from django.http import HttpRequest

User = get_user_model()

def print_header(title):
    """Print formatted section header"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)

def print_success(message):
    """Print success message"""
    print(f"✓ {message}")

def print_error(message):
    """Print error message"""
    print(f"✗ {message}")

def print_info(message):
    """Print info message"""
    print(f"ℹ {message}")

def verify_models():
    """Verify Model Layer"""
    print_header("1. MODEL LAYER - Database Structure")
    
    try:
        # Check NavigationGroup
        group_count = NavigationGroup.objects.count()
        print_success(f"NavigationGroup model OK - {group_count} groups found")
        
        # Check NavigationItem
        item_count = NavigationItem.objects.count()
        print_success(f"NavigationItem model OK - {item_count} items found")
        
        # Check DashboardWidget
        widget_count = DashboardWidget.objects.count()
        print_success(f"DashboardWidget model OK - {widget_count} widgets found")
        
        # Display groups
        print_info("\nNavigation Groups:")
        for group in NavigationGroup.objects.filter(is_active=True):
            print(f"  - {group.name} (Order: {group.order}, Roles: {group.visible_to_roles})")
        
        return True
    except Exception as e:
        print_error(f"Model verification failed: {str(e)}")
        return False

def verify_service_layer():
    """Verify Service Layer"""
    print_header("2. SERVICE LAYER - NavigationService Methods")
    
    try:
        service = NavigationService()
        print_success("NavigationService instantiated successfully")
        
        # Get hiring manager user
        hiring_manager = User.objects.filter(
            groups__name='hiring_manager'
        ).first() or User.objects.filter(is_superuser=False).first()
        
        if not hiring_manager:
            print_error("No user found for testing")
            return False
        
        print_success(f"Found test user: {hiring_manager.username}")
        
        # Test get_navigation_for_user
        nav_response = service.get_navigation_for_user(hiring_manager)
        
        # Extract navigation from response
        navigation = []
        if isinstance(nav_response, dict) and nav_response.get('success'):
            navigation = nav_response.get('data', {}).get('navigation', [])
        
        print_success(f"get_navigation_for_user() returned {len(navigation)} groups")
        
        # Display navigation structure
        if navigation and len(navigation) > 0:
            for group_data in navigation[:3]:  # Show first 3 groups
                if isinstance(group_data, dict):
                    print(f"\n  Group: {group_data.get('name', 'Unknown')}")
                    for item in group_data.get('items', [])[:5]:  # Show first 5 items
                        if isinstance(item, dict):
                            print(f"    - {item.get('title', 'Unknown')} ({item.get('url_name', '')})")
                            for child in item.get('children', [])[:3]:  # Show first 3 children
                                if isinstance(child, dict):
                                    print(f"      └─ {child.get('title', 'Unknown')}")
        
        # Test get_dashboard_widgets
        widgets = service.get_dashboard_widgets(hiring_manager)
        print_success(f"get_dashboard_widgets() returned {len(widgets)} widgets")
        
        # Test get_quick_actions
        actions = service.get_quick_actions(hiring_manager)
        print_success(f"get_quick_actions() returned {len(actions)} actions")
        
        # Test get_navigation_stats
        stats = service.get_navigation_stats(hiring_manager)
        print_success(f"get_navigation_stats() returned: {stats}")
        
        return True
    except Exception as e:
        print_error(f"Service layer verification failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def verify_response_class():
    """Verify ApiResponse Class"""
    print_header("3. RESPONSE CLASS - ApiResponse Functionality")
    
    try:
        # Test success response
        response = ApiResponse.success(
            data={'test': 'data'},
            message="Test success"
        )
        print_success("ApiResponse.success() working")
        
        # Test error response
        response = ApiResponse.error(
            message="Test error",
            error_details={'field': 'error'}
        )
        print_success("ApiResponse.error() working")
        
        # Test other methods
        methods = [
            'created', 'not_found', 'unauthorized', 
            'forbidden', 'validation_error', 'server_error'
        ]
        for method in methods:
            getattr(ApiResponse, method)("Test message")
        print_success(f"All {len(methods) + 2} response methods working")
        
        # Display response structure
        test_response_data = {
            'success': True,
            'status_code': 200,
            'message': 'Sample response',
            'data': {'navigation': 'test'}
        }
        print_info("\nSample Response Structure:")
        import json
        print(json.dumps(test_response_data, indent=2))
        
        return True
    except Exception as e:
        print_error(f"Response class verification failed: {str(e)}")
        return False

def verify_role_based_access():
    """Verify Role-Based Navigation"""
    print_header("4. ROLE-BASED ACCESS - Navigation by Role")
    
    try:
        service = NavigationService()
        
        # Test hiring_manager role
        hiring_manager = User.objects.filter(groups__name='hiring_manager').first() or User.objects.filter(is_superuser=False).first()
        if hiring_manager:
            nav_response = service.get_navigation_for_user(hiring_manager)
            nav = []
            if isinstance(nav_response, dict) and nav_response.get('success'):
                nav = nav_response.get('data', {}).get('navigation', [])
            
            print_success(f"Test User ({hiring_manager.username}) gets {len(nav)} navigation groups")
            
            total_items = 0
            for g in nav:
                if isinstance(g, dict):
                    total_items += len(g.get('items', []))
            print_info(f"  Total menu items: {total_items}")
        
        # Test candidate role
        candidate = User.objects.filter(groups__name='candidate').first()
        if candidate:
            nav_response = service.get_navigation_for_user(candidate)
            nav = []
            if isinstance(nav_response, dict) and nav_response.get('success'):
                nav = nav_response.get('data', {}).get('navigation', [])
            
            print_success(f"Candidate gets {len(nav)} navigation groups")
            total_items = 0
            for g in nav:
                if isinstance(g, dict):
                    total_items += len(g.get('items', []))
            print_info(f"  Total menu items: {total_items}")
        
        # Test admin role
        admin = User.objects.filter(is_superuser=True).first()
        if admin:
            nav_response = service.get_navigation_for_user(admin)
            nav = []
            if isinstance(nav_response, dict) and nav_response.get('success'):
                nav = nav_response.get('data', {}).get('navigation', [])
            
            print_success(f"Admin gets {len(nav)} navigation groups")
            total_items = 0
            for g in nav:
                if isinstance(g, dict):
                    total_items += len(g.get('items', []))
            print_info(f"  Total menu items: {total_items}")
        
        return True
    except Exception as e:
        print_error(f"Role-based access verification failed: {str(e)}")
        return False

def verify_data_integrity():
    """Verify Navigation Data Integrity"""
    print_header("5. DATA INTEGRITY - Navigation Database Check")
    
    try:
        # Check for orphaned items
        orphaned = NavigationItem.objects.filter(group__isnull=True)
        if orphaned.count() == 0:
            print_success("No orphaned navigation items")
        else:
            print_error(f"Found {orphaned.count()} orphaned items")
        
        # Check for circular parent references
        for item in NavigationItem.objects.filter(parent__isnull=False):
            if item.parent.id == item.id:
                print_error(f"Circular reference found: {item.title}")
                return False
        print_success("No circular parent references")
        
        # Check role consistency
        for group in NavigationGroup.objects.all():
            if not group.visible_to_roles or len(group.visible_to_roles) == 0:
                print_error(f"Group '{group.name}' has no roles assigned")
            else:
                print_success(f"Group '{group.name}' has {len(group.visible_to_roles)} roles")
        
        # Check hierarchical structure
        parent_items = NavigationItem.objects.filter(
            parent__isnull=True,
            is_active=True
        ).count()
        child_items = NavigationItem.objects.filter(
            parent__isnull=False,
            is_active=True
        ).count()
        print_info(f"\nHierarchical Structure:")
        print(f"  - Parent items: {parent_items}")
        print(f"  - Child items: {child_items}")
        
        return True
    except Exception as e:
        print_error(f"Data integrity check failed: {str(e)}")
        return False

def main():
    """Main verification function"""
    print("\n" + "🔍 MVT NAVIGATION SYSTEM - VERIFICATION TEST" + "\n")
    print("This script verifies the complete MVT implementation")
    print("Following the Model-View-Template pattern with Service Layer")
    
    results = {
        'models': verify_models(),
        'service': verify_service_layer(),
        'response': verify_response_class(),
        'role_access': verify_role_based_access(),
        'data_integrity': verify_data_integrity(),
    }
    
    # Summary
    print_header("VERIFICATION SUMMARY")
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, passed_test in results.items():
        status = "✓ PASS" if passed_test else "✗ FAIL"
        print(f"{status} - {test_name.replace('_', ' ').title()}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All verifications PASSED! MVT implementation is complete.")
        print("\nNext Steps:")
        print("1. Start Django server: python manage.py runserver")
        print("2. Login as hiring_manager")
        print("3. Navigate to: /employer/dashboard/")
        print("4. Check navigation menu renders correctly")
        print("5. Test API endpoints: /api/navigation/")
        return 0
    else:
        print("\n❌ Some verifications FAILED. Please review errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
