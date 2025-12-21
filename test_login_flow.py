"""
Test login flow manually
Run with: python manage.py shell < test_login_flow.py
"""
import django
import os

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Jobstock.settings')
django.setup()

from django.contrib.auth import authenticate
from django.contrib.auth.models import User

print("="*60)
print("TESTING LOGIN FLOW")
print("="*60)

# Test users
test_credentials = [
    ('rituranjangupta', 'H@ppy123'),
    ('test', 'H@ppy123'),
    ('hiring_manager', 'H@ppy123'),
]

for username, password in test_credentials:
    print(f"\nTesting: {username}")
    
    # Check if user exists
    try:
        user_obj = User.objects.get(username=username)
        print(f"  ✓ User exists")
        print(f"  - is_active: {user_obj.is_active}")
        print(f"  - is_staff: {user_obj.is_staff}")
        print(f"  - email: {user_obj.email}")
        
        # Test authentication
        auth_user = authenticate(username=username, password=password)
        if auth_user:
            print(f"  ✓ Authentication SUCCESSFUL")
        else:
            print(f"  ✗ Authentication FAILED")
            
            # Check password hash
            from django.contrib.auth.hashers import check_password
            if check_password(password, user_obj.password):
                print(f"  ! Password hash is correct but authenticate() failed")
            else:
                print(f"  ! Password hash is INCORRECT")
                
    except User.DoesNotExist:
        print(f"  ✗ User does NOT exist")
        
print("\n" + "="*60)
print("If authentication is successful here but login fails in browser,")
print("the issue is likely with:")
print("  1. CSRF token")
print("  2. Session middleware")
print("  3. Form submission")
print("  4. JavaScript interference")
print("="*60)
