"""Quick check of ResumeProcessing records"""
import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Jobstock.settings')
django.setup()

from App.models import ResumeProcessing

records = ResumeProcessing.objects.all()
print(f'\n✅ Total Records: {records.count()}\n')

for r in records:
    skills_count = r.resume_json.get('skills', {}).get('total_skills', 0) if r.resume_json else 0
    print(f'{r.id}. {r.user.username} - {r.original_filename}')
    print(f'   Status: {r.status}')
    print(f'   Skills: {skills_count}')
    print(f'   Words: {r.word_count}')
    print(f'   Created: {r.created_at}')
    print()
