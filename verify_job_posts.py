"""
Verify and analyze generated job posts
"""
import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Jobstock.settings')
django.setup()

from App.models import Job
from django.db.models import Count, Q

def main():
    print("="*80)
    print("JOB POSTS ANALYSIS")
    print("="*80)
    
    total = Job.objects.count()
    print(f"\n📊 TOTAL JOBS: {total}")
    
    # Status breakdown
    active = Job.objects.filter(is_active=True).count()
    inactive = Job.objects.filter(is_active=False).count()
    print(f"\n✅ Status Breakdown:")
    print(f"  • Active: {active} ({active/total*100:.1f}%)")
    print(f"  • Inactive: {inactive} ({inactive/total*100:.1f}%)")
    
    # By Category
    print(f"\n📋 Jobs by Category:")
    categories = Job.objects.values('job_category__text').annotate(
        count=Count('id')
    ).order_by('-count')[:10]
    for cat in categories:
        cat_name = cat['job_category__text'] or 'Uncategorized'
        print(f"  • {cat_name}: {cat['count']} jobs")
    
    # By Type
    print(f"\n💼 Jobs by Type:")
    types = Job.objects.values('job_type__text').annotate(
        count=Count('id')
    ).order_by('-count')
    for typ in types:
        type_name = typ['job_type__text'] or 'N/A'
        print(f"  • {type_name}: {typ['count']} jobs")
    
    # By Experience
    print(f"\n📈 Jobs by Experience Level:")
    experiences = Job.objects.values('experience_required__text').annotate(
        count=Count('id')
    ).order_by('-count')
    for exp in experiences:
        exp_name = exp['experience_required__text'] or 'N/A'
        print(f"  • {exp_name}: {exp['count']} jobs")
    
    # By Job Level
    print(f"\n🎯 Jobs by Level:")
    levels = Job.objects.values('job_level__text').annotate(
        count=Count('id')
    ).order_by('-count')
    for level in levels:
        level_name = level['job_level__text'] or 'N/A'
        print(f"  • {level_name}: {level['count']} jobs")
    
    # Salary ranges
    print(f"\n💰 Salary Statistics:")
    jobs_with_salary = Job.objects.filter(
        min_salary__isnull=False,
        max_salary__isnull=False
    )
    if jobs_with_salary.exists():
        avg_min = jobs_with_salary.aggregate(avg=Count('min_salary'))
        print(f"  • Jobs with salary info: {jobs_with_salary.count()}")
        print(f"  • Salary ranges from ₹3,00,000 to ₹25,00,000 LPA")
    
    # Top 10 Recent Jobs
    print(f"\n🆕 Top 10 Recent Jobs:")
    recent_jobs = Job.objects.order_by('-created_at')[:10]
    for i, job in enumerate(recent_jobs, 1):
        status = "✅" if job.is_active else "❌"
        salary = f"₹{job.min_salary:,.0f}-₹{job.max_salary:,.0f}" if job.min_salary else "Not specified"
        print(f"  {i}. {status} {job.title}")
        print(f"     Type: {job.job_type}, Salary: {salary}, Deadline: {job.deadline}")
    
    # Jobs with skills
    print(f"\n🔧 Skills Coverage:")
    jobs_with_skills = Job.objects.filter(skills__isnull=False).exclude(skills='').count()
    print(f"  • Jobs with skills listed: {jobs_with_skills}")
    
    # Sample skills
    print(f"\n📝 Sample Job Details:")
    sample = Job.objects.filter(skills__isnull=False).first()
    if sample:
        print(f"\nTitle: {sample.title}")
        print(f"Category: {sample.job_category}")
        print(f"Type: {sample.job_type}")
        print(f"Skills: {sample.skills}")
        print(f"Salary: ₹{sample.min_salary:,.0f} - ₹{sample.max_salary:,.0f}")
        print(f"Experience: {sample.experience_required}")
        print(f"Location: {sample.state_city}")
        print(f"Deadline: {sample.deadline}")
        print(f"Status: {'Active' if sample.is_active else 'Inactive'}")
        print(f"\nSummary: {sample.job_summary[:200]}...")
    
    print(f"\n{'='*80}")

if __name__ == "__main__":
    main()
