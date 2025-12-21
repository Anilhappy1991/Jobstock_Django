"""
Generic Resume Processing Service
Handles resume extraction, analysis, and database storage
Reusable by REST API, Django views, and background tasks
"""
import os
from typing import Dict, Any, Optional
from pathlib import Path
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.models import User

from App.models import ResumeProcessing, Profile
from App.tasks_simple import SimpleDocumentProcessor


class ResumeProcessingService:
    """
    Generic service for processing resumes with data extraction
    
    Features:
    - Text extraction from PDF, DOCX, DOC, TXT
    - Contact information extraction (email, phone)
    - Skills identification
    - Named entity recognition
    - Sentiment analysis
    - Database persistence
    
    Usage:
        service = ResumeProcessingService()
        result = service.process_resume(
            file_path='/path/to/resume.pdf',
            user=user_instance,
            resume_record_id=123
        )
    """
    
    def __init__(self):
        """Initialize the processor"""
        self.processor = SimpleDocumentProcessor()
    
    @classmethod
    def create_resume_record(cls, 
                            user: User, 
                            file_path: str,
                            original_filename: str,
                            file_size: int,
                            file_extension: str,
                            profile: Optional[Profile] = None) -> ResumeProcessing:
        """
        Create a ResumeProcessing database record
        
        Args:
            user: User who uploaded the resume
            file_path: Relative path to the resume file
            original_filename: Original name of the uploaded file
            file_size: Size of the file in bytes
            file_extension: File extension (e.g., '.pdf', '.docx')
            profile: Optional Profile instance to associate
            
        Returns:
            ResumeProcessing instance
        """
        resume_record = ResumeProcessing.objects.create(
            user=user,
            profile=profile,
            resume_path=file_path,
            original_filename=original_filename,
            file_size=file_size,
            file_extension=file_extension,
            status='pending'
        )
        return resume_record
    
    def extract_resume_data(self, file_path: str) -> Dict[str, Any]:
        """
        Extract all data from resume file
        
        Args:
            file_path: Absolute path to the resume file
            
        Returns:
            Dictionary with extracted data:
            {
                'text': str,
                'contact_info': dict,
                'skills': dict,
                'entities': dict,
                'statistics': dict,
                'sentiment': dict,
                'metadata': dict
            }
            
        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If text extraction fails or text is too short
            Exception: Other processing errors with detailed context
        """
        file_path_obj = Path(file_path)
        
        # Validate file exists
        if not file_path_obj.exists():
            raise FileNotFoundError(f"Resume file not found at path: {file_path}")
        
        # Check file is readable
        if not os.access(file_path, os.R_OK):
            raise PermissionError(f"Resume file is not readable: {file_path}")
        
        # Check file size
        file_size = file_path_obj.stat().st_size
        if file_size == 0:
            raise ValueError(f"Resume file is empty (0 bytes): {file_path}")
        
        # Extract text with error handling
        try:
            text = self.processor.extract_text(str(file_path))
        except Exception as e:
            raise ValueError(f"Text extraction failed for {file_path_obj.suffix} file: {str(e)}")
        
        # Validate text extraction
        if not text:
            raise ValueError(f"No text extracted from resume file: {file_path}")
        
        if len(text.strip()) < 50:
            raise ValueError(f"Extracted text is too short ({len(text)} characters, minimum 50 required). File may be corrupted or empty.")
        
        # Extract contact information
        try:
            contact_info = self.processor.extract_contact_info(text)
        except Exception as e:
            raise ValueError(f"Contact information extraction failed: {str(e)}")
        
        # Extract skills
        try:
            skills_results = self.processor.extract_skills(text)
        except Exception as e:
            raise ValueError(f"Skills extraction failed: {str(e)}")
        
        # Extract entities
        try:
            entity_results = self.processor.extract_entities(text)
        except Exception as e:
            raise ValueError(f"Entity extraction failed: {str(e)}")
        
        # Get text statistics
        try:
            stats = self.processor.get_text_statistics(text)
        except Exception as e:
            raise ValueError(f"Text statistics calculation failed: {str(e)}")
        
        # Analyze sentiment
        try:
            sentiment = self.processor.analyze_sentiment(text)
        except Exception as e:
            raise ValueError(f"Sentiment analysis failed: {str(e)}")
        
        # Compile results
        return {
            'text': text,
            'contact_info': contact_info,
            'skills': skills_results,
            'entities': entity_results,
            'statistics': stats,
            'sentiment': sentiment,
            'metadata': {
                'original_filename': file_path_obj.name,
                'file_size_bytes': file_size,
                'processed_at': datetime.now().isoformat(),
                'file_extension': file_path_obj.suffix,
                'word_count': stats['word_count'],
                'total_skills': skills_results['total_skills'],
                'total_entities': entity_results['total_entities']
            }
        }
    
    def update_resume_record(self, 
                            resume_record: ResumeProcessing, 
                            extracted_data: Dict[str, Any]) -> ResumeProcessing:
        """
        Update ResumeProcessing record with extracted data
        
        Args:
            resume_record: ResumeProcessing instance to update
            extracted_data: Dictionary from extract_resume_data()
            
        Returns:
            Updated ResumeProcessing instance
        """
        # Compile full JSON results
        results = {
            'contact_info': extracted_data['contact_info'],
            'skills': extracted_data['skills'],
            'entities': extracted_data['entities'],
            'statistics': extracted_data['statistics'],
            'sentiment': extracted_data['sentiment'],
            'metadata': extracted_data['metadata']
        }
        
        # Update fields
        resume_record.resume_text = extracted_data['text']
        resume_record.resume_json = results
        
        # Extract specific fields for quick access
        resume_record.extracted_skills = ', '.join(
            extracted_data['skills']['skills'][:30]  # Limit to 30 skills
        )
        
        resume_record.extracted_email = (
            extracted_data['contact_info']['emails'][0] 
            if extracted_data['contact_info']['emails'] 
            else None
        )
        
        resume_record.extracted_phone = (
            extracted_data['contact_info']['phones'][0] 
            if extracted_data['contact_info']['phones'] 
            else None
        )
        
        resume_record.years_of_experience = ', '.join(
            map(str, extracted_data['skills']['experience_years'][:3])
        )
        
        resume_record.sentiment_score = extracted_data['sentiment']['polarity']
        resume_record.word_count = extracted_data['statistics']['word_count']
        resume_record.status = 'completed'
        resume_record.processing_completed_at = timezone.now()
        
        resume_record.save()
        return resume_record
    
    def process_resume(self,
                      file_path: str,
                      user: User,
                      resume_record_id: Optional[int] = None,
                      profile: Optional[Profile] = None) -> Dict[str, Any]:
        """
        Complete resume processing workflow
        
        Args:
            file_path: Absolute path to the resume file
            user: User instance who owns the resume
            resume_record_id: Optional existing ResumeProcessing ID
            profile: Optional Profile instance to associate
            
        Returns:
            Dictionary with:
            {
                'success': bool,
                'resume_record': ResumeProcessing instance,
                'extracted_data': dict,
                'error': str (if failed)
            }
        """
        resume_record = None
        
        try:
            # Get or create resume record
            if resume_record_id:
                resume_record = ResumeProcessing.objects.get(id=resume_record_id)
            
            # Update status to processing
            if resume_record:
                resume_record.status = 'processing'
                resume_record.processing_started_at = timezone.now()
                resume_record.save()
            
            # Extract data from resume
            extracted_data = self.extract_resume_data(file_path)
            
            # Update database record
            if resume_record:
                resume_record = self.update_resume_record(resume_record, extracted_data)
            
            return {
                'success': True,
                'resume_record': resume_record,
                'extracted_data': extracted_data,
                'error': None
            }
            
        except Exception as e:
            import traceback
            import sys
            
            error_msg = str(e)
            error_type = type(e).__name__
            
            # Capture detailed error information
            error_details = {
                'error_type': error_type,
                'error_message': error_msg,
                'traceback': traceback.format_exc(),
                'file_path': file_path,
                'timestamp': datetime.now().isoformat(),
                'python_version': sys.version,
            }
            
            # Add file-specific information if available
            try:
                from pathlib import Path
                file_obj = Path(file_path)
                if file_obj.exists():
                    error_details['file_info'] = {
                        'exists': True,
                        'size': file_obj.stat().st_size,
                        'extension': file_obj.suffix,
                        'is_readable': os.access(file_path, os.R_OK)
                    }
                else:
                    error_details['file_info'] = {
                        'exists': False,
                        'error': 'File not found'
                    }
            except Exception as file_error:
                error_details['file_info'] = {
                    'error': str(file_error)
                }
            
            # Update record as failed if exists
            if resume_record:
                resume_record.status = 'failed'
                resume_record.error_message = error_msg
                resume_record.error_details = error_details
                resume_record.processing_completed_at = timezone.now()
                resume_record.save()
            
            return {
                'success': False,
                'resume_record': resume_record,
                'extracted_data': None,
                'error': error_msg,
                'error_details': error_details
            }
    
    def process_multiple_resumes(self,
                                resume_records: list,
                                verbose: bool = False) -> Dict[str, Any]:
        """
        Process multiple resumes in batch
        
        Args:
            resume_records: List of ResumeProcessing instances
            verbose: If True, print progress messages
            
        Returns:
            Dictionary with:
            {
                'total': int,
                'successful': int,
                'failed': int,
                'results': list of individual results
            }
        """
        results = []
        successful = 0
        failed = 0
        
        for resume_record in resume_records:
            if verbose:
                print(f"Processing: {resume_record.original_filename}")
            
            # Build absolute path from relative path
            from django.conf import settings
            import os
            absolute_path = os.path.join(settings.BASE_DIR, resume_record.resume_path)
            
            result = self.process_resume(
                file_path=absolute_path,
                user=resume_record.user,
                resume_record_id=resume_record.id,
                profile=resume_record.profile
            )
            
            if result['success']:
                successful += 1
                if verbose:
                    print(f"  ✅ Success")
            else:
                failed += 1
                if verbose:
                    print(f"  ❌ Failed: {result['error']}")
            
            results.append(result)
        
        return {
            'total': len(resume_records),
            'successful': successful,
            'failed': failed,
            'results': results
        }
