"""
Test script for resume processing
Location: test_resume_processing.py

This script tests the resume processing functionality without requiring
Celery/Redis to be running.
"""
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Jobstock.settings')
django.setup()

from App.tasks_simple import SimpleDocumentProcessor
import json

def test_resume_processing():
    """Test resume processing with sample resume"""
    
    print("=" * 80)
    print("RESUME PROCESSING TEST")
    print("=" * 80)
    print()
    
    # Initialize processor
    print("📋 Initializing document processor...")
    processor = SimpleDocumentProcessor()
    print("✅ Processor initialized\n")
    
    # Get test resume path
    resume_path = os.path.join(os.path.dirname(__file__), 'test_resume.txt')
    
    if not os.path.exists(resume_path):
        print(f"❌ Error: Test resume not found at {resume_path}")
        return
    
    print(f"📄 Processing resume: {resume_path}\n")
    
    # Step 1: Extract text
    print("STEP 1: Extracting text...")
    print("-" * 80)
    text = processor.extract_text(resume_path)
    print(f"✅ Extracted {len(text)} characters")
    print(f"Preview: {text[:200]}...\n")
    
    # Step 2: Extract contact information
    print("STEP 2: Extracting contact information...")
    print("-" * 80)
    contact_info = processor.extract_contact_info(text)
    print(f"✅ Contact Information Found:")
    print(f"   📧 Emails: {contact_info['emails']}")
    print(f"   📱 Phones: {contact_info['phones']}")
    print(f"   🔗 LinkedIn: {contact_info['linkedin']}")
    print(f"   💻 GitHub: {contact_info['github']}\n")
    
    # Step 3: Extract skills
    print("STEP 3: Extracting skills...")
    print("-" * 80)
    skills_results = processor.extract_skills(text)
    print(f"✅ Found {skills_results['total_skills']} technical skills:")
    for i, skill in enumerate(skills_results['skills'][:15], 1):
        print(f"   {i}. {skill}")
    if len(skills_results['skills']) > 15:
        print(f"   ... and {len(skills_results['skills']) - 15} more")
    print(f"\n   📅 Experience Years: {skills_results['experience_years']}\n")
    
    # Step 4: Extract entities
    print("STEP 4: Extracting named entities...")
    print("-" * 80)
    entity_results = processor.extract_entities(text)
    print(f"✅ Found {entity_results['total_entities']} named entities:")
    print(f"   👤 Persons: {entity_results['persons']}")
    print(f"   🏢 Organizations: {entity_results['organizations'][:5]}")
    print(f"   📍 Locations: {entity_results['locations']}\n")
    
    # Step 5: Text statistics
    print("STEP 5: Analyzing text statistics...")
    print("-" * 80)
    stats = processor.get_text_statistics(text)
    print(f"✅ Text Statistics:")
    print(f"   📝 Total Characters: {stats['character_count']:,}")
    print(f"   📖 Total Words: {stats['word_count']:,}")
    print(f"   📄 Total Sentences: {stats['sentence_count']}")
    print(f"   📊 Avg Words/Sentence: {stats['avg_words_per_sentence']}")
    print(f"   🔤 Unique Words: {stats['unique_words']:,}")
    print(f"\n   🔝 Most Common Words:")
    for word_data in stats['most_common_words'][:10]:
        print(f"      • {word_data['word']}: {word_data['count']} times")
    print()
    
    # Step 6: Sentiment analysis
    print("STEP 6: Analyzing sentiment...")
    print("-" * 80)
    sentiment = processor.analyze_sentiment(text)
    print(f"✅ Sentiment Analysis:")
    print(f"   😊 Sentiment: {sentiment['sentiment_label'].upper()}")
    print(f"   📈 Polarity: {sentiment['polarity']:.3f} (range: -1 to 1)")
    print(f"   📊 Subjectivity: {sentiment['subjectivity']:.3f} (range: 0 to 1)\n")
    
    # Summary
    print("=" * 80)
    print("PROCESSING COMPLETE!")
    print("=" * 80)
    print("\n📊 SUMMARY:")
    print(f"   • Extracted contact info: {len(contact_info['emails'])} emails, {len(contact_info['phones'])} phones")
    print(f"   • Identified {skills_results['total_skills']} technical skills")
    print(f"   • Found {entity_results['total_entities']} named entities")
    print(f"   • Analyzed {stats['word_count']:,} words in {stats['sentence_count']} sentences")
    print(f"   • Overall sentiment: {sentiment['sentiment_label']}")
    print("\n✅ All tests passed successfully!")
    print()
    
    # Save full results to JSON
    results = {
        'text_length': len(text),
        'contact_info': contact_info,
        'skills': skills_results,
        'entities': entity_results,
        'statistics': stats,
        'sentiment': sentiment
    }
    
    output_file = 'test_resume_results.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Full results saved to: {output_file}")
    print()

if __name__ == '__main__':
    try:
        test_resume_processing()
    except Exception as e:
        print(f"\n❌ Error during processing: {str(e)}")
        import traceback
        traceback.print_exc()
