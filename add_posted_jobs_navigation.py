"""
Add 'Posted Jobs' Navigation Menu Item to RPO Admin Group
This script adds a new navigation item for viewing all posted jobs in the RPO Admin dashboard
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Jobstock.settings')
django.setup()

from App.models import NavigationItem, NavigationGroup

print("=" * 80)
print("ADDING 'POSTED JOBS' NAVIGATION ITEM TO RPO ADMIN GROUP")
print("=" * 80)

# Get the Resume Management group (RPO Admin group)
resume_group = NavigationGroup.objects.filter(
    slug='rpo-resume-management',
    is_active=True
).first()

if not resume_group:
    print("\n❌ ERROR: Resume Management group not found or not active")
    print("   Please run setup_hierarchical_navigation.py first")
    exit(1)

print(f"\n✅ Found Navigation Group: {resume_group.name}")
print(f"   Slug: {resume_group.slug}")
print(f"   Visible to: {', '.join(resume_group.visible_to_roles)}")

# Get the Dashboard item (parent)
dashboard_item = NavigationItem.objects.filter(
    url_name='App:rpo_dashboard',
    group=resume_group,
    is_active=True
).first()

if not dashboard_item:
    print("\n❌ ERROR: Dashboard navigation item not found")
    print("   Please run update_rpo_navigation.py first")
    exit(1)

print(f"\n✅ Found Parent Item: {dashboard_item.title}")

# Check if Posted Jobs item already exists
existing_item = NavigationItem.objects.filter(
    url_name='App:rpo_posted_jobs',
    group=resume_group
).first()

if existing_item:
    print(f"\n⚠️  'Posted Jobs' navigation item already exists (ID: {existing_item.id})")
    print("   Updating configuration...")
    
    existing_item.title = 'Posted Jobs'
    existing_item.icon = 'fa-solid fa-briefcase'
    existing_item.parent = dashboard_item
    existing_item.order = 3
    existing_item.is_active = True
    existing_item.visible_to_roles = ['rpo_admin']
    existing_item.save()
    
    posted_jobs_item = existing_item
    action = "Updated"
else:
    print("\n✅ Creating new 'Posted Jobs' navigation item...")
    
    posted_jobs_item = NavigationItem.objects.create(
        group=resume_group,
        url_name='App:rpo_posted_jobs',
        title='Posted Jobs',
        icon='fa-solid fa-briefcase',
        parent=dashboard_item,  # Child of Dashboard
        order=3,  # After Upload Resumes (1) and All Resumes (2)
        is_active=True,
        visible_to_roles=['rpo_admin']
    )
    
    action = "Created"

print(f"\n✅ {action} Navigation Item:")
print(f"   Title: {posted_jobs_item.title}")
print(f"   URL: App:rpo_posted_jobs → /rpo-posted-jobs/")
print(f"   Icon: {posted_jobs_item.icon}")
print(f"   Parent: {posted_jobs_item.parent.title}")
print(f"   Order: {posted_jobs_item.order}")
print(f"   Visible to: {', '.join(posted_jobs_item.visible_to_roles)}")

print("\n" + "=" * 80)
print("NAVIGATION STRUCTURE (RPO Admin)")
print("=" * 80)

# Display the full navigation structure
all_items = NavigationItem.objects.filter(
    group=resume_group,
    is_active=True,
    parent=dashboard_item
).order_by('order')

print(f"\n📁 {resume_group.name}")
print(f"   ├── 📊 {dashboard_item.title} (App:rpo_dashboard)")
for item in all_items:
    is_last = item == all_items.last()
    connector = "└──" if is_last else "├──"
    print(f"   │   {connector} {item.icon} {item.title} ({item.url_name})")

print("\n" + "=" * 80)
print("✅ CONFIGURATION COMPLETE")
print("=" * 80)

print("\n📋 Next Steps:")
print("   1. Restart Django server (if running)")
print("   2. Login as RPO Admin")
print("   3. Navigate to Dashboard → Posted Jobs")
print("   4. View, search, filter, and sort all posted jobs")
print("\n📌 Features Available:")
print("   ✓ Search by title, company, skills")
print("   ✓ Filter by job type, category, status")
print("   ✓ Sort by date, title, deadline")
print("   ✓ Pagination (20 jobs per page)")
print("   ✓ Click job title to view details")
print("   ✓ Statistics: total, active, weekly, monthly")

print("\n" + "=" * 80)
