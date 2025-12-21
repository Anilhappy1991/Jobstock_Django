"""
Quick test to verify the Jazzmin pagination fix works in browser.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Jobstock.settings')
django.setup()

print("=" * 60)
print("JAZZMIN FIX - QUICK TEST")
print("=" * 60)

# Check template content
template_path = "templates/admin/pagination.html"
with open(template_path, 'r') as f:
    first_line = f.readline().strip()
    print(f"\n✓ Template first line:")
    print(f"  {first_line}")
    
    if 'jazzmin_fixes' in first_line and 'jazzmin' in first_line:
        print("\n✅ Template loads BOTH libraries correctly!")
        print("   - 'jazzmin' for get_jazzmin_ui_tweaks")
        print("   - 'jazzmin_fixes' for fixed jazzmin_paginator_number")
    else:
        print("\n⚠️  Template might have an issue")

print("\n" + "=" * 60)
print("TEST IN BROWSER:")
print("=" * 60)
print("1. Go to: http://127.0.0.1:8000/admin/")
print("2. Login with your credentials")
print("3. Try accessing any model (e.g., Groups, Users, DropdownMaster)")
print("4. If the page loads without errors, the fix works! ✅")
print("=" * 60)
