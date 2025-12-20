"""
Quick script to check existing users in the database
Usage: python check_users.py
"""
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Jobstock.settings')
django.setup()

from django.contrib.auth.models import User

print("\n" + "="*60)
print("USER DATABASE CHECK".center(60))
print("="*60 + "\n")

users = User.objects.all()

if not users:
    print("❌ NO USERS FOUND IN DATABASE")
    print("\nTo create a test user, run:")
    print("   python manage.py create_test_user")
else:
    print(f"✅ Found {users.count()} user(s) in database:\n")
    
    for user in users:
        print(f"{'─'*60}")
        print(f"  ID: {user.id}")
        print(f"  Username: {user.username}")
        print(f"  Email: {user.email or '(not set)'}")
        print(f"  Active: {'✅ Yes' if user.is_active else '❌ No'}")
        print(f"  Staff: {'✅ Yes' if user.is_staff else '❌ No'}")
        print(f"  Superuser: {'✅ Yes' if user.is_superuser else '❌ No'}")
        print(f"  Last Login: {user.last_login or '(never)'}")
        print(f"  Date Joined: {user.date_joined}")
        
        # Try to authenticate with a test password
        if user.username == 'testuser':
            from django.contrib.auth import authenticate
            test_auth = authenticate(username='testuser', password='testpass123')
            if test_auth:
                print(f"  Test Auth: ✅ Password 'testpass123' works!")
            else:
                print(f"  Test Auth: ❌ Password 'testpass123' doesn't work")

print(f"\n{'─'*60}\n")
print("💡 Quick Tips:")
print("   • Create user: python manage.py create_test_user")
print("   • Test login: http://127.0.0.1:8000/login-debug/")
print("   • Create superuser: python manage.py createsuperuser")
print("\n" + "="*60 + "\n")
