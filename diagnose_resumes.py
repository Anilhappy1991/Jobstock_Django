"""Check resume processing records and file paths"""
import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Jobstock.settings')
django.setup()

from App.models import ResumeProcessing
from pathlib import Path

print("\n" + "=" * 80)
print("RESUME PROCESSING DIAGNOSTICS")
print("=" * 80 + "\n")

records = ResumeProcessing.objects.all()
print(f"Total Records: {records.count()}\n")

for r in records:
    print(f"ID: {r.id}")
    print(f"User: {r.user.username}")
    print(f"Filename: {r.original_filename}")
    print(f"Status: {r.status}")
    print(f"Resume Path: {r.resume_path}")
    print(f"File Exists: {Path(r.resume_path).exists() if r.resume_path else 'No path'}")
    print(f"Created: {r.created_at}")
    print("-" * 80)
    print()

# Check for pending records
pending = ResumeProcessing.objects.filter(status='pending')
print(f"\n✅ Pending Records: {pending.count()}")
for p in pending:
    print(f"   - {p.original_filename} (User: {p.user.username})")
    print(f"     Path: {p.resume_path}")
    print(f"     Exists: {Path(p.resume_path).exists() if p.resume_path else False}")
