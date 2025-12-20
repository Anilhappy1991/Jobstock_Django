"""
Job Service Layer
Handles business logic for job operations
"""
from django.shortcuts import get_object_or_404
from django.db.models import Q
from App.models import Job, DropdownMaster, DropdownGroup


class JobService:
    """Service class for Job-related operations"""
    
    @staticmethod
    def get_all_jobs(user=None, filters=None):
        """
        Get all jobs, optionally filtered by user and other criteria
        
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
        Get a single job by ID
        
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
