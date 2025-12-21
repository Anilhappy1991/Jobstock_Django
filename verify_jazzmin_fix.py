"""
Simple verification that our custom template tag is loaded correctly.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Jobstock.settings')
django.setup()

from django import template

print("=" * 60)
print("JAZZMIN FIX VERIFICATION")
print("=" * 60)

# Check if our custom template tag library exists
try:
    from App.templatetags import jazzmin_fixes
    print("✅ Custom template tag library 'jazzmin_fixes' loaded successfully")
    
    # Check if the function exists
    if hasattr(jazzmin_fixes, 'jazzmin_paginator_number'):
        print("✅ Function 'jazzmin_paginator_number' exists in jazzmin_fixes")
    else:
        print("❌ Function 'jazzmin_paginator_number' NOT FOUND in jazzmin_fixes")
        
    # Check if it's registered as a template tag
    register = jazzmin_fixes.register
    if 'jazzmin_paginator_number' in register.tags:
        print("✅ Template tag 'jazzmin_paginator_number' is registered")
    else:
        print("⚠️  Template tag 'jazzmin_paginator_number' is NOT registered")
        
except ImportError as e:
    print(f"❌ Failed to import jazzmin_fixes: {e}")

# Check if our pagination template exists
import os
from pathlib import Path

template_path = Path("templates/admin/pagination.html")
if template_path.exists():
    print(f"✅ Override template exists: {template_path}")
    
    # Check if it loads our custom tag
    with open(template_path, 'r') as f:
        content = f.read()
        if 'jazzmin_fixes' in content:
            print("✅ Template loads 'jazzmin_fixes' tag library")
        else:
            print("❌ Template does NOT load 'jazzmin_fixes' tag library")
else:
    print(f"❌ Override template NOT FOUND: {template_path}")

print("\n" + "=" * 60)
print("NEXT STEPS:")
print("=" * 60)
print("1. Server is running at: http://127.0.0.1:8000/")
print("2. Login to admin: http://127.0.0.1:8000/admin/")
print("3. Test DropdownMaster page: http://127.0.0.1:8000/admin/App/dropdownmaster/")
print("\nIf you see the DropdownMaster list without errors, the fix is working! ✅")
print("=" * 60)
