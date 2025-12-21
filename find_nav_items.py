"""
Find navigation items for Resume Upload and Post a Job
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Jobstock.settings')
django.setup()

from App.models import NavigationItem

print("\n" + "="*70)
print("  Finding Navigation Items")
print("="*70)

# Search for resume-related items
print("\n1. Resume Upload items (searching for 'resume' and 'upload'):")
resume_items = NavigationItem.objects.filter(title__icontains='resume')
for item in resume_items:
    upload_check = "✓ UPLOAD" if 'upload' in item.title.lower() else ""
    print(f"  - {item.title} {upload_check}")
    print(f"    URL Name: {item.url_name}")
    print(f"    Active: {item.is_active}")
    print()

# Search for job posting items
print("\n2. Post Job items (searching for 'post' and 'job'):")
post_items = NavigationItem.objects.filter(title__icontains='post')
for item in post_items:
    job_check = "✓ JOB" if 'job' in item.title.lower() else ""
    print(f"  - {item.title} {job_check}")
    print(f"    URL Name: {item.url_name}")
    print(f"    Active: {item.is_active}")
    print()

# Also search for 'submit job'
print("\n3. Submit Job items (searching for 'submit'):")
submit_items = NavigationItem.objects.filter(title__icontains='submit')
for item in submit_items:
    print(f"  - {item.title}")
    print(f"    URL Name: {item.url_name}")
    print(f"    Active: {item.is_active}")
    print()

print("="*70 + "\n")
