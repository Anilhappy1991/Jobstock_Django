"""
Job Application Management Service
Handles job application business logic
"""
from typing import Dict, Any, Optional
from django.db import transaction
from django.contrib.auth.models import User
from App.models import Job
from App.models_extended import JobApplication, CandidateProfile, ApplicationStatusHistory, SavedJob
from App.services.base_service import BaseService
from App.utils.response import ApiResponse
import logging

logger = logging.getLogger(__name__)


class ApplicationService(BaseService):
    """Service for Job Application operations"""
    
    model = JobApplication
    
    @classmethod
    @transaction.atomic
    def apply_for_job(cls, user_id: int, job_id: int, cover_letter: str = '',
                      resume=None) -> Dict[str, Any]:
        """
        Apply for a job
        
        Args:
            user_id: User applying for the job
            job_id: Job to apply for
            cover_letter: Optional cover letter
            resume: Optional resume file
            
        Returns:
            ApiResponse dict
        """
        try:
            # Get user and check if candidate
            user = User.objects.get(id=user_id)
            profile = user.profile
            
            if profile.role != 'candidate':
                return ApiResponse.forbidden(
                    message="Only candidates can apply for jobs"
                )
            
            # Get candidate profile
            if not hasattr(profile, 'candidate_data'):
                return ApiResponse.error(
                    message="Candidate profile not found",
                    status_code=404
                )
            
            candidate = profile.candidate_data
            
            # Get job
            job = Job.objects.get(id=job_id)
            
            if not job.is_active:
                return ApiResponse.error(
                    message="This job is no longer active"
                )
            
            # Check if already applied
            if JobApplication.objects.filter(candidate=candidate, job=job).exists():
                return ApiResponse.validation_error(
                    errors={'job': 'You have already applied for this job'},
                    message="Already applied"
                )
            
            # Create application
            application = JobApplication.objects.create(
                candidate=candidate,
                job=job,
                cover_letter=cover_letter,
                resume=resume,
                status='submitted'
            )
            
            # Update candidate stats
            candidate.total_applications += 1
            candidate.save()
            
            # Create status history
            ApplicationStatusHistory.objects.create(
                application=application,
                status='submitted',
                changed_by=user,
                notes="Application submitted"
            )
            
            return ApiResponse.created(
                data={'application_id': application.id},
                message="Application submitted successfully"
            )
            
        except User.DoesNotExist:
            return ApiResponse.not_found(message="User not found")
        except Job.DoesNotExist:
            return ApiResponse.not_found(message="Job not found")
        except Exception as e:
            logger.error(f"Error applying for job: {str(e)}")
            return ApiResponse.server_error(
                message="Failed to submit application",
                error_details=str(e)
            )
    
    @classmethod
    def get_candidate_applications(cls, user_id: int, page: int = 1, 
                                   page_size: int = 10) -> Dict[str, Any]:
        """Get all applications for a candidate"""
        try:
            user = User.objects.get(id=user_id)
            candidate = user.profile.candidate_data
            
            queryset = JobApplication.objects.filter(
                candidate=candidate
            ).select_related('job').order_by('-applied_at')
            
            paginated_data = cls.paginate(queryset, page, page_size)
            
            return ApiResponse.success(
                data=paginated_data,
                message="Applications retrieved successfully"
            )
        except Exception as e:
            logger.error(f"Error getting applications: {str(e)}")
            return ApiResponse.server_error(
                message="Failed to retrieve applications",
                error_details=str(e)
            )
    
    @classmethod
    def get_job_applications(cls, job_id: int, user_id: int,
                            page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        """Get all applications for a specific job"""
        try:
            # Check permissions
            user = User.objects.get(id=user_id)
            profile = user.profile
            
            if profile.role not in ['hiring_manager', 'rpo_admin']:
                return ApiResponse.forbidden(
                    message="Only hiring managers and RPO admins can view applications"
                )
            
            job = Job.objects.get(id=job_id)
            
            # Check if hiring manager owns this job
            if profile.role == 'hiring_manager' and job.posted_by_id != user_id:
                return ApiResponse.forbidden(
                    message="You don't have permission to view these applications"
                )
            
            queryset = JobApplication.objects.filter(
                job=job
            ).select_related('candidate__profile__user').order_by('-applied_at')
            
            paginated_data = cls.paginate(queryset, page, page_size)
            
            return ApiResponse.success(
                data=paginated_data,
                message="Applications retrieved successfully"
            )
        except Exception as e:
            logger.error(f"Error getting job applications: {str(e)}")
            return ApiResponse.server_error(
                message="Failed to retrieve applications",
                error_details=str(e)
            )
    
    @classmethod
    @transaction.atomic
    def update_application_status(cls, application_id: int, user_id: int,
                                  new_status: str, notes: str = '') -> Dict[str, Any]:
        """Update application status"""
        try:
            user = User.objects.get(id=user_id)
            profile = user.profile
            
            if profile.role not in ['hiring_manager', 'rpo_admin']:
                return ApiResponse.forbidden(
                    message="Only hiring managers and RPO admins can update application status"
                )
            
            application = JobApplication.objects.get(id=application_id)
            
            # Check if hiring manager owns the job
            if profile.role == 'hiring_manager' and application.job.posted_by_id != user_id:
                return ApiResponse.forbidden(
                    message="You don't have permission to update this application"
                )
            
            # Update status
            old_status = application.status
            application.status = new_status
            application.save()
            
            # Create status history
            ApplicationStatusHistory.objects.create(
                application=application,
                status=new_status,
                changed_by=user,
                notes=notes or f"Status changed from {old_status} to {new_status}"
            )
            
            return ApiResponse.success(
                data={'application_id': application.id, 'new_status': new_status},
                message="Application status updated successfully"
            )
        except Exception as e:
            logger.error(f"Error updating application status: {str(e)}")
            return ApiResponse.server_error(
                message="Failed to update application status",
                error_details=str(e)
            )
    
    @classmethod
    @transaction.atomic
    def save_job(cls, user_id: int, job_id: int, notes: str = '') -> Dict[str, Any]:
        """Save a job for later"""
        try:
            user = User.objects.get(id=user_id)
            candidate = user.profile.candidate_data
            job = Job.objects.get(id=job_id)
            
            # Check if already saved
            if SavedJob.objects.filter(candidate=candidate, job=job).exists():
                return ApiResponse.validation_error(
                    errors={'job': 'Job already saved'},
                    message="Job already in saved list"
                )
            
            saved_job = SavedJob.objects.create(
                candidate=candidate,
                job=job,
                notes=notes
            )
            
            return ApiResponse.created(
                data={'saved_job_id': saved_job.id},
                message="Job saved successfully"
            )
        except Exception as e:
            logger.error(f"Error saving job: {str(e)}")
            return ApiResponse.server_error(
                message="Failed to save job",
                error_details=str(e)
            )
    
    @classmethod
    def get_saved_jobs(cls, user_id: int, page: int = 1, 
                      page_size: int = 10) -> Dict[str, Any]:
        """Get all saved jobs for a candidate"""
        try:
            user = User.objects.get(id=user_id)
            candidate = user.profile.candidate_data
            
            queryset = SavedJob.objects.filter(
                candidate=candidate
            ).select_related('job').order_by('-saved_at')
            
            paginated_data = cls.paginate(queryset, page, page_size)
            
            return ApiResponse.success(
                data=paginated_data,
                message="Saved jobs retrieved successfully"
            )
        except Exception as e:
            logger.error(f"Error getting saved jobs: {str(e)}")
            return ApiResponse.server_error(
                message="Failed to retrieve saved jobs",
                error_details=str(e)
            )
