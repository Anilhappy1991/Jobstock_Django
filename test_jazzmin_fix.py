"""
Test script to verify Jazzmin pagination fix works.
This will test accessing the DropdownMaster admin page.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Jobstock.settings')
django.setup()

from django.test import RequestFactory, Client
from django.contrib.auth.models import User
from django.urls import reverse

# Create a test client
client = Client()

# Get or create a superuser
try:
    admin_user = User.objects.filter(is_superuser=True).first()
    if not admin_user:
        admin_user = User.objects.create_superuser(
            username='admin_test',
            email='admin@test.com',
            password='admin123'
        )
        print(f"✓ Created test superuser: {admin_user.username}")
    else:
        print(f"✓ Using existing superuser: {admin_user.username}")
    
    # Login
    client.login(username=admin_user.username, password='admin123')
    print(f"✓ Logged in as {admin_user.username}")
    
    # Try to access the DropdownMaster admin page
    url = '/admin/App/dropdownmaster/'
    print(f"\n📋 Testing URL: {url}")
    
    response = client.get(url)
    
    if response.status_code == 200:
        print(f"✅ SUCCESS! DropdownMaster admin page loaded without errors")
        print(f"   Status Code: {response.status_code}")
        print(f"   Content Length: {len(response.content)} bytes")
        
        # Check if pagination template is in the response
        if b'pagination' in response.content:
            print(f"   ✓ Pagination elements found in response")
        
        print(f"\n🎉 Fix is working! You can now access:")
        print(f"   http://127.0.0.1:8000{url}")
        
    elif response.status_code == 500:
        print(f"❌ FAILED - Server Error (500)")
        print(f"   The template tag fix may not be working")
        print(f"   Check the error in browser at: http://127.0.0.1:8000{url}")
        
    else:
        print(f"⚠️  Unexpected Status Code: {response.status_code}")
        print(f"   Check the URL in browser: http://127.0.0.1:8000{url}")
        
except Exception as e:
    print(f"❌ Error during test: {e}")
    import traceback
    traceback.print_exc()
