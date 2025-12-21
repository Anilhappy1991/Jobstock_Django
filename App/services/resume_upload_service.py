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


class ResumeUploadService:
    """
    Service for handling resume uploads
    Supports: PDF, DOC, DOCX, TXT formats
    Storage: Data/resume/YYYYMMDD/username/
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
    def get_upload_path(cls, user: User) -> str:
        """
        Generate upload path: Data/resume/YYYYMMDD/username/
        Creates directory if it doesn't exist
        """
        # Get current date in YYYYMMDD format
        current_date = datetime.now().strftime('%Y%m%d')
        
        # Build path
        upload_dir = os.path.join(
            settings.BASE_DIR,
            'Data',
            'resume',
            current_date,
            user.username
        )
        
        # Create directory if it doesn't exist
        os.makedirs(upload_dir, exist_ok=True)
        
        return upload_dir
    
    @classmethod
    def save_resume_file(cls, file: UploadedFile, user: User) -> Dict[str, Any]:
        """
        Save resume file to disk
        Returns: dict with 'success', 'file_path', 'error'
        """
        try:
            # Get upload directory
            upload_dir = cls.get_upload_path(user)
            
            # Generate unique filename if file already exists
            filename = file.name
            file_path = os.path.join(upload_dir, filename)
            
            # Handle duplicate filenames
            counter = 1
            base_name, ext = os.path.splitext(filename)
            while os.path.exists(file_path):
                filename = f"{base_name}_{counter}{ext}"
                file_path = os.path.join(upload_dir, filename)
                counter += 1
            
            # Save file
            with open(file_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            
            return {
                'success': True,
                'file_path': file_path,
                'filename': filename,
                'error': None
            }
            
        except Exception as e:
            return {
                'success': False,
                'file_path': None,
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
                    resume_path=save_result['file_path'],
                    original_filename=save_result['filename'],
                    file_size=file.size,
                    file_extension=file_ext,
                    status='pending'
                )
                
                results['successful'].append({
                    'id': resume_record.id,
                    'filename': save_result['filename'],
                    'file_size': file.size,
                    'file_path': save_result['file_path'],
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
