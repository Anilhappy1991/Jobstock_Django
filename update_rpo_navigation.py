"""
Update RPO Resume Upload navigation to use RPO Dashboard as parent
This will make the Dashboard menu item active when on the upload page
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Jobstock.settings')
django.setup()

from App.models import NavigationItem, NavigationGroup

print("=" * 80)
print("UPDATING RPO NAVIGATION STRUCTURE")
print("=" * 80)

# Get the Resume Management group (active one)
resume_group = NavigationGroup.objects.filter(
    slug='rpo-resume-management',
    is_active=True
).first()

if not resume_group:
    print("❌ Resume Management group not found or not active")
    print("   Run setup_hierarchical_navigation.py first")
    exit(1)

# Find or create the active RPO Dashboard item
rpo_dashboard = NavigationItem.objects.filter(
    url_name='App:rpo_dashboard',
    group=resume_group
).first()

if not rpo_dashboard:
    print("\n1. Creating RPO Dashboard navigation item...")
    rpo_dashboard = NavigationItem.objects.create(
        group=resume_group,
        url_name='App:rpo_dashboard',
        title='Dashboard',
        icon='fa-solid fa-tachometer-alt',
        order=0,  # First item
        is_active=True,
        visible_to_roles=['rpo_admin'],
        parent=None  # Top level
    )
    print(f"   ✅ Created: {rpo_dashboard.title}")
else:
    # Update existing dashboard to ensure it's properly configured
    rpo_dashboard.title = 'Dashboard'
    rpo_dashboard.icon = 'fa-solid fa-tachometer-alt'
    rpo_dashboard.order = 0
    rpo_dashboard.is_active = True
    rpo_dashboard.parent = None
    rpo_dashboard.group = resume_group
    rpo_dashboard.save()
    print(f"\n1. Updated RPO Dashboard:")
    print(f"   ✅ {rpo_dashboard.title} (top-level, order: {rpo_dashboard.order})")

# Update RPO Upload to be child of Dashboard
print("\n2. Updating RPO Resume Upload...")
rpo_upload = NavigationItem.objects.filter(url_name='App:rpo_resume_upload').first()

if rpo_upload:
    rpo_upload.parent = rpo_dashboard  # Set dashboard as parent
    rpo_upload.group = resume_group
    rpo_upload.order = 1  # Second item under dashboard
    rpo_upload.is_active = True
    rpo_upload.save()
    print(f"   ✅ {rpo_upload.title}")
    print(f"      Parent: {rpo_upload.parent.title}")
    print(f"      Order: {rpo_upload.order}")
else:
    print("   ❌ Upload Resumes item not found")

# Update RPO Resume List
print("\n3. Updating RPO Resume List...")
rpo_list = NavigationItem.objects.filter(url_name='App:rpo_resume_list').first()

if rpo_list:
    rpo_list.parent = rpo_dashboard  # Also child of dashboard
    rpo_list.group = resume_group
    rpo_list.order = 2  # Third item under dashboard
    rpo_list.is_active = True
    rpo_list.save()
    print(f"   ✅ {rpo_list.title}")
    print(f"      Parent: {rpo_list.parent.title}")
    print(f"      Order: {rpo_list.order}")
else:
    print("   ❌ All Resumes item not found")

# Deactivate old Dashboard Home if it exists in different group
print("\n4. Cleaning up old navigation items...")
old_dashboard = NavigationItem.objects.filter(
    url_name='App:rpo_dashboard'
).exclude(group=resume_group)

if old_dashboard.exists():
    count = old_dashboard.update(is_active=False)
    print(f"   ✅ Deactivated {count} old dashboard item(s)")
else:
    print("   ✅ No old items to clean up")

print("\n" + "=" * 80)
print("NAVIGATION STRUCTURE (RPO Admin)")
print("=" * 80)

print(f"\n📁 {resume_group.name}")
print(f"   ├── 📊 {rpo_dashboard.title} (App:rpo_dashboard)")
print(f"   │   ├── 📤 {rpo_upload.title} (App:rpo_resume_upload)")
if rpo_list:
    print(f"   │   └── 📋 {rpo_list.title} (App:rpo_resume_list)")

print("\n" + "=" * 80)
print("✅ CONFIGURATION COMPLETE")
print("=" * 80)
print("\nResult:")
print("  When visiting /rpo-resume-upload/, the 'Dashboard' menu item")
print("  will now be highlighted as the active parent navigation.")
print("\n  Navigation hierarchy:")
print("    Dashboard (parent) → Upload Resumes (child)")
print("=" * 80)
