"""
Check for duplicate entries in auth_group table and identify which are in use.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Jobstock.settings')
django.setup()

from django.contrib.auth.models import Group, User
from collections import defaultdict

print("=" * 70)
print("AUTH_GROUP DUPLICATE ANALYSIS")
print("=" * 70)

# Get all groups
all_groups = Group.objects.all().order_by('name', 'id')
print(f"\nTotal groups in database: {all_groups.count()}")

# Find duplicates by name
groups_by_name = defaultdict(list)
for group in all_groups:
    groups_by_name[group.name].append(group)

# Identify duplicates
duplicates = {name: groups for name, groups in groups_by_name.items() if len(groups) > 1}

if not duplicates:
    print("\n✅ No duplicate groups found!")
else:
    print(f"\n⚠️  Found {len(duplicates)} group name(s) with duplicates:\n")
    
    for group_name, group_list in duplicates.items():
        print(f"\n{'='*70}")
        print(f"GROUP NAME: '{group_name}' - {len(group_list)} duplicates")
        print(f"{'='*70}")
        
        for group in group_list:
            # Count users in this group
            user_count = group.user_set.count()
            users = list(group.user_set.values_list('username', flat=True))
            
            print(f"\n  ID: {group.id}")
            print(f"  Name: {group.name}")
            print(f"  Users assigned: {user_count}")
            if users:
                print(f"  Users: {', '.join(users)}")
            else:
                print(f"  Users: None (NOT IN USE)")
            print(f"  Permissions: {group.permissions.count()}")

# Summary of unused groups
print(f"\n{'='*70}")
print("SUMMARY - GROUPS NOT IN USE (CAN BE DELETED)")
print(f"{'='*70}")

unused_groups = []
for group_name, group_list in duplicates.items():
    for group in group_list:
        if group.user_set.count() == 0:
            unused_groups.append(group)
            print(f"  - ID {group.id}: '{group.name}' (0 users, {group.permissions.count()} permissions)")

if unused_groups:
    print(f"\n✅ Found {len(unused_groups)} duplicate group(s) that can be safely deleted")
    print(f"\nTo delete these, run: python delete_unused_auth_groups.py")
else:
    print(f"\n⚠️  All duplicate groups have users assigned. Manual review needed.")

print("\n" + "=" * 70)
