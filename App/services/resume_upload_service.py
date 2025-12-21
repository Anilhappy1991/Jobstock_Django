"""
Resume Upload Service
Handles multiple resume uploads with file validation and storage
"""
import os
from datetime import datetime
from typing import List, Dict, Any
from django.core.files.uploadedfile import UploadedFile
from django.conf import settings
from django.contrib.auth.models import User
from App.utils.response import ApiResponse
from App.models import ResumeProcessing
from App.services.resume_processing_service import ResumeProcessingService


class ResumeUploadService:
    """
    Service for handling resume uploads
    Supports: PDF, DOC, DOCX, TXT formats
    Storage: /Data/resume/YYYYMMDD/username_userID/
    Database: Stores relative path
    """
    
    # Allowed file extensions
    ALLOWED_EXTENSIONS = {'.pdf', '.doc', '.docx', '.txt'}
    
    # Max file size (10MB)
    MAX_FILE_SIZE = 10 * 1024 * 1024
    
    @classmethod
    def validate_file(cls, file: UploadedFile) -> Dict[str, Any]:
        """
        Validate uploaded file
        Returns: dict with 'valid' (bool) and 'error' (str if invalid)
        """
        # Check file exists
        if not file:
            return {'valid': False, 'error': 'No file provided'}
        
        # Get file extension
        file_ext = os.path.splitext(file.name)[1].lower()
        
        # Check extension
        if file_ext not in cls.ALLOWED_EXTENSIONS:
            return {
                'valid': False,
                'error': f'Invalid file type. Allowed: {", ".join(cls.ALLOWED_EXTENSIONS)}'
            }
        
        # Check file size
        if file.size > cls.MAX_FILE_SIZE:
            return {
                'valid': False,
                'error': f'File too large. Maximum size: {cls.MAX_FILE_SIZE / (1024*1024)}MB'
            }
        
        # Check if file is empty
        if file.size == 0:
            return {'valid': False, 'error': 'File is empty'}
        
        return {'valid': True, 'error': None}
    
    @classmethod
    def get_upload_path(cls, user: User) -> tuple:
        """
        Generate upload path: /Data/resume/YYYYMMDD/username_userID/
        Creates directory if it doesn't exist
        
        Returns:
            tuple: (absolute_path, relative_path)
        """
        # Get current date in YYYYMMDD format
        current_date = datetime.now().strftime('%Y%m%d')
        
        # Build folder name: username_userID
        folder_name = f"{user.username}_{user.id}"
        
        # Build relative path (for database storage) - use forward slashes
        relative_path = os.path.join(
            'Data',
            'resume',
            current_date,
            folder_name
        ).replace('\\', '/')
        
        # Build absolute path (for file system)
        absolute_path = os.path.join(settings.BASE_DIR, relative_path)
        
        # Create directory if it doesn't exist
        os.makedirs(absolute_path, exist_ok=True)
        
        return absolute_path, relative_path
    
    @classmethod
    def save_resume_file(cls, file: UploadedFile, user: User) -> Dict[str, Any]:
        """
        Save resume file to disk
        Returns: dict with 'success', 'file_path' (absolute), 'relative_path', 'error'
        """
        try:
            # Get upload directory (absolute and relative paths)
            absolute_dir, relative_dir = cls.get_upload_path(user)
            
            # Generate unique filename if file already exists
            filename = file.name
            absolute_file_path = os.path.join(absolute_dir, filename)
            
            # Handle duplicate filenames
            counter = 1
            base_name, ext = os.path.splitext(filename)
            while os.path.exists(absolute_file_path):
                filename = f"{base_name}_{counter}{ext}"
                absolute_file_path = os.path.join(absolute_dir, filename)
                counter += 1
            
            # Build relative path for database (use forward slashes)
            relative_file_path = os.path.join(relative_dir, filename).replace('\\', '/')
            
            # Save file
            with open(absolute_file_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            
            return {
                'success': True,
                'file_path': absolute_file_path,
                'relative_path': relative_file_path,
                'filename': filename,
                'error': None
            }
            
        except Exception as e:
            return {
                'success': False,
                'file_path': None,
                'relative_path': None,
                'filename': None,
                'error': str(e)
            }
    
    @classmethod
    def upload_resumes(cls, files: List[UploadedFile], user: User) -> ApiResponse:
        """
        Upload multiple resume files
        
        Args:
            files: List of uploaded files
            user: User uploading the resumes
            
        Returns:
            ApiResponse with upload results
        """
        if not files:
            return ApiResponse.error(
                message="No files provided",
                status_code=400
            )
        
        results = {
            'successful': [],
            'failed': [],
            'total': len(files),
            'success_count': 0,
            'failed_count': 0
        }
        
        for file in files:
            # Validate file
            validation = cls.validate_file(file)
            
            if not validation['valid']:
                results['failed'].append({
                    'filename': file.name,
                    'error': validation['error']
                })
                results['failed_count'] += 1
                continue
            
            # Save file to disk
            save_result = cls.save_resume_file(file, user)
            
            if not save_result['success']:
                results['failed'].append({
                    'filename': file.name,
                    'error': save_result['error']
                })
                results['failed_count'] += 1
                continue
            
            # Create database record
            try:
                file_ext = os.path.splitext(file.name)[1].lower()
                resume_record = ResumeProcessing.objects.create(
                    user=user,
                    profile=user.profile if hasattr(user, 'profile') else None,
                    resume_path=save_result['relative_path'],  # Store relative path
                    original_filename=save_result['filename'],
                    file_size=file.size,
                    file_extension=file_ext,
                    status='pending'
                )
                
                results['successful'].append({
                    'id': resume_record.id,
                    'filename': save_result['filename'],
                    'file_size': file.size,
                    'file_path': save_result['relative_path'],  # Return relative path
                    'status': 'pending'
                })
                results['success_count'] += 1
                
            except Exception as e:
                # File saved but database record failed
                results['failed'].append({
                    'filename': file.name,
                    'error': f'Database error: {str(e)}'
                })
                results['failed_count'] += 1
        
        # Determine overall success
        if results['success_count'] > 0:
            message = f"Uploaded {results['success_count']} of {results['total']} resumes successfully"
            return ApiResponse.success(
                data=results,
                message=message
            )
        else:
            return ApiResponse.error(
                message="All uploads failed",
                error_details=results,
                status_code=400
            )
    
    @classmethod
    def get_user_resumes(cls, user: User, limit: int = 50, offset: int = 0) -> ApiResponse:
        """
        Get all resumes uploaded by a user
        
        Args:
            user: User to get resumes for
            limit: Maximum number of resumes to return
            offset: Offset for pagination
            
        Returns:
            ApiResponse with resume list
        """
        try:
            resumes = ResumeProcessing.objects.filter(user=user).order_by('-created_at')
            total_count = resumes.count()
            
            # Apply pagination
            resumes = resumes[offset:offset + limit]
            
            resume_list = []
            for resume in resumes:
                resume_list.append({
                    'id': resume.id,
                    'filename': resume.original_filename,
                    'file_size': resume.file_size,
                    'file_extension': resume.file_extension,
                    'status': resume.status,
                    'created_at': resume.created_at.isoformat(),
                    'resume_path': resume.resume_path,
                    'error_message': resume.error_message if resume.status == 'failed' else None
                })
            
            return ApiResponse.success(
                data={
                    'resumes': resume_list,
                    'total': total_count,
                    'limit': limit,
                    'offset': offset
                },
                message=f"Retrieved {len(resume_list)} resumes"
            )
            
        except Exception as e:
            return ApiResponse.error(
                message="Failed to retrieve resumes",
                error=str(e),
                status_code=500
            )
    
    @classmethod
    def delete_resume(cls, resume_id: int, user: User) -> ApiResponse:
        """
        Delete a resume file and its database record
        
        Args:
            resume_id: ID of the resume to delete
            user: User requesting the deletion
            
        Returns:
            ApiResponse with deletion result
        """
        try:
            # Get resume record
            resume = ResumeProcessing.objects.get(id=resume_id, user=user)
            
            # Delete file from disk if it exists
            if os.path.exists(resume.resume_path):
                os.remove(resume.resume_path)
            
            # Delete database record
            filename = resume.original_filename
            resume.delete()
            
            return ApiResponse.success(
                message=f"Resume '{filename}' deleted successfully"
            )
            
        except ResumeProcessing.DoesNotExist:
            return ApiResponse.error(
                message="Resume not found",
                status_code=404
            )
        except Exception as e:
            return ApiResponse.error(
                message="Failed to delete resume",
                error=str(e),
                status_code=500
            )
    
    @classmethod
    def get_upload_statistics(cls, user: User) -> ApiResponse:
        """
        Get upload statistics for a user
        
        Returns:
            ApiResponse with statistics
        """
        try:
            resumes = ResumeProcessing.objects.filter(user=user)
            
            stats = {
                'total_uploads': resumes.count(),
                'pending': resumes.filter(status='pending').count(),
                'processing': resumes.filter(status='processing').count(),
                'completed': resumes.filter(status='completed').count(),
                'failed': resumes.filter(status='failed').count(),
                'total_size_mb': sum(r.file_size for r in resumes) / (1024 * 1024),
                'recent_uploads': []
            }
            
            # Get 5 most recent uploads
            recent = resumes.order_by('-created_at')[:5]
            for resume in recent:
                stats['recent_uploads'].append({
                    'filename': resume.original_filename,
                    'status': resume.status,
                    'created_at': resume.created_at.isoformat()
                })
            
            return ApiResponse.success(
                data=stats,
                message="Statistics retrieved successfully"
            )
            
        except Exception as e:
            return ApiResponse.error(
                message="Failed to retrieve statistics",
                error=str(e),
                status_code=500
            )
    
    @classmethod
    def process_pending_resumes(cls, user: User, resume_ids: List[int] = None) -> ApiResponse:
        """
        Process pending resumes for a user using ResumeProcessingService
        
        Args:
            user: User whose resumes to process
            resume_ids: Optional list of specific resume IDs to process
            
        Returns:
            ApiResponse with processing results
        """
        try:
            # Build query
            query = {'user': user, 'status': 'pending'}
            
            if resume_ids:
                query['id__in'] = resume_ids
            
            # Get resumes to process
            resumes = ResumeProcessing.objects.filter(**query)
            
            if not resumes.exists():
                return ApiResponse.success(
                    data={'total': 0, 'successful': 0, 'failed': 0},
                    message="No pending resumes to process"
                )
            
            # Use generic processing service
            processing_service = ResumeProcessingService()
            results = processing_service.process_multiple_resumes(
                resume_records=list(resumes),
                verbose=False
            )
            
            return ApiResponse.success(
                data=results,
                message=f"Processed {results['successful']} of {results['total']} resumes successfully"
            )
            
        except Exception as e:
            return ApiResponse.error(
                message="Failed to process resumes",
                error=str(e),
                status_code=500
            )
    
    @classmethod
    def process_single_resume(cls, resume_id: int, user: User) -> ApiResponse:
        """
        Process a single resume using ResumeProcessingService
        
        Args:
            resume_id: ID of the resume to process
            user: User who owns the resume
            
        Returns:
            ApiResponse with processing result
        """
        try:
            # Get resume record
            resume_record = ResumeProcessing.objects.get(id=resume_id, user=user)
            
            # Build absolute path from relative path
            absolute_path = os.path.join(settings.BASE_DIR, resume_record.resume_path)
            
            # Use generic processing service
            processing_service = ResumeProcessingService()
            result = processing_service.process_resume(
                file_path=absolute_path,
                user=user,
                resume_record_id=resume_id,
                profile=resume_record.profile
            )
            
            if result['success']:
                return ApiResponse.success(
                    data={
                        'resume_id': resume_id,
                        'filename': resume_record.original_filename,
                        'status': 'completed',
                        'extracted_data': result['extracted_data']['metadata']
                    },
                    message="Resume processed successfully"
                )
            else:
                return ApiResponse.error(
                    message="Resume processing failed",
                    error=result['error'],
                    status_code=400
                )
                
        except ResumeProcessing.DoesNotExist:
            return ApiResponse.error(
                message="Resume not found",
                status_code=404
            )
        except Exception as e:
            return ApiResponse.error(
                message="Failed to process resume",
                error=str(e),
                status_code=500
            )
