"""
Automated Resume Processing Script
Monitors data/candidate-resume folder and processes all resumes
Moves processed files to data/candidate-resume/process
"""
import os
import sys
import django
import json
import shutil
from datetime import datetime
from pathlib import Path

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Jobstock.settings')
django.setup()

from App.tasks_simple import SimpleDocumentProcessor

# Define paths
BASE_DIR = Path(__file__).parent
INPUT_FOLDER = BASE_DIR / "data" / "candidate-resume"
PROCESSED_FOLDER = INPUT_FOLDER / "process"
RESULTS_FOLDER = INPUT_FOLDER / "results"

# Supported file extensions
SUPPORTED_EXTENSIONS = ['.pdf', '.docx', '.doc', '.txt']


def setup_folders():
    """Create necessary folders if they don't exist"""
    INPUT_FOLDER.mkdir(parents=True, exist_ok=True)
    PROCESSED_FOLDER.mkdir(parents=True, exist_ok=True)
    RESULTS_FOLDER.mkdir(parents=True, exist_ok=True)
    print(f"✅ Folders initialized:")
    print(f"   📂 Input: {INPUT_FOLDER}")
    print(f"   📂 Processed: {PROCESSED_FOLDER}")
    print(f"   📂 Results: {RESULTS_FOLDER}\n")


