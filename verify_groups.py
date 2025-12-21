"""
Verification script to check Groups and Roles setup
"""
from django.contrib.auth.models import Group, User
from App.models import GroupProfile

print("\n" + "="*60)
print("GROUPS AND ROLE IDENTIFIERS")
print("="*60)

for group_profile in GroupProfile.objects.select_related('group').all():
    group = group_profile.group
    user_count = group.user_set.count()
    print(f"\nGroup: {group.name}")
    print(f"  Role Identifier: {group_profile.role_identifier}")
    print(f"  Users: {user_count}")
    
    # Show users in this group
    if user_count > 0:
        for user in group.user_set.all():
            try:
                role = user.profile.role
            except:
                role = 'N/A (no profile)'
            print(f"    - {user.username} (role: {role})")

print("\n" + "="*60)
print("USERS AND THEIR GROUPS")
print("="*60)

for user in User.objects.all():
    try:
        role = user.profile.role
    except:
        role = 'N/A (no profile)'
    
    groups = user.groups.all()
    
    print(f"\nUser: {user.username}")
    print(f"  Profile Role: {role}")
    print(f"  Groups: {', '.join([g.name for g in groups]) if groups else 'None'}")

print("\n" + "="*60)
print("SUMMARY")
print("="*60)
print(f"Total Groups: {Group.objects.count()}")
print(f"Total GroupProfiles: {GroupProfile.objects.count()}")
print(f"Total Users: {User.objects.count()}")
print(f"Users with Profiles: {User.objects.filter(profile__isnull=False).count()}")
print(f"Users in Groups: {User.objects.filter(groups__isnull=False).distinct().count()}")
print("="*60 + "\n")
