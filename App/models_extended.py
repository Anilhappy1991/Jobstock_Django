"""
Enhanced Models for User Groups and Role Management
Provides separate models for Hiring Manager, Candidate, and RPO Admin
"""
from django.db import models
from django.contrib.auth.models import User, Group
from App.models import Profile, Job, DropdownMaster


class HiringManager(models.Model):
    """
    Hiring Manager specific data
    Extended information for users with Hiring Manager role
    """
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='hiring_manager_data')
    
    # Company Information
    company_name = models.CharField(max_length=255)
    company_website = models.URLField(max_length=500, blank=True, null=True)
    company_size = models.ForeignKey(
        DropdownMaster,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='company_size_managers',
        limit_choices_to={'group__value': 'company_size'}
    )
    industry = models.ForeignKey(
        DropdownMaster,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='industry_managers',
        limit_choices_to={'group__value': 'industry'}
    )
    
    # Department & Position
    department = models.CharField(max_length=255, blank=True, null=True)
    position = models.CharField(max_length=255, blank=True, null=True)
    employee_id = models.CharField(max_length=100, blank=True, null=True, unique=True)
    
    # Contact & Verification
    office_phone = models.CharField(max_length=30, blank=True, null=True)
    office_email = models.EmailField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    verification_date = models.DateTimeField(null=True, blank=True)
    
    # Hiring Permissions
    can_post_jobs = models.BooleanField(default=True)
    can_view_all_applications = models.BooleanField(default=True)
    can_shortlist_candidates = models.BooleanField(default=True)
    max_job_posts = models.IntegerField(default=10, help_text="Maximum number of active job posts")
    
    # Stats
    total_jobs_posted = models.IntegerField(default=0)
    total_hires_made = models.IntegerField(default=0)
    
    # Metadata
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.profile.user.username} - {self.company_name}"
    
    class Meta:
        db_table = 'hiring_manager'
        verbose_name = 'Hiring Manager'
        verbose_name_plural = 'Hiring Managers'
        permissions = (
            ("verify_hiring_manager", "Can verify hiring managers"),
            ("manage_job_posts", "Can manage job posts"),
        )


class CandidateProfile(models.Model):
    """
    Candidate specific data
    Extended information for job seekers
    """
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='candidate_data')
    
    # Career Information
    current_job_title = models.CharField(max_length=255, blank=True, null=True)
    current_company = models.CharField(max_length=255, blank=True, null=True)
    current_salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    expected_salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Job Preferences
    preferred_job_type = models.ForeignKey(
        DropdownMaster,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='preferred_type_candidates',
        limit_choices_to={'group__value': 'job_type'}
    )
    preferred_location = models.ForeignKey(
        DropdownMaster,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='preferred_location_candidates',
        limit_choices_to={'group__value': 'state_city'}
    )
    willing_to_relocate = models.BooleanField(default=False)
    
    # Professional Details
    total_experience_years = models.IntegerField(default=0)
    notice_period = models.ForeignKey(
        DropdownMaster,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='notice_period_candidates',
        limit_choices_to={'group__value': 'notice_period'}
    )
    
    # Resume & Portfolio
    resume_headline = models.CharField(max_length=500, blank=True, null=True)
    portfolio_url = models.URLField(max_length=500, blank=True, null=True)
    github_url = models.URLField(max_length=500, blank=True, null=True)
    
    # Job Search Status
    JOB_SEARCH_STATUS = (
        ('actively_looking', 'Actively Looking'),
        ('open_to_offers', 'Open to Offers'),
        ('not_looking', 'Not Looking'),
    )
    job_search_status = models.CharField(
        max_length=20,
        choices=JOB_SEARCH_STATUS,
        default='actively_looking'
    )
    
    # Stats
    total_applications = models.IntegerField(default=0)
    total_interviews = models.IntegerField(default=0)
    total_offers = models.IntegerField(default=0)
    
    # Visibility
    profile_visibility = models.BooleanField(
        default=True,
        help_text="Make profile visible to employers"
    )
    allow_contact = models.BooleanField(
        default=True,
        help_text="Allow employers to contact directly"
    )
    
    # Metadata
    last_active = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.profile.user.username} - Candidate"
    
    class Meta:
        db_table = 'candidate_profile'
        verbose_name = 'Candidate Profile'
        verbose_name_plural = 'Candidate Profiles'


