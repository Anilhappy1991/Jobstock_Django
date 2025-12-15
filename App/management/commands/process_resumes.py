"""
Django Management Command: Process Pending Resumes
Usage: python manage.py process_resumes
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from App.models import ResumeProcessing
from App.tasks_simple import SimpleDocumentProcessor
from pathlib import Path


class Command(BaseCommand):
    help = 'Process all pending resume uploads'

    def add_arguments(self, parser):
        parser.add_argument(
            '--all',
            action='store_true',
            help='Process all resumes including already processed ones',
        )
        parser.add_argument(
            '--user',
            type=str,
            help='Process resumes for a specific username',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('=' * 80))
        self.stdout.write(self.style.SUCCESS('PROCESSING PENDING RESUMES'))
        self.stdout.write(self.style.SUCCESS('=' * 80))
        self.stdout.write('')

        # Build query
        query = {}
        if not options['all']:
            query['status'] = 'pending'
        
        if options['user']:
            query['user__username'] = options['user']
            self.stdout.write(f"Filtering by user: {options['user']}")

        # Get resumes to process
        resumes = ResumeProcessing.objects.filter(**query).order_by('created_at')
        
        if not resumes.exists():
            self.stdout.write(self.style.WARNING('No pending resumes found.'))
            return

        self.stdout.write(f"Found {resumes.count()} resume(s) to process.\n")

        processor = SimpleDocumentProcessor()
        processed_count = 0
        failed_count = 0

        for resume_record in resumes:
            self.stdout.write('-' * 80)
            self.stdout.write(f"Processing: {resume_record.original_filename}")
            self.stdout.write(f"User: {resume_record.user.username}")
            self.stdout.write(f"Status: {resume_record.status}")

            try:
                # Check if file exists
                file_path = Path(resume_record.resume_path)
                if not file_path.exists():
                    raise FileNotFoundError(f"Resume file not found: {resume_record.resume_path}")

                # Update status to processing
                resume_record.status = 'processing'
                resume_record.processing_started_at = timezone.now()
                resume_record.save()

                # Extract text
                text = processor.extract_text(str(file_path))
                if not text or len(text.strip()) < 50:
                    raise ValueError(f"Extracted text is too short ({len(text)} chars)")

                # Extract all information
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
                resume_record.processing_completed_at = timezone.now()
                resume_record.save()

                self.stdout.write(self.style.SUCCESS(f"✅ Successfully processed!"))
                self.stdout.write(f"   Skills: {skills_results['total_skills']}")
                self.stdout.write(f"   Words: {stats['word_count']}")
                self.stdout.write(f"   Sentiment: {sentiment['sentiment_label']}")
                processed_count += 1

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"❌ Error: {str(e)}"))
                resume_record.status = 'failed'
                resume_record.error_message = str(e)
                resume_record.processing_completed_at = timezone.now()
                resume_record.save()
                failed_count += 1

            self.stdout.write('')

        # Summary
        self.stdout.write('=' * 80)
        self.stdout.write(self.style.SUCCESS('PROCESSING COMPLETE'))
        self.stdout.write('=' * 80)
        self.stdout.write(f"✅ Successfully processed: {processed_count}")
        self.stdout.write(f"❌ Failed: {failed_count}")
        self.stdout.write(f"📊 Total: {resumes.count()}")
        self.stdout.write('')
