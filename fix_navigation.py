"""Fix navigation items - remove duplicates and update URLs"""
import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Jobstock.settings')
django.setup()

from App.models import NavigationGroup, NavigationItem

print("=== Fixing Navigation Items ===\n")

# Step 1: Remove items from the FIRST Main Menu group (without App: prefix)
print("Step 1: Removing duplicate Main Menu items...")
all_groups = NavigationGroup.objects.filter(name="Main Menu", is_active=True)

# Find the group with items WITHOUT App: prefix
for group in all_groups:
    items = group.items.filter(url_name="employer_dashboard")
    if items.exists():
        print(f"  Deleting {group.items.count()} items from group ID {group.id}")
        group.items.all().delete()
        group.delete()
        print("  ✓ Deleted duplicate group")
        break

# Step 2: Update remaining items to ensure they have correct URLs
print("\nStep 2: Updating URL patterns...")

url_mappings = {
    # Map current url_name to correct url_name
    'employer_applications': 'App:employer_applicants_jobs',
    'employer_candidates': 'App:employer_shortlist_candidates',
    'employer_interviews': 'App:employer_messages',  # Temporary mapping
    'employer_pipeline': 'App:employer_dashboard',  # Temporary
    'employer_analytics': 'App:employer_dashboard',  # Temporary
    'employer_reports': 'App:employer_dashboard',  # Temporary
    'employer_team': 'App:employer_profile',  # Temporary
    'employer_notifications': 'App:employer_messages',  # Temporary
    'employer_settings': 'App:employer_change_password',
    'employer_saved_candidates': 'App:employer_shortlist_candidates',
    'employer_ai_screening': 'App:employer_applicants_jobs',  # Temporary
    'employer_help': 'App:employer_dashboard',  # Temporary
    'employer_manage_jobs': 'App:employer_jobs',
    'employer_job_templates': 'App:employer_submit_job',  # Temporary
}

for old_url, new_url in url_mappings.items():
    items = NavigationItem.objects.filter(url_name=old_url)
    if items.exists():
        count = items.update(url_name=new_url)
        print(f"  ✓ Updated {count} items: {old_url} → {new_url}")

# Step 3: Fix parent items with # url_name
print("\nStep 3: Fixing parent menu items...")
parent_items = NavigationItem.objects.filter(url_name__startswith='#')
for item in parent_items:
    item.url_name = 'javascript:void(0)'
    item.save()
    print(f"  ✓ Fixed parent item: {item.title}")

print("\n=== Fix Complete ===")
print("Navigation items have been updated to use existing URL patterns.")
print("Run: python manage.py runserver")
print("Then login and check navigation.")
