from django.contrib.auth import authenticate
from django.contrib.auth.models import User

print("Testing authentication for all users...\n")

users_to_test = ['rituranjangupta', 'hiring_manager', 'rpo_admin', 'system_admin', 'test', 'employer_test']
password = 'H@ppy123'

for username in users_to_test:
    try:
        # Check if user exists
        user_obj = User.objects.get(username=username)
        print(f"User '{username}' exists:")
        print(f"  - is_active: {user_obj.is_active}")
        print(f"  - is_staff: {user_obj.is_staff}")
        
        # Try to authenticate
        auth_result = authenticate(username=username, password=password)
        if auth_result:
            print(f"  ✓ Authentication SUCCESSFUL")
        else:
            print(f"  ✗ Authentication FAILED")
    except User.DoesNotExist:
        print(f"User '{username}' does NOT exist")
    print()
