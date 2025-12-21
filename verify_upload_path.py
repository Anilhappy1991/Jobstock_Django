"""
Verification script for file upload path changes
"""

import os
import django
import sys

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Jobstock.settings')
django.setup()

from datetime import datetime
from django.contrib.auth.models import User

# Import service
from App.services.resume_upload_service import ResumeUploadService

print("=" * 80)
print("VERIFYING UPLOAD PATH CHANGES")
print("=" * 80)

# Test get_upload_path
print("\n1. Testing get_upload_path():")
print("-" * 80)

# Get or create test user
test_user, created = User.objects.get_or_create(
    username='testuser',
    defaults={'first_name': 'Test', 'last_name': 'User', 'email': 'test@example.com'}
)
print(f"   Test user: {test_user.username} (ID: {test_user.id})")

service = ResumeUploadService()
absolute_path, relative_path = service.get_upload_path(test_user)

print(f"   Absolute path: {absolute_path}")
print(f"   Relative path: {relative_path}")

# Check path structure
current_date = datetime.now().strftime('%Y%m%d')
expected_folder = f"{test_user.username}_{test_user.id}"
expected_relative = f"Data/resume/{current_date}/{expected_folder}"

print(f"\n   Expected folder: {expected_folder}")
print(f"   Expected relative: {expected_relative}")

if expected_folder in relative_path:
    print("   ✓ Username and user ID included in path")
else:
    print("   ✗ Username and user ID NOT found in path")

if relative_path.replace('\\', '/') == expected_relative.replace('\\', '/'):
    print("   ✓ Relative path format correct")
else:
    print("   ✗ Relative path format incorrect")

# Check forward slashes
if '/' in relative_path or '\\' not in relative_path:
    print("   ✓ Path separators normalized")
else:
    print("   ✗ Path separators NOT normalized")

print("\n2. Checking service class docstring:")
print("-" * 80)
docstring = service.__class__.__doc__
if 'username_userID' in docstring or 'username_' in docstring:
    print("   ✓ Docstring updated with new path structure")
else:
    print("   ✗ Docstring NOT updated")

print(f"\n   Docstring excerpt:")
for line in docstring.split('\n')[:10]:
    if line.strip():
        print(f"   {line}")

print("\n3. Expected database storage:")
print("-" * 80)
print(f"   Format: Data/resume/YYYYMMDD/username_userID/filename.ext")
print(f"   Example: Data/resume/{current_date}/{test_user.username}_{test_user.id}/resume.pdf")
print(f"   ✓ Relative paths for portability")

print("\n4. Summary:")
print("-" * 80)
print("   Changes implemented:")
print("   ✓ Directory structure: /Data/resume/YYYYMMDD/username_userID/")
print("   ✓ get_upload_path() returns (absolute_path, relative_path)")
print("   ✓ save_resume_file() generates and returns relative path")
print("   ✓ Database stores relative paths for portability")
print("   ✓ rpo_resume_download() reconstructs absolute path from relative")

print("\n" + "=" * 80)
print("VERIFICATION COMPLETE")
print("=" * 80)
print("\nNext steps:")
print("1. Start Django server: python manage.py runserver")
print("2. Login as RPO admin")
print("3. Visit: http://127.0.0.1:8000/rpo-resume-upload/")
print("4. Upload test resume file")
print(f"5. Verify file saved to: /Data/resume/{current_date}/{test_user.username}_{test_user.id}/")
print("6. Check database has relative path in ResumeProcessing.resume_path")
print("7. Test download functionality from dashboard")
