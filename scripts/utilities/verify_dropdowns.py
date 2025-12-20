import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Jobstock.settings')
django.setup()

from App.models import DropdownGroup, DropdownMaster

print("=== Dropdown Groups ===")
for group in DropdownGroup.objects.all():
    print(f"ID: {group.id}, Text: {group.text}, Value: {group.value}")

print("\n=== Dropdown Master Data ===")
for group in DropdownGroup.objects.all():
    print(f"\n{group.text}:")
    for item in group.items.all():
        print(f"  ID: {item.id}, Text: {item.text}, Value: {item.value}")