class RPOAdmin(models.Model):
    """
    RPO (Recruitment Process Outsourcing) Admin
    Extended information for RPO administrators
    """
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='rpo_admin_data')
    
    # RPO Organization Details
    organization_name = models.CharField(max_length=255)
    organization_website = models.URLField(max_length=500, blank=True, null=True)
    license_number = models.CharField(max_length=100, blank=True, null=True, unique=True)
    
    # Contact Information
    office_address = models.CharField(max_length=500, blank=True, null=True)
    office_phone = models.CharField(max_length=30, blank=True, null=True)
    office_email = models.EmailField(blank=True, null=True)
    
    # Specialization
    specialization = models.ManyToManyField(
        DropdownMaster,
        related_name='rpo_specializations',
        limit_choices_to={'group__value': 'job_category'},
        blank=True
    )
    
    # Verification & Permissions
    is_verified = models.BooleanField(default=False)
    verification_date = models.DateTimeField(null=True, blank=True)
    
    # RPO Permissions
    can_manage_all_jobs = models.BooleanField(default=True)
    can_manage_candidates = models.BooleanField(default=True)
    can_generate_reports = models.BooleanField(default=True)
    can_manage_hiring_managers = models.BooleanField(default=True)
    
    # Statistics
    total_placements = models.IntegerField(default=0)
    total_clients = models.IntegerField(default=0)
    
    # Service Area
    service_countries = models.ManyToManyField(
        DropdownMaster,
        related_name='rpo_service_countries',
        limit_choices_to={'group__value': 'country'},
        blank=True
    )
    
    # Metadata
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.profile.user.username} - {self.organization_name}"
    
    class Meta:
        db_table = 'rpo_admin'
        verbose_name = 'RPO Admin'
        verbose_name_plural = 'RPO Admins'
        permissions = (
            ("verify_rpo_admin", "Can verify RPO administrators"),
            ("manage_platform_users", "Can manage all platform users"),
            ("generate_analytics", "Can generate platform analytics"),
        )


class JobApplication(models.Model):
    """
    Job Application tracking
    Links Candidate to Jobs they applied for
    """
    candidate = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE, related_name='applications')
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    
    # Application Details
    cover_letter = models.TextField(blank=True, null=True)
    resume = models.FileField(upload_to='application_resumes/', blank=True, null=True)
    
    # Status Tracking
    STATUS_CHOICES = (
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('shortlisted', 'Shortlisted'),
        ('interview_scheduled', 'Interview Scheduled'),
        ('interview_completed', 'Interview Completed'),
        ('offered', 'Offered'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('withdrawn', 'Withdrawn'),
    )
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='submitted')
    
    # Interview Details
    interview_date = models.DateTimeField(null=True, blank=True)
    interview_location = models.CharField(max_length=500, blank=True, null=True)
    interview_notes = models.TextField(blank=True, null=True)
    
    # Ratings & Feedback
    recruiter_rating = models.IntegerField(
        null=True,
        blank=True,
        help_text="Rating from 1-5"
    )
    recruiter_notes = models.TextField(blank=True, null=True)
    
    # Assignment
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_applications'
    )
    
    # Metadata
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.candidate.profile.user.username} -> {self.job.title}"
    
    class Meta:
        db_table = 'job_applications'
        verbose_name = 'Job Application'
        verbose_name_plural = 'Job Applications'
        unique_together = ['candidate', 'job']
        ordering = ['-applied_at']


class ApplicationStatusHistory(models.Model):
    """
    Track status changes for job applications
    """
    application = models.ForeignKey(
        JobApplication,
        on_delete=models.CASCADE,
        related_name='status_history'
    )
    status = models.CharField(max_length=30)
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.application.id} - {self.status} - {self.created_at}"
    
    class Meta:
        db_table = 'application_status_history'
        verbose_name = 'Application Status History'
        verbose_name_plural = 'Application Status Histories'
        ordering = ['-created_at']


class SavedJob(models.Model):
    """
    Candidates can save jobs for later
    """
    candidate = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE, related_name='saved_jobs')
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='saved_by')
    saved_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.candidate.profile.user.username} saved {self.job.title}"
    
    class Meta:
        db_table = 'saved_jobs'
        verbose_name = 'Saved Job'
        verbose_name_plural = 'Saved Jobs'
        unique_together = ['candidate', 'job']
        ordering = ['-saved_at']


class Notification(models.Model):
    """
    User notifications system
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    
    NOTIFICATION_TYPES = (
        ('application', 'Job Application'),
        ('interview', 'Interview'),
        ('status_change', 'Status Change'),
        ('new_job', 'New Job Posted'),
        ('message', 'Message'),
        ('system', 'System'),
    )
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    
    title = models.CharField(max_length=255)
    message = models.TextField()
    link = models.URLField(max_length=500, blank=True, null=True)
    
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"
    
    class Meta:
        db_table = 'notifications'
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        ordering = ['-created_at']
