"""
Delete unused groups from auth_group table.
This script will delete groups that have NO users assigned.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Jobstock.settings')
django.setup()

from django.contrib.auth.models import Group

print("=" * 70)
print("DELETE UNUSED AUTH_GROUP ENTRIES")
print("=" * 70)

# Find all groups with no users
unused_groups = []
for group in Group.objects.all():
    if group.user_set.count() == 0:
        unused_groups.append(group)

if not unused_groups:
    print("\n✅ No unused groups found. Nothing to delete.")
    print("=" * 70)
    exit(0)

print(f"\nFound {len(unused_groups)} unused group(s):\n")
for group in unused_groups:
    print(f"  ID {group.id}: '{group.name}' - {group.permissions.count()} permissions")

print("\n" + "=" * 70)
print("DELETING UNUSED GROUPS...")
print("=" * 70)

deleted_count = 0
for group in unused_groups:
    group_id = group.id
    group_name = group.name
    perm_count = group.permissions.count()
    
    try:
        group.delete()
        print(f"✅ Deleted: ID {group_id} - '{group_name}' ({perm_count} permissions)")
        deleted_count += 1
    except Exception as e:
        print(f"❌ Failed to delete ID {group_id} - '{group_name}': {e}")

print("\n" + "=" * 70)
print("CLEANUP COMPLETE")
print("=" * 70)
print(f"Successfully deleted: {deleted_count} group(s)")
print(f"Failed: {len(unused_groups) - deleted_count}")

# Show remaining groups
remaining = Group.objects.all().count()
print(f"\nRemaining groups in database: {remaining}")

print("\n" + "=" * 70)
print("REMAINING GROUPS:")
print("=" * 70)
for group in Group.objects.all().order_by('id'):
    user_count = group.user_set.count()
    print(f"  ID {group.id}: '{group.name}' - {user_count} user(s)")

print("=" * 70)
