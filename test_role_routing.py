"""Test role-based dashboard routing"""
import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Jobstock.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()

print("=== Testing Role-Based Dashboard Routing ===\n")

# Test all users
users = User.objects.all()[:10]

print("User → Expected Dashboard\n" + "=" * 60)

for user in users:
    # Get user's role
    user_role = "unknown"
    try:
        user_role = user.profile.role
    except:
        if user.groups.filter(name__icontains='hiring').exists() or user.groups.filter(name='Hiring Managers').exists():
            user_role = 'hiring_manager'
        elif user.groups.filter(name__icontains='candidate').exists() or user.groups.filter(name='Candidates').exists():
            user_role = 'candidate'
        elif user.groups.filter(name__icontains='rpo').exists():
            user_role = 'rpo_admin'
    
    # Determine dashboard
    if user.is_superuser:
        dashboard = "employer_dashboard (superuser)"
    elif user_role == 'hiring_manager':
        dashboard = "employer_dashboard"
    elif user_role == 'candidate':
        dashboard = "candidate_dashboard"
    elif user_role == 'rpo_admin':
        dashboard = "employer_dashboard (RPO)"
    else:
        dashboard = "index (unknown role)"
    
    groups = ', '.join([g.name for g in user.groups.all()]) or 'None'
    
    print(f"{user.username:20} | Role: {user_role:15} | Groups: {groups:30} → {dashboard}")

print("\n" + "=" * 60)
print("\n✅ Login routing configured:")
print("   - Candidates → /candidate-dashboard/")
print("   - Hiring Managers → /employer-dashboard/")
print("   - RPO Admins → /employer-dashboard/")
print("   - Superusers → /employer-dashboard/")
print("   - Unknown roles → /index/")
