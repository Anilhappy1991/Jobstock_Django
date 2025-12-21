"""
Check current RPO navigation setup
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Jobstock.settings')
django.setup()

from App.models import NavigationItem

print("=" * 80)
print("CHECKING RPO NAVIGATION SETUP")
print("=" * 80)

# Find RPO Resume Upload item
rpo_upload = NavigationItem.objects.filter(url_name='App:rpo_resume_upload').first()
rpo_dashboard = NavigationItem.objects.filter(url_name='App:rpo_dashboard').first()

print("\n1. RPO Resume Upload Item:")
print("-" * 80)
if rpo_upload:
    print(f"   Title: {rpo_upload.title}")
    print(f"   URL Name: {rpo_upload.url_name}")
    print(f"   Parent: {rpo_upload.parent.title if rpo_upload.parent else 'None (top-level)'}")
    print(f"   Group: {rpo_upload.group.name if rpo_upload.group else 'None'}")
    print(f"   Is Active: {rpo_upload.is_active}")
else:
    print("   ❌ NOT FOUND")

print("\n2. RPO Dashboard Item:")
print("-" * 80)
if rpo_dashboard:
    print(f"   Title: {rpo_dashboard.title}")
    print(f"   URL Name: {rpo_dashboard.url_name}")
    print(f"   Parent: {rpo_dashboard.parent.title if rpo_dashboard.parent else 'None (top-level)'}")
    print(f"   Group: {rpo_dashboard.group.name if rpo_dashboard.group else 'None'}")
    print(f"   Is Active: {rpo_dashboard.is_active}")
else:
    print("   ❌ NOT FOUND")

print("\n" + "=" * 80)
print("RECOMMENDATION")
print("=" * 80)

if rpo_upload and rpo_dashboard:
    if rpo_upload.parent == rpo_dashboard:
        print("✅ Already configured correctly!")
        print("   'Upload Resumes' is a child of 'Dashboard'")
    else:
        print("⚠️  Configuration needed:")
        print("   Currently 'Upload Resumes' parent is:", rpo_upload.parent.title if rpo_upload.parent else "None")
        print("   Should be set to:", rpo_dashboard.title)
        print("\n   This will make 'Dashboard' highlight when on the upload page.")
else:
    print("❌ Missing navigation items - cannot configure")

print("=" * 80)