def process_resume_file(file_path):
    """Process a single resume file and extract data"""
    
    print("=" * 80)
    print(f"📄 PROCESSING: {file_path.name}")
    print("=" * 80)
    
    try:
        # Initialize processor
        processor = SimpleDocumentProcessor()
        
        # Extract text
        print("⏳ Step 1/6: Extracting text...")
        text = processor.extract_text(str(file_path))
        
        if not text or len(text.strip()) < 50:
            print(f"⚠️  Warning: Extracted text is too short ({len(text)} chars)")
            return None
        
        print(f"   ✅ Extracted {len(text)} characters")
        
        # Extract contact information
        print("⏳ Step 2/6: Extracting contact information...")
        contact_info = processor.extract_contact_info(text)
        print(f"   ✅ Found: {len(contact_info['emails'])} emails, {len(contact_info['phones'])} phones")
        
        # Extract skills
        print("⏳ Step 3/6: Extracting technical skills...")
        skills_results = processor.extract_skills(text)
        print(f"   ✅ Identified {skills_results['total_skills']} skills")
        
        # Extract entities
        print("⏳ Step 4/6: Extracting named entities...")
        entity_results = processor.extract_entities(text)
        print(f"   ✅ Found {entity_results['total_entities']} entities")
        
        # Text statistics
        print("⏳ Step 5/6: Analyzing text statistics...")
        stats = processor.get_text_statistics(text)
        print(f"   ✅ Stats: {stats['word_count']} words, {stats['sentence_count']} sentences")
        
        # Sentiment analysis
        print("⏳ Step 6/6: Analyzing sentiment...")
        sentiment = processor.analyze_sentiment(text)
        print(f"   ✅ Sentiment: {sentiment['sentiment_label'].upper()}")
        
        # Compile results
        results = {
            'metadata': {
                'original_filename': file_path.name,
                'file_size_bytes': file_path.stat().st_size,
                'processed_at': datetime.now().isoformat(),
                'file_extension': file_path.suffix
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
        
        print("✅ Processing complete!\n")
        return results
        
    except Exception as e:
        print(f"❌ Error processing {file_path.name}: {str(e)}")
        import traceback
        traceback.print_exc()
        return None


def save_results(results, original_filename):
    """Save processing results to JSON and TXT files"""
    
    base_name = Path(original_filename).stem
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Save JSON
    json_filename = f"{base_name}_{timestamp}_results.json"
    json_path = RESULTS_FOLDER / json_filename
    
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    # Save TXT summary
    txt_filename = f"{base_name}_{timestamp}_summary.txt"
    txt_path = RESULTS_FOLDER / txt_filename
    
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write(f"RESUME PROCESSING SUMMARY\n")
        f.write(f"File: {original_filename}\n")
        f.write(f"Processed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 80 + "\n\n")
        
        f.write("CONTACT INFORMATION\n")
        f.write("-" * 80 + "\n")
        contact = results['contact_info']
        f.write(f"Emails: {', '.join(contact['emails']) if contact['emails'] else 'None found'}\n")
        f.write(f"Phones: {', '.join(contact['phones']) if contact['phones'] else 'None found'}\n")
        f.write(f"LinkedIn: {', '.join(contact['linkedin']) if contact['linkedin'] else 'None found'}\n")
        f.write(f"GitHub: {', '.join(contact['github']) if contact['github'] else 'None found'}\n\n")
        
        f.write("TECHNICAL SKILLS\n")
        f.write("-" * 80 + "\n")
        skills = results['skills']
        f.write(f"Total: {skills['total_skills']}\n")
        f.write(f"Skills: {', '.join(skills['skills'])}\n")
        f.write(f"Experience Years: {', '.join(map(str, skills['experience_years']))}\n\n")
        
        f.write("KEY STATISTICS\n")
        f.write("-" * 80 + "\n")
        stats = results['statistics']
        f.write(f"Words: {stats['word_count']:,}\n")
        f.write(f"Sentences: {stats['sentence_count']}\n")
        f.write(f"Unique Words: {stats['unique_words']:,}\n\n")
        
        f.write("SENTIMENT\n")
        f.write("-" * 80 + "\n")
        sentiment = results['sentiment']
        f.write(f"Sentiment: {sentiment['sentiment_label'].upper()}\n")
        f.write(f"Polarity: {sentiment['polarity']:.3f}\n")
        f.write(f"Subjectivity: {sentiment['subjectivity']:.3f}\n")
    
    return json_path, txt_path


def move_to_processed(file_path):
    """Move processed file to the 'process' folder"""
    
    destination = PROCESSED_FOLDER / file_path.name
    
    # If file already exists, add timestamp
    if destination.exists():
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        stem = file_path.stem
        suffix = file_path.suffix
        destination = PROCESSED_FOLDER / f"{stem}_{timestamp}{suffix}"
    
    shutil.move(str(file_path), str(destination))
    return destination


def process_all_resumes():
    """Main function to process all resumes in the input folder"""
    
    print("\n" + "=" * 80)
    print("AUTOMATED RESUME PROCESSING")
    print("=" * 80)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Setup folders
    setup_folders()
    
    # Find all resume files
    resume_files = []
    for ext in SUPPORTED_EXTENSIONS:
        resume_files.extend(list(INPUT_FOLDER.glob(f"*{ext}")))
    
    # Filter out files that are in subdirectories
    resume_files = [f for f in resume_files if f.parent == INPUT_FOLDER]
    
    if not resume_files:
        print("⚠️  No resume files found in the input folder")
        print(f"   Place PDF, DOCX, DOC, or TXT files in: {INPUT_FOLDER}")
        return
    
    print(f"📋 Found {len(resume_files)} resume file(s) to process:\n")
    for i, file_path in enumerate(resume_files, 1):
        print(f"   {i}. {file_path.name} ({file_path.stat().st_size:,} bytes)")
    print()
    
    # Process each file
    successful = 0
    failed = 0
    
    for file_path in resume_files:
        try:
            # Process the resume
            results = process_resume_file(file_path)
            
            if results:
                # Save results
                print("💾 Saving results...")
                json_path, txt_path = save_results(results, file_path.name)
                print(f"   ✅ JSON: {json_path.name}")
                print(f"   ✅ TXT: {txt_path.name}")
                
                # Move to processed folder
                print("📦 Moving to processed folder...")
                new_location = move_to_processed(file_path)
                print(f"   ✅ Moved to: {new_location.name}\n")
                
                successful += 1
            else:
                print(f"⚠️  Skipping {file_path.name} due to processing errors\n")
                failed += 1
                
        except Exception as e:
            print(f"❌ Failed to process {file_path.name}: {str(e)}\n")
            failed += 1
    
    # Summary
    print("\n" + "=" * 80)
    print("PROCESSING COMPLETE")
    print("=" * 80)
    print(f"✅ Successfully processed: {successful}")
    print(f"❌ Failed: {failed}")
    print(f"📊 Total: {len(resume_files)}")
    print(f"\n📂 Results saved to: {RESULTS_FOLDER}")
    print(f"📂 Processed files moved to: {PROCESSED_FOLDER}")
    print(f"\nCompleted at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80 + "\n")


if __name__ == '__main__':
    process_all_resumes()
