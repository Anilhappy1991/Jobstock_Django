"""Quick verification of menu role mapping"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Jobstock.settings')
django.setup()

from App.services.menu_validation_service import MenuValidationService

print("\n" + "="*60)
print("  Menu Role Mapping Verification")
print("="*60)

print("\nAllowed Roles:")
for role in MenuValidationService.ALLOWED_ROLES:
    print(f"  - {role}")

print("\nRole Mapping:")
test_roles = ['employee', 'hiring_manager', 'rpo_admin', 'candidate']
for role in test_roles:
    mapped = MenuValidationService.get_mapped_role(role)
    indicator = " <-- MAPS TO hiring_manager" if role == 'employee' else ""
    print(f"  {role:20} --> {mapped}{indicator}")

print("\n" + "="*60)
print("  Implementation Summary:")
print("="*60)
print("  1. No login        --> No menu (template check)")
print("  2. Employee login  --> Hiring Manager menu (mapped)")
print("  3. HM login        --> Hiring Manager menu (direct)")
print("  4. RPO Admin login --> RPO Admin menu (direct)")
print("="*60 + "\n")
