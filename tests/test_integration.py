"""
Test Resume Processing Integration
Tests the complete flow: upload -> database entry -> processing -> status update
"""
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Jobstock.settings')
django.setup()

from django.contrib.auth.models import User
from App.models import Profile, ResumeProcessing
from pathlib import Path
import shutil

def test_resume_processing_flow():
    """Test the complete resume processing workflow"""
    
    print("=" * 80)
    print("TESTING RESUME PROCESSING INTEGRATION")
    print("=" * 80)
    print()
    
    # Get or create a test user
    user, created = User.objects.get_or_create(
        username='testuser',
        defaults={
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User'
        }
    )
    if created:
        user.set_password('testpass123')
        user.save()
        print(f"✅ Created test user: {user.username}")
    else:
        print(f"✅ Using existing user: {user.username}")
    
    # Get or create profile
    profile, created = Profile.objects.get_or_create(
        user=user,
        defaults={
            'full_name': 'Test User',
            'phone': '1234567890'
        }
    )
    print(f"✅ Profile: {profile}")
    print()
    
    # Simulate a resume upload
    test_resume_path = Path("Rituranjan ResumeAZ.pdf")
    if not test_resume_path.exists():
        print("❌ Test resume file not found!")
        return
    
    # Create a ResumeProcessing record (simulating what happens on upload)
    print("📝 Creating ResumeProcessing record...")
    resume_record = ResumeProcessing.objects.create(
        user=user,
        profile=profile,
        resume_path=str(test_resume_path),
        original_filename=test_resume_path.name,
        file_size=test_resume_path.stat().st_size,
        file_extension=test_resume_path.suffix.lower(),
        status='pending'
    )
    print(f"✅ Created record ID: {resume_record.id}")
    print(f"   Status: {resume_record.status}")
    print(f"   User: {resume_record.user.username}")
    print(f"   File: {resume_record.original_filename}")
    print()
    
    # Now process it
    print("🔄 Processing resume...")
    from App.tasks_simple import SimpleDocumentProcessor
    from datetime import datetime
    
    processor = SimpleDocumentProcessor()
    
    # Update status to processing
    resume_record.status = 'processing'
    resume_record.processing_started_at = datetime.now()
    resume_record.save()
    print(f"   Status updated to: {resume_record.status}")
    
    try:
        # Extract all data
        text = processor.extract_text(str(test_resume_path))
        contact_info = processor.extract_contact_info(text)
        skills_results = processor.extract_skills(text)
        entity_results = processor.extract_entities(text)
        stats = processor.get_text_statistics(text)
        sentiment = processor.analyze_sentiment(text)
        
        # Compile results
        results = {
            'contact_info': contact_info,
            'skills': skills_results,
            'entities': entity_results,
            'statistics': stats,
            'sentiment': sentiment
        }
        
        # Update database record
        resume_record.resume_text = text
        resume_record.resume_json = results
        resume_record.extracted_skills = ', '.join(skills_results['skills'][:30])
        resume_record.extracted_email = contact_info['emails'][0] if contact_info['emails'] else None
        resume_record.extracted_phone = contact_info['phones'][0] if contact_info['phones'] else None
        resume_record.years_of_experience = ', '.join(map(str, skills_results['experience_years'][:3]))
        resume_record.sentiment_score = sentiment['polarity']
        resume_record.word_count = stats['word_count']
        resume_record.status = 'completed'
        resume_record.processing_completed_at = datetime.now()
        resume_record.save()
        
        print(f"✅ Processing completed successfully!")
        print()
        
        # Display results
        print("=" * 80)
        print("PROCESSING RESULTS")
        print("=" * 80)
        print(f"📊 Record ID: {resume_record.id}")
        print(f"👤 User: {resume_record.user.username}")
        print(f"📄 File: {resume_record.original_filename}")
        print(f"✅ Status: {resume_record.status}")
        print(f"📝 Text Length: {len(resume_record.resume_text)} characters")
        print(f"🔧 Skills Found: {skills_results['total_skills']}")
        print(f"   Top Skills: {', '.join(skills_results['skills'][:10])}")
        print(f"📧 Email: {resume_record.extracted_email or 'Not found'}")
        print(f"📱 Phone: {resume_record.extracted_phone or 'Not found'}")
        print(f"💼 Experience: {resume_record.years_of_experience}")
        print(f"📖 Word Count: {resume_record.word_count}")
        print(f"😊 Sentiment: {sentiment['sentiment_label']} ({sentiment['polarity']:.3f})")
        print(f"⏱️  Processing Duration: {resume_record.get_processing_duration():.2f} seconds")
        print()
        
        # Show how to query this data
        print("=" * 80)
        print("QUERYING PROCESSED RESUMES")
        print("=" * 80)
        
        # Get all completed resumes for this user
        completed_resumes = ResumeProcessing.objects.filter(
            user=user,
            status='completed'
        ).order_by('-created_at')
        
        print(f"\n✅ Found {completed_resumes.count()} completed resume(s) for {user.username}:")
        for idx, record in enumerate(completed_resumes, 1):
            print(f"\n{idx}. {record.original_filename}")
            print(f"   Uploaded: {record.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"   Skills: {record.resume_json['skills']['total_skills']}")
            print(f"   Words: {record.word_count}")
            print(f"   Sentiment: {record.resume_json['sentiment']['sentiment_label']}")
        
        print("\n" + "=" * 80)
        print("✅ TEST COMPLETED SUCCESSFULLY!")
        print("=" * 80)
        print()
        print("📌 Next Steps:")
        print("   1. Upload a resume through the Django profile page")
        print("   2. The system will automatically create a ResumeProcessing record")
        print("   3. Run auto_process_resumes.py to process it")
        print("   4. View the results on the candidate profile page")
        print()
        
    except Exception as e:
        print(f"\n❌ Error during processing: {e}")
        import traceback
        traceback.print_exc()
        
        # Update record with error
        resume_record.status = 'failed'
        resume_record.error_message = str(e)
        resume_record.processing_completed_at = datetime.now()
        resume_record.save()


if __name__ == '__main__':
    test_resume_processing_flow()
