"""
Extract resume data from PDF and save results
Location: extract_resume_data.py
"""
import os
import sys
import django
import json
from datetime import datetime

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Jobstock.settings')
django.setup()

from App.tasks_simple import SimpleDocumentProcessor

def extract_resume_data(resume_path):
    """Extract data from resume file"""
    
    if not os.path.exists(resume_path):
        print(f"❌ Error: Resume file not found at {resume_path}")
        return None
    
    # Get filename without extension for output
    base_name = os.path.splitext(os.path.basename(resume_path))[0]
    output_json = f"{base_name}_extracted_data.json"
    output_txt = f"{base_name}_extracted_data.txt"
    
    print("=" * 80)
    print(f"EXTRACTING RESUME DATA: {os.path.basename(resume_path)}")
    print("=" * 80)
    print()
    
    # Initialize processor
    print("📋 Initializing document processor...")
    processor = SimpleDocumentProcessor()
    print("✅ Processor initialized\n")
    
    try:
        # Step 1: Extract text
        print("STEP 1: Extracting text from PDF...")
        print("-" * 80)
        text = processor.extract_text(resume_path)
        
        if not text:
            print("❌ No text could be extracted from the document")
            return None
            
        print(f"✅ Extracted {len(text)} characters")
        print(f"Preview (first 300 chars):\n{text[:300]}...\n")
        
        # Step 2: Extract contact information
        print("STEP 2: Extracting contact information...")
        print("-" * 80)
        contact_info = processor.extract_contact_info(text)
        print(f"✅ Contact Information:")
        print(f"   📧 Emails: {', '.join(contact_info['emails']) if contact_info['emails'] else 'None found'}")
        print(f"   📱 Phones: {', '.join(contact_info['phones']) if contact_info['phones'] else 'None found'}")
        print(f"   🔗 LinkedIn: {', '.join(contact_info['linkedin']) if contact_info['linkedin'] else 'None found'}")
        print(f"   💻 GitHub: {', '.join(contact_info['github']) if contact_info['github'] else 'None found'}\n")
        
        # Step 3: Extract skills
        print("STEP 3: Extracting technical skills...")
        print("-" * 80)
        skills_results = processor.extract_skills(text)
        print(f"✅ Found {skills_results['total_skills']} technical skills:")
        if skills_results['skills']:
            for i, skill in enumerate(skills_results['skills'][:20], 1):
                print(f"   {i}. {skill}")
            if len(skills_results['skills']) > 20:
                print(f"   ... and {len(skills_results['skills']) - 20} more")
        print(f"\n   📅 Experience Years Mentioned: {skills_results['experience_years']}\n")
        
        # Step 4: Extract entities
        print("STEP 4: Extracting named entities...")
        print("-" * 80)
        entity_results = processor.extract_entities(text)
        print(f"✅ Found {entity_results['total_entities']} named entities:")
        print(f"   👤 Persons: {', '.join(entity_results['persons'][:5]) if entity_results['persons'] else 'None'}")
        print(f"   🏢 Organizations: {', '.join(entity_results['organizations'][:10]) if entity_results['organizations'] else 'None'}")
        print(f"   📍 Locations: {', '.join(entity_results['locations'][:5]) if entity_results['locations'] else 'None'}\n")
        
        # Step 5: Text statistics
        print("STEP 5: Analyzing text statistics...")
        print("-" * 80)
        stats = processor.get_text_statistics(text)
        print(f"✅ Text Statistics:")
        print(f"   📝 Total Characters: {stats['character_count']:,}")
        print(f"   📖 Total Words: {stats['word_count']:,}")
        print(f"   📄 Total Sentences: {stats['sentence_count']}")
        print(f"   🔤 Unique Words: {stats['unique_words']:,}\n")
        
        # Step 6: Sentiment analysis
        print("STEP 6: Analyzing sentiment...")
        print("-" * 80)
        sentiment = processor.analyze_sentiment(text)
        print(f"✅ Sentiment Analysis:")
        print(f"   😊 Sentiment: {sentiment['sentiment_label'].upper()}")
        print(f"   📈 Polarity: {sentiment['polarity']:.3f}")
        print(f"   📊 Subjectivity: {sentiment['subjectivity']:.3f}\n")
        
        # Compile results
        results = {
            'metadata': {
                'filename': os.path.basename(resume_path),
                'extracted_at': datetime.now().isoformat(),
                'file_size_bytes': os.path.getsize(resume_path)
            },
            'text_content': {
                'full_text': text,
                'length': len(text),
                'word_count': stats['word_count']
            },
            'contact_info': contact_info,
            'skills': skills_results,
            'entities': entity_results,
            'statistics': stats,
            'sentiment': sentiment
        }
        
        # Save JSON
        print("=" * 80)
        print("SAVING RESULTS...")
        print("=" * 80)
        
        with open(output_json, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"✅ JSON saved: {output_json}")
        
        # Save human-readable TXT
        with open(output_txt, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write(f"RESUME EXTRACTION RESULTS\n")
            f.write(f"File: {os.path.basename(resume_path)}\n")
            f.write(f"Extracted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 80 + "\n\n")
            
            f.write("CONTACT INFORMATION\n")
            f.write("-" * 80 + "\n")
            f.write(f"Emails: {', '.join(contact_info['emails']) if contact_info['emails'] else 'None found'}\n")
            f.write(f"Phones: {', '.join(contact_info['phones']) if contact_info['phones'] else 'None found'}\n")
            f.write(f"LinkedIn: {', '.join(contact_info['linkedin']) if contact_info['linkedin'] else 'None found'}\n")
            f.write(f"GitHub: {', '.join(contact_info['github']) if contact_info['github'] else 'None found'}\n\n")
            
            f.write("TECHNICAL SKILLS\n")
            f.write("-" * 80 + "\n")
            f.write(f"Total: {skills_results['total_skills']}\n")
            f.write(f"Skills: {', '.join(skills_results['skills'])}\n")
            f.write(f"Experience Years: {', '.join(map(str, skills_results['experience_years']))}\n\n")
            
            f.write("NAMED ENTITIES\n")
            f.write("-" * 80 + "\n")
            f.write(f"Total: {entity_results['total_entities']}\n")
            f.write(f"Persons: {', '.join(entity_results['persons'])}\n")
            f.write(f"Organizations: {', '.join(entity_results['organizations'])}\n")
            f.write(f"Locations: {', '.join(entity_results['locations'])}\n\n")
            
            f.write("TEXT STATISTICS\n")
            f.write("-" * 80 + "\n")
            f.write(f"Characters: {stats['character_count']:,}\n")
            f.write(f"Words: {stats['word_count']:,}\n")
            f.write(f"Sentences: {stats['sentence_count']}\n")
            f.write(f"Unique Words: {stats['unique_words']:,}\n")
            f.write(f"Most Common Words:\n")
            for word_data in stats['most_common_words'][:15]:
                f.write(f"  - {word_data['word']}: {word_data['count']} times\n")
            f.write("\n")
            
            f.write("SENTIMENT ANALYSIS\n")
            f.write("-" * 80 + "\n")
            f.write(f"Sentiment: {sentiment['sentiment_label'].upper()}\n")
            f.write(f"Polarity: {sentiment['polarity']:.3f} (range: -1 to 1)\n")
            f.write(f"Subjectivity: {sentiment['subjectivity']:.3f} (range: 0 to 1)\n\n")
            
            f.write("FULL TEXT CONTENT\n")
            f.write("=" * 80 + "\n")
            f.write(text)
        
        print(f"✅ TXT saved: {output_txt}")
        print()
        print("=" * 80)
        print("✅ EXTRACTION COMPLETE!")
        print("=" * 80)
        print(f"\n📊 Summary:")
        print(f"   • Contact: {len(contact_info['emails'])} emails, {len(contact_info['phones'])} phones")
        print(f"   • Skills: {skills_results['total_skills']} identified")
        print(f"   • Entities: {entity_results['total_entities']} found")
        print(f"   • Text: {stats['word_count']:,} words, {stats['sentence_count']} sentences")
        print(f"   • Sentiment: {sentiment['sentiment_label']}\n")
        
        return results
        
    except Exception as e:
        print(f"\n❌ Error during processing: {str(e)}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == '__main__':
    # Get resume path from command line or use default
    if len(sys.argv) > 1:
        resume_path = sys.argv[1]
    else:
        # Default to the attached PDF
        resume_path = "Rituranjan ResumeAZ.pdf"
    
    if not os.path.isabs(resume_path):
        resume_path = os.path.join(os.path.dirname(__file__), resume_path)
    
    extract_resume_data(resume_path)
