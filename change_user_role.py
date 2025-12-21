"""Change user role to hiring_manager"""
import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Jobstock.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()

print("=== Changing User Role ===\n")

# Get user
user = User.objects.filter(username='rituranjangupta').first()
if not user:
    print("❌ User not found!")
    sys.exit(1)

print(f"Current user: {user.username}")
print(f"Current groups: {', '.join([g.name for g in user.groups.all()])}")

# Update profile role
try:
    user.profile.role = 'hiring_manager'
    user.profile.save()
    print(f"✓ Updated profile role to: hiring_manager")
except Exception as e:
    print(f"Profile update: {e}")

# Remove from Candidates group, add to hiring_manager group
candidate_group = Group.objects.filter(name='Candidates').first()
if candidate_group:
    user.groups.remove(candidate_group)
    print(f"✓ Removed from 'Candidates' group")

hiring_manager_group, created = Group.objects.get_or_create(name='hiring_manager')
user.groups.add(hiring_manager_group)
print(f"✓ Added to 'hiring_manager' group")

user.save()

print(f"\n=== Update Complete ===")
print(f"User: {user.username}")
print(f"Groups: {', '.join([g.name for g in user.groups.all()])}")
print(f"Profile Role: {user.profile.role}")
print(f"\nUser can now see hiring_manager navigation!")
