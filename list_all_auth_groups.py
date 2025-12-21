"""
List all auth_group entries and identify which ones are unused.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Jobstock.settings')
django.setup()

from django.contrib.auth.models import Group

print("=" * 70)
print("ALL AUTH_GROUP ENTRIES")
print("=" * 70)

all_groups = Group.objects.all().order_by('id')
print(f"\nTotal groups: {all_groups.count()}\n")

unused_groups = []
used_groups = []

for group in all_groups:
    user_count = group.user_set.count()
    perm_count = group.permissions.count()
    users = list(group.user_set.values_list('username', flat=True)[:5])  # First 5 users
    
    status = "✓ IN USE" if user_count > 0 else "✗ UNUSED"
    
    print(f"\nID: {group.id} - {group.name}")
    print(f"  Status: {status}")
    print(f"  Users: {user_count}")
    if users:
        user_list = ', '.join(users)
        if user_count > 5:
            user_list += f" ... (+{user_count - 5} more)"
        print(f"  Users list: {user_list}")
    print(f"  Permissions: {perm_count}")
    
    if user_count == 0:
        unused_groups.append(group)
    else:
        used_groups.append(group)

print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)
print(f"Groups in use: {len(used_groups)}")
print(f"Unused groups: {len(unused_groups)}")

if unused_groups:
    print(f"\n{'='*70}")
    print("UNUSED GROUPS (CAN BE DELETED)")
    print(f"{'='*70}")
    for group in unused_groups:
        print(f"  - ID {group.id}: '{group.name}' ({group.permissions.count()} permissions)")
    print(f"\nTo delete these unused groups, run: python delete_unused_auth_groups.py")
else:
    print("\n✅ All groups are in use. No cleanup needed.")

print("=" * 70)
