"""
Check details of Post New Job duplicates
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Jobstock.settings')
django.setup()

from App.models import NavigationItem

print("\n" + "="*70)
print("  Analyzing 'Post New Job' Items")
print("="*70)

post_job_items = NavigationItem.objects.filter(
    title__icontains='Post New Job',
    is_active=True
)

print(f"\nFound {post_job_items.count()} 'Post New Job' items:\n")

for item in post_job_items:
    print(f"ID: {item.id}")
    print(f"  Title: {item.title}")
    print(f"  URL Name: {item.url_name}")
    print(f"  Group: {item.group.name if item.group else 'None'} (ID: {item.group_id})")
    print(f"  Parent: {item.parent.title if item.parent else 'None'} (ID: {item.parent_id})")
    print(f"  Order: {item.order}")
    print(f"  Roles: {item.visible_to_roles}")
    print(f"  Icon: {item.icon}")
    print()

# Check if they're truly identical
if post_job_items.count() == 2:
    item1, item2 = post_job_items[0], post_job_items[1]
    
    print("-"*70)
    print("Comparison:")
    print(f"  Same Title: {item1.title == item2.title}")
    print(f"  Same URL: {item1.url_name == item2.url_name}")
    print(f"  Same Parent ID: {item1.parent_id == item2.parent_id}")
    print(f"  Same Group ID: {item1.group_id == item2.group_id}")
    print(f"  Same Order: {item1.order == item2.order}")
    print()
    
    if (item1.title == item2.title and 
        item1.url_name == item2.url_name and 
        item1.parent_id == item2.parent_id and 
        item1.group_id == item2.group_id):
        
        print("  ⚠️  These are DUPLICATE items!")
        print(f"\n  Keeping ID {item1.id}, deactivating ID {item2.id}")
        
        item2.is_active = False
        item2.save()
        print(f"  ✓ Deactivated duplicate (ID: {item2.id})")

print("\n" + "="*70)
print("  Final Active Items for Hiring Manager")
print("="*70)

active_items = NavigationItem.objects.filter(is_active=True)
for item in active_items:
    if 'hiring_manager' in item.visible_to_roles:
        parent_name = item.parent.title if item.parent else 'TOP LEVEL'
        print(f"  ✓ {item.title} (Parent: {parent_name})")

print("="*70 + "\n")
