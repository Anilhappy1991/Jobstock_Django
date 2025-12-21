import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Jobstock.settings')
django.setup()

from django.contrib.auth.models import User, Group
from App.models import Profile

# Define correct role mappings
role_mappings = {
    'hiring_manager': 'hiring_manager',  # Currently has candidate role
    'rpo_admin': 'rpo_admin',  # Currently has candidate role
    'employer_test': 'hiring_manager',  # Currently has candidate role
}

def fix_user_roles():
    print("=== Fixing User Roles ===\n")
    
    for username, correct_role in role_mappings.items():
        try:
            user = User.objects.get(username=username)
            profile = user.profile
            
            # Get or create the correct group
            group, _ = Group.objects.get_or_create(name=correct_role)
            
            old_role = profile.role
            
            # Update profile role
            profile.role = correct_role
            profile.save()
            
            # Clear all groups and add correct group
            user.groups.clear()
            user.groups.add(group)
            
            print(f"✅ {username}:")
            print(f"   Role: {old_role} → {correct_role}")
            print(f"   Group: {correct_role}")
            print()
            
        except User.DoesNotExist:
            print(f"❌ User {username} not found")
            print()
        except Exception as e:
            print(f"❌ Error fixing {username}: {e}")
            print()
    
    print("\n=== Updated User Summary ===")
    for user in User.objects.all():
        try:
            profile = user.profile
            groups = list(user.groups.values_list('name', flat=True))
            print(f"{user.username:20} | Role: {profile.role:15} | Groups: {', '.join(groups)}")
        except:
            print(f"{user.username:20} | No profile")

if __name__ == '__main__':
    fix_user_roles()
