"""
Job Management Service - Enhanced
Handles all job-related business logic with standardized responses
"""
from typing import Dict, Any, Optional, List
from django.db.models import Q
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from App.models import Job, DropdownMaster, DropdownGroup
from App.models_extended import JobApplication, SavedJob, CandidateProfile
from App.services.base_service import BaseService
from App.utils.response import ApiResponse
import logging

logger = logging.getLogger(__name__)


class JobService(BaseService):
    """Service for Job operations with standardized responses"""
    
    model = Job
    
    # Legacy methods for backward compatibility
    @staticmethod
    def get_all_jobs(user=None, filters=None):
        """
        LEGACY: Get all jobs (backward compatibility)
        For new code, use get_all_jobs_api() instead
        
        Args:
            user: User object to filter jobs by posted_by
            filters: Dict of filter criteria
            
        Returns:
            QuerySet of Job objects
        """
        queryset = Job.objects.select_related(
            'job_category', 'job_type', 'job_level',
            'experience_required', 'qualification_required',
            'gender_preference', 'total_openings', 'job_fee_type',
            'country', 'state_city', 'posted_by'
        ).all()
        
        if user:
            queryset = queryset.filter(posted_by=user)
        
        if filters:
            if filters.get('is_active') is not None:
                queryset = queryset.filter(is_active=filters['is_active'])
            if filters.get('job_category'):
                queryset = queryset.filter(job_category__value=filters['job_category'])
            if filters.get('job_type'):
                queryset = queryset.filter(job_type__value=filters['job_type'])
        
        return queryset.order_by('-created_at')
    
    @staticmethod
    def get_job_by_id(job_id, user=None):
        """
        LEGACY: Get a single job by ID (backward compatibility)
        For new code, use get_job_details() instead
        
        Args:
            job_id: Job ID
            user: Optional user to verify ownership
            
        Returns:
            Job object or raises 404
        """
        queryset = Job.objects.select_related(
            'job_category', 'job_type', 'job_level',
            'experience_required', 'qualification_required',
            'gender_preference', 'total_openings', 'job_fee_type',
            'country', 'state_city', 'posted_by'
        )
        
        if user:
            return get_object_or_404(queryset, id=job_id, posted_by=user)
        
        return get_object_or_404(queryset, id=job_id)
    
    @staticmethod
    def create_job(data, user):
        """
        Create a new job posting
        
        Args:
            data: Dictionary of job data
            user: User posting the job
            
        Returns:
            Created Job object
        """
        job = Job()
        JobService._populate_job_fields(job, data, user)
        job.save()
        return job
    
    @staticmethod
    def update_job(job_id, data, user):
        """
        Update an existing job
        
        Args:
            job_id: Job ID to update
            data: Dictionary of job data
            user: User updating the job
            
        Returns:
            Updated Job object
        """
        job = JobService.get_job_by_id(job_id, user)
        JobService._populate_job_fields(job, data, user)
        job.save()
        return job
    
    @staticmethod
    def delete_job(job_id, user):
        """
        Delete a job posting
        
        Args:
            job_id: Job ID to delete
            user: User deleting the job
            
        Returns:
            Boolean indicating success
        """
        job = JobService.get_job_by_id(job_id, user)
        job.delete()
        return True
    
    @staticmethod
    def _populate_job_fields(job, data, user):
        """
        Helper method to populate job fields from data dictionary
        
        Args:
            job: Job object to populate
            data: Dictionary of job data
            user: User posting/updating the job
        """
        # Basic fields
        job.title = data.get('job_title', '')
        job.job_summary = data.get('job_summary', '')
        job.responsibilities = data.get('responsibilities', '')
        job.qualifications = data.get('qualifications', '')
        
        # File upload
        if 'company_logo' in data and data['company_logo']:
            job.company_logo = data['company_logo']
        
        # Dropdown fields
        job.job_category = JobService._get_dropdown_item(data.get('job_category'))
        job.job_type = JobService._get_dropdown_item(data.get('job_type'))
        job.job_level = JobService._get_dropdown_item(data.get('job_level'))
        job.experience_required = JobService._get_dropdown_item(data.get('experience'))
        job.qualification_required = JobService._get_dropdown_item(data.get('qualification'))
        job.gender_preference = JobService._get_dropdown_item(data.get('gender'))
        job.total_openings = JobService._get_dropdown_item(data.get('total_openings'))
        job.job_fee_type = JobService._get_dropdown_item(data.get('job_fee_type'))
        job.country = JobService._get_dropdown_item(data.get('country'))
        job.state_city = JobService._get_dropdown_item(data.get('state_city'))
        
        # Salary
        min_sal = data.get('min_salary', '').replace('$', '').replace(',', '').strip()
        max_sal = data.get('max_salary', '').replace('$', '').replace(',', '').strip()
        job.min_salary = min_sal if min_sal else None
        job.max_salary = max_sal if max_sal else None
        
        # Dates
        start_date = data.get('start_date', '').strip()
        deadline = data.get('deadline', '').strip()
        job.start_date = start_date if start_date else None
        job.deadline = deadline if deadline else None
        
        # Other fields
        job.skills = data.get('skills', '')
        job.permanent_address = data.get('permanent_address', '')
        job.temporary_address = data.get('temporary_address', '')
        job.zip_code = data.get('zip_code', '')
        job.video_url = data.get('video_url', '')
        
        # Location coordinates
        lat = data.get('latitude', '').strip()
        lon = data.get('longitude', '').strip()
        job.latitude = lat if lat else None
        job.longitude = lon if lon else None
        
        # Set posted by and status
        job.posted_by = user
        job.is_active = data.get('is_active', True)
    
    @staticmethod
    def _get_dropdown_item(value):
        """
        Helper function to get dropdown item by value
        
        Args:
            value: Dropdown value
            
        Returns:
            DropdownMaster object or None
        """
        if value:
            try:
                return DropdownMaster.objects.get(value=value)
            except DropdownMaster.DoesNotExist:
                return None
        return None
    
    @staticmethod
    def get_dropdown_data():
        """
        Get all dropdown data for form population
        
        Returns:
            Dictionary of dropdown groups with their items
        """
        dropdown_groups = DropdownGroup.objects.filter(is_active=True).prefetch_related('items')
        
        dropdowns = {}
        for group in dropdown_groups:
            dropdowns[group.value] = group.items.filter(is_active=True).order_by('sort_order', 'text')
        
        return dropdowns
    
    @staticmethod
    def get_job_statistics(user=None):
        """
        Get job statistics for dashboard
        
        Args:
            user: User to filter statistics by
            
        Returns:
            Dictionary of statistics
        """
        queryset = Job.objects.all()
        
        if user:
            queryset = queryset.filter(posted_by=user)
        
        return {
            'total_jobs': queryset.count(),
            'active_jobs': queryset.filter(is_active=True).count(),
            'inactive_jobs': queryset.filter(is_active=False).count(),
        }
    
    # ========== NEW API-BASED METHODS WITH STANDARDIZED RESPONSES ==========
    
    @classmethod
    def get_all_jobs_api(cls, filters: Optional[Dict] = None, page: int = 1, 
                         page_size: int = 10) -> Dict[str, Any]:
        """
        Get all jobs with filtering and pagination (API standardized response)
        
        Args:
            filters: Dictionary of filter parameters
            page: Page number
            page_size: Items per page
            
        Returns:
            ApiResponse dict with jobs
        """
        try:
            queryset = Job.objects.filter(is_active=True).select_related(
                'job_category', 'job_type', 'job_level', 'posted_by'
            )
            
            # Apply filters
            if filters:
                if 'title' in filters:
                    queryset = queryset.filter(title__icontains=filters['title'])
                if 'job_category' in filters:
                    queryset = queryset.filter(job_category_id=filters['job_category'])
                if 'job_type' in filters:
                    queryset = queryset.filter(job_type_id=filters['job_type'])
                if 'location' in filters:
                    queryset = queryset.filter(
                        Q(permanent_address__icontains=filters['location']) |
                        Q(temporary_address__icontains=filters['location'])
                    )
                if 'min_salary' in filters:
                    queryset = queryset.filter(min_salary__gte=filters['min_salary'])
                if 'max_salary' in filters:
                    queryset = queryset.filter(max_salary__lte=filters['max_salary'])
                if 'posted_by' in filters:
                    queryset = queryset.filter(posted_by_id=filters['posted_by'])
            
            # Order by
            queryset = queryset.order_by('-created_at')
            
            # Paginate
            paginated_data = cls.paginate(queryset, page, page_size)
            
            return ApiResponse.success(
                data=paginated_data,
                message="Jobs retrieved successfully"
            )
        except Exception as e:
            logger.error(f"Error getting jobs: {str(e)}")
            return ApiResponse.server_error(
                message="Failed to retrieve jobs",
                error_details=str(e)
            )
    
    @classmethod
    def get_job_details_api(cls, job_id: int, user_id: Optional[int] = None) -> Dict[str, Any]:
        """
        Get detailed job information with standardized API response
        
        Args:
            job_id: Job ID
            user_id: Optional user ID to check if applied/saved
            
        Returns:
            ApiResponse dict with job details
        """
        try:
            job = Job.objects.select_related(
                'job_category', 'job_type', 'job_level', 'posted_by',
                'experience_required', 'qualification_required',
                'country', 'state_city'
            ).get(id=job_id)
            
            data = {
                'id': job.id,
                'title': job.title,
                'company_logo': job.company_logo.url if job.company_logo else None,
                'job_summary': job.job_summary,
                'responsibilities': job.responsibilities,
                'qualifications': job.qualifications,
                'job_category': job.job_category.text if job.job_category else None,
                'job_type': job.job_type.text if job.job_type else None,
                'job_level': job.job_level.text if job.job_level else None,
                'experience_required': job.experience_required.text if job.experience_required else None,
                'qualification_required': job.qualification_required.text if job.qualification_required else None,
                'min_salary': float(job.min_salary) if job.min_salary else None,
                'max_salary': float(job.max_salary) if job.max_salary else None,
                'start_date': job.start_date.isoformat() if job.start_date else None,
                'deadline': job.deadline.isoformat() if job.deadline else None,
                'skills': job.skills,
                'permanent_address': job.permanent_address,
                'country': job.country.text if job.country else None,
                'city': job.state_city.text if job.state_city else None,
                'slug': job.slug,
                'posted_by': {
                    'id': job.posted_by.id,
                    'username': job.posted_by.username,
                } if job.posted_by else None,
                'created_at': job.created_at.isoformat(),
            }
            
            # Check if user has applied or saved this job
            if user_id:
                try:
                    profile = User.objects.get(id=user_id).profile
                    if hasattr(profile, 'candidate_data'):
                        candidate = profile.candidate_data
                        data['has_applied'] = JobApplication.objects.filter(
                            candidate=candidate, job=job
                        ).exists()
                        data['has_saved'] = SavedJob.objects.filter(
                            candidate=candidate, job=job
                        ).exists()
                except Exception:
                    pass
            
            return ApiResponse.success(
                data=data,
                message="Job details retrieved successfully"
            )
        except Job.DoesNotExist:
            return ApiResponse.not_found(
                message=f"Job with ID {job_id} not found"
            )
        except Exception as e:
            logger.error(f"Error getting job details: {str(e)}")
            return ApiResponse.server_error(
                message="Failed to retrieve job details",
                error_details=str(e)
            )
    
    @classmethod
    def search_jobs_api(cls, search_query: str, filters: Optional[Dict] = None,
                        page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        """
        Search jobs with filters and standardized API response
        
        Args:
            search_query: Search text
            filters: Additional filters
            page: Page number
            page_size: Items per page
            
        Returns:
            ApiResponse dict with search results
        """
        try:
            queryset = Job.objects.filter(is_active=True)
            
            # Apply search
            if search_query:
                queryset = queryset.filter(
                    Q(title__icontains=search_query) |
                    Q(job_summary__icontains=search_query) |
                    Q(skills__icontains=search_query)
                )
            
            # Apply additional filters
            if filters:
                if 'job_category' in filters:
                    queryset = queryset.filter(job_category_id=filters['job_category'])
                if 'job_type' in filters:
                    queryset = queryset.filter(job_type_id=filters['job_type'])
                if 'location' in filters:
                    queryset = queryset.filter(
                        Q(permanent_address__icontains=filters['location']) |
                        Q(state_city__text__icontains=filters['location'])
                    )
            
            queryset = queryset.order_by('-created_at')
            paginated_data = cls.paginate(queryset, page, page_size)
            
            return ApiResponse.success(
                data=paginated_data,
                message="Search completed successfully"
            )
        except Exception as e:
            logger.error(f"Error searching jobs: {str(e)}")
            return ApiResponse.server_error(
                message="Failed to search jobs",
                error_details=str(e)
            )
    
    @classmethod
    def get_posted_jobs_for_rpo(cls, search: Optional[str] = None, 
                                filters: Optional[Dict] = None,
                                sort_by: str = '-created_at',
                                page: int = 1, 
                                page_size: int = 20) -> Dict[str, Any]:
        """
        Get all posted jobs for RPO Admin dashboard with search, filter, sort
        
        Args:
            search: Search query (title, company, skills)
            filters: Dictionary of filter parameters (job_type, job_category, is_active, posted_by, date_range)
            sort_by: Field to sort by (default: -created_at)
            page: Page number
            page_size: Items per page
            
        Returns:
            ApiResponse dict with job list data
        """
        try:
            # Base queryset with optimized select_related
            queryset = Job.objects.select_related(
                'job_category', 
                'job_type', 
                'job_level',
                'posted_by',
                'posted_by__profile',
                'country',
                'state_city'
            ).all()
            
            # Apply search
            if search:
                search = search.strip()
                queryset = queryset.filter(
                    Q(title__icontains=search) |
                    Q(job_summary__icontains=search) |
                    Q(skills__icontains=search) |
                    Q(posted_by__username__icontains=search) |
                    Q(posted_by__profile__full_name__icontains=search)
                )
            
            # Apply filters
            if filters:
                if 'job_type' in filters and filters['job_type']:
                    queryset = queryset.filter(job_type__value=filters['job_type'])
                
                if 'job_category' in filters and filters['job_category']:
                    queryset = queryset.filter(job_category__value=filters['job_category'])
                
                if 'is_active' in filters and filters['is_active'] is not None:
                    queryset = queryset.filter(is_active=filters['is_active'])
                
                if 'posted_by' in filters and filters['posted_by']:
                    queryset = queryset.filter(posted_by_id=filters['posted_by'])
                
                if 'date_from' in filters and filters['date_from']:
                    queryset = queryset.filter(created_at__gte=filters['date_from'])
                
                if 'date_to' in filters and filters['date_to']:
                    queryset = queryset.filter(created_at__lte=filters['date_to'])
            
            # Apply sorting
            valid_sort_fields = [
                'title', '-title', 
                'created_at', '-created_at',
                'deadline', '-deadline',
                'posted_by__username', '-posted_by__username'
            ]
            if sort_by in valid_sort_fields:
                queryset = queryset.order_by(sort_by)
            else:
                queryset = queryset.order_by('-created_at')  # Default
            
            # Get total count before pagination
            total_count = queryset.count()
            
            # Calculate pagination
            total_pages = (total_count + page_size - 1) // page_size if total_count > 0 else 1
            start = (page - 1) * page_size
            end = start + page_size
            
            # Get page items
            jobs_page = queryset[start:end]
            
            # Transform data for template/API
            jobs_list = []
            for job in jobs_page:
                jobs_list.append({
                    'id': job.id,
                    'title': job.title,
                    'slug': job.slug,
                    'job_category': job.job_category.text if job.job_category else 'N/A',
                    'job_type': job.job_type.text if job.job_type else 'N/A',
                    'job_level': job.job_level.text if job.job_level else 'N/A',
                    'company_name': job.posted_by.profile.full_name if job.posted_by and hasattr(job.posted_by, 'profile') and job.posted_by.profile.full_name else job.posted_by.username if job.posted_by else 'Unknown',
                    'posted_by': job.posted_by.username if job.posted_by else 'Unknown',
                    'posted_by_id': job.posted_by.id if job.posted_by else None,
                    'location': f"{job.state_city.text}, {job.country.text}" if job.state_city and job.country else (job.state_city.text if job.state_city else (job.country.text if job.country else 'N/A')),
                    'min_salary': float(job.min_salary) if job.min_salary else None,
                    'max_salary': float(job.max_salary) if job.max_salary else None,
                    'salary_display': f"${job.min_salary:,.0f} - ${job.max_salary:,.0f}" if job.min_salary and job.max_salary else ('Negotiable' if not job.min_salary and not job.max_salary else f"${job.min_salary:,.0f}+" if job.min_salary else f"Up to ${job.max_salary:,.0f}"),
                    'created_at': job.created_at,
                    'created_at_display': job.created_at.strftime('%Y-%m-%d %H:%M') if job.created_at else 'N/A',
                    'start_date': job.start_date.strftime('%Y-%m-%d') if job.start_date else 'N/A',
                    'deadline': job.deadline.strftime('%Y-%m-%d') if job.deadline else 'N/A',
                    'is_active': job.is_active,
                    'status_display': 'Active' if job.is_active else 'Inactive',
                    'status_class': 'badge-success' if job.is_active else 'badge-secondary',
                    'detail_url': f'/job-detail/{job.slug}/' if job.slug else '#',
                })
            
            # Prepare pagination data
            paginated_data = {
                'items': jobs_list,
                'total_count': total_count,
                'page': page,
                'page_size': page_size,
                'total_pages': total_pages,
                'has_next': page < total_pages,
                'has_previous': page > 1,
                'next_page': page + 1 if page < total_pages else None,
                'previous_page': page - 1 if page > 1 else None,
            }
            
            return ApiResponse.success(
                data=paginated_data,
                message=f"Found {total_count} job(s)"
            )
            
        except Exception as e:
            logger.error(f"Error getting posted jobs for RPO: {str(e)}")
            return ApiResponse.server_error(
                message="Failed to retrieve posted jobs",
                error_details=str(e)
            )
    
    @classmethod
    def get_job_statistics_api(cls, user_id: Optional[int] = None) -> Dict[str, Any]:
        """
        Get job statistics for dashboard with API standardized response
        
        Args:
            user_id: Optional user ID to filter statistics
            
        Returns:
            ApiResponse dict with statistics
        """
        try:
            queryset = Job.objects.all()
            
            if user_id:
                queryset = queryset.filter(posted_by_id=user_id)
            
            from django.utils import timezone
            from datetime import timedelta
            
            now = timezone.now()
            week_ago = now - timedelta(days=7)
            month_ago = now - timedelta(days=30)
            
            stats = {
                'total_jobs': queryset.count(),
                'active_jobs': queryset.filter(is_active=True).count(),
                'inactive_jobs': queryset.filter(is_active=False).count(),
                'jobs_this_week': queryset.filter(created_at__gte=week_ago).count(),
                'jobs_this_month': queryset.filter(created_at__gte=month_ago).count(),
                'jobs_with_deadline': queryset.filter(deadline__isnull=False).count(),
                'expired_jobs': queryset.filter(deadline__lt=now.date(), is_active=True).count(),
            }
            
            return ApiResponse.success(
                data=stats,
                message="Job statistics retrieved successfully"
            )
            
        except Exception as e:
            logger.error(f"Error getting job statistics: {str(e)}")
            return ApiResponse.server_error(
                message="Failed to retrieve job statistics",
                error_details=str(e)
            )
