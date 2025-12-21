"""
Quick test to verify all users can authenticate
"""
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

print("=" * 60)
print("USER LOGIN CREDENTIALS - ALL PASSWORDS: H@ppy123")
print("=" * 60)

users = User.objects.all().order_by('username')

for user in users:
    # Test authentication
    auth_result = authenticate(username=user.username, password='H@ppy123')
    status = "✓ WORKS" if auth_result else "✗ FAILED"
    
    print(f"\nUsername: {user.username}")
    print(f"Password: H@ppy123")
    print(f"Status:   {status}")
    print(f"Active:   {user.is_active}")
    print(f"Staff:    {user.is_staff}")

print("\n" + "=" * 60)
print("Try logging in at: http://localhost:8000/")
print("=" * 60)
