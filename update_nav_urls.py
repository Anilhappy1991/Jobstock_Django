"""Update all navigation items to use existing URLs"""
import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Jobstock.settings')
django.setup()

from App.models import NavigationItem

print("=== Updating Navigation URLs ===\n")

# Map navigation items to actual existing URLs
url_updates = [
    # Main Menu
    ('Applications', 'App:employer_applicants_jobs'),
    ('Candidates', 'App:employer_shortlist_candidates'),
    ('Interviews', 'App:employer_messages'),  # Using messages as placeholder
    ('Manage Jobs', 'App:employer_jobs'),
    ('Job Templates', 'App:employer_submit_job'),  # Using submit job
    
    # Reports & Analytics
    ('Hiring Pipeline', 'App:employer_dashboard'),  # Placeholder
    ('Analytics', 'App:employer_dashboard'),  # Placeholder
    ('Reports', 'App:employer_dashboard'),  # Placeholder
    
    # Settings
    ('Team Members', 'App:employer_profile'),  # Placeholder
    ('Notifications', 'App:employer_messages'),  # Placeholder
    ('Account Settings', 'App:employer_change_password'),
    
    # Features
    ('Saved Candidates', 'App:employer_shortlist_candidates'),
    ('AI Screening', 'App:employer_applicants_jobs'),  # Placeholder
    ('Help & Support', 'App:employer_dashboard'),  # Placeholder
]

for title, url_name in url_updates:
    items = NavigationItem.objects.filter(title=title)
    if items.exists():
        count = items.update(url_name=url_name)
        print(f"✓ Updated '{title}' → {url_name}")
    else:
        print(f"  '{title}' not found")

print("\n=== Update Complete ===")
print("All navigation items now use existing URL patterns.")
print("\nVerify with: python check_nav_items.py")
