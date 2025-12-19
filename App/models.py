from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import os

# Create your models here.

def validate_resume_file(file):
    """Validate resume file type and size"""
    # Maximum file size: 5MB
    max_size = 5 * 1024 * 1024  # 5MB in bytes
    
    # Allowed file extensions
    allowed_extensions = ['.pdf', '.doc', '.docx', '.txt']
    
    # Check file size
    if file.size > max_size:
        raise ValidationError(f'Resume file size cannot exceed 5MB. Current size: {file.size / (1024*1024):.2f}MB')
    
    # Check file extension
    ext = os.path.splitext(file.name)[1].lower()
    if ext not in allowed_extensions:
        raise ValidationError(f'Unsupported file type. Allowed types: PDF, DOC, DOCX, TXT')
    
    return file

class Blog(models.Model):
    id = models.AutoField(primary_key=True)
    img = models.ImageField(upload_to='blog_images/')
    title = models.CharField(max_length=255)
    date = models.DateField(auto_now_add=True)
    slug = models.SlugField(unique=True)  # Add a slug field
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)  # Automatically generate the slug from the title
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Candidate(models.Model):
    id = models.AutoField(primary_key=True)
    img = models.ImageField(upload_to='candidate_images/')
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)  # Add a slug field
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)  # Automatically generate the slug from the title
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Employer(models.Model):
    id = models.AutoField(primary_key=True)
    img = models.ImageField(upload_to='employer_images/')
    title = models.CharField(max_length=255)
    open = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)  # Add a slug field
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)  # Automatically generate the slug from the title
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


WORK_STATUS_CHOICES = (
    ('findjob', "I'm looking for a job"),
    ('findtalent', "I'm looking for talent"),
)


class DropdownGroup(models.Model):
    """
    Group table for dropdown categories
    e.g., Education, Experience, Country, City
    """
    id = models.AutoField(primary_key=True)
    text = models.CharField(max_length=100, unique=True)
    value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.text
    
    class Meta:
        db_table = 'dropdown_group'
        verbose_name = 'Dropdown Group'
        verbose_name_plural = 'Dropdown Groups'


class DropdownMaster(models.Model):
    """
    Master table for dropdown values
    e.g., High School, Bachelor's Degree (for Education group)
    """
    id = models.AutoField(primary_key=True)
    group = models.ForeignKey(DropdownGroup, on_delete=models.CASCADE, related_name='items')
    text = models.CharField(max_length=200)
    value = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    sort_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.group.text} - {self.text}"
    
    class Meta:
        db_table = 'dropdown_master'
        verbose_name = 'Dropdown Master'
        verbose_name_plural = 'Dropdown Masters'
        ordering = ['group', 'sort_order', 'text']


class Job(models.Model):
    id = models.AutoField(primary_key=True)
    
    # Basic Information
    title = models.CharField(max_length=255, verbose_name='Job Title')
    company_logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    job_summary = models.TextField(blank=True, null=True)
    responsibilities = models.TextField(blank=True, null=True)
    qualifications = models.TextField(blank=True, null=True)
    
    # Job Details
    job_category = models.ForeignKey(
        DropdownMaster, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='category_jobs',
        limit_choices_to={'group__value': 'job_category'}
    )
    job_type = models.ForeignKey(
        DropdownMaster, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='type_jobs',
        limit_choices_to={'group__value': 'job_type'}
    )
    job_level = models.ForeignKey(
        DropdownMaster, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='level_jobs',
        limit_choices_to={'group__value': 'job_level'}
    )
    experience_required = models.ForeignKey(
        DropdownMaster, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='experience_jobs',
        limit_choices_to={'group__value': 'experience'}
    )
    qualification_required = models.ForeignKey(
        DropdownMaster, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='qualification_jobs',
        limit_choices_to={'group__value': 'qualification'}
    )
    gender_preference = models.ForeignKey(
        DropdownMaster, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='gender_jobs',
        limit_choices_to={'group__value': 'gender'}
    )
    
    # Salary Information
    min_salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    max_salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    
    # Dates
    start_date = models.DateField(blank=True, null=True)
    deadline = models.DateField(blank=True, null=True)
    
    # Additional Details
    total_openings = models.ForeignKey(
        DropdownMaster, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='openings_jobs',
        limit_choices_to={'group__value': 'total_openings'}
    )
    job_fee_type = models.ForeignKey(
        DropdownMaster, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='feetype_jobs',
        limit_choices_to={'group__value': 'job_fee_type'}
    )
    skills = models.CharField(max_length=500, blank=True, null=True, help_text="Comma-separated skills")
    
    # Location Information
    permanent_address = models.CharField(max_length=500, blank=True, null=True)
    temporary_address = models.CharField(max_length=500, blank=True, null=True)
    country = models.ForeignKey(
        DropdownMaster, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='country_jobs',
        limit_choices_to={'group__value': 'country'}
    )
    state_city = models.ForeignKey(
        DropdownMaster, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='city_jobs',
        limit_choices_to={'group__value': 'state_city'}
    )
    zip_code = models.CharField(max_length=20, blank=True, null=True)
    video_url = models.URLField(max_length=500, blank=True, null=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True)
    
    # Metadata
    price = models.CharField(max_length=255, blank=True, null=True)  # Kept for backward compatibility
    slug = models.SlugField(unique=True, blank=True)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='posted_jobs')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)  # Automatically generate the slug from the title
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Job'
        verbose_name_plural = 'Jobs'


class Profile(models.Model):
    """Extended User Profile - Base Information"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=30, blank=True)
    work_status = models.CharField(max_length=20, choices=WORK_STATUS_CHOICES, default='findjob')
    
    ROLE_CHOICES = (
        ('rpo_admin', 'RPO Admin'),
        ('hiring_manager', 'Hiring Manager'),
        ('candidate', 'Candidate'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='candidate')
    
    # Basic Details
    job_title = models.CharField(max_length=255, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    education = models.ForeignKey(
        DropdownMaster, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='education_profiles',
        limit_choices_to={'group__text': 'Education'}
    )
    experience = models.ForeignKey(
        DropdownMaster, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='experience_profiles',
        limit_choices_to={'group__text': 'Experience'}
    )
    languages = models.CharField(max_length=500, blank=True, null=True, help_text="Comma-separated languages")
    about = models.TextField(blank=True, null=True)
    
    # Contact Details
    email = models.EmailField(blank=True, null=True)
    temp_address = models.CharField(max_length=500, blank=True, null=True)
    address = models.CharField(max_length=500, blank=True, null=True)
    address2 = models.CharField(max_length=500, blank=True, null=True)
    country = models.ForeignKey(
        DropdownMaster, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='country_profiles',
        limit_choices_to={'group__text': 'Country'}
    )
    city = models.ForeignKey(
        DropdownMaster, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='city_profiles',
        limit_choices_to={'group__text': 'State/City'}
    )
    zip_code = models.CharField(max_length=20, blank=True, null=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True)
    
    # Social Links
    facebook = models.URLField(max_length=500, blank=True, null=True)
    twitter = models.URLField(max_length=500, blank=True, null=True)
    instagram = models.URLField(max_length=500, blank=True, null=True)
    linkedin = models.URLField(max_length=500, blank=True, null=True)
    google_plus = models.URLField(max_length=500, blank=True, null=True)
    
    # Profile Management
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    resume = models.FileField(
        upload_to='candidate-resume/', 
        blank=True, 
        null=True,
        validators=[validate_resume_file],
        help_text="Upload your resume (PDF, DOC, DOCX, or TXT - Max 5MB)"
    )
    profile_completion = models.IntegerField(default=0, help_text="Profile completion percentage")
    is_active = models.BooleanField(default=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def calculate_profile_completion(self):
        """Calculate profile completion percentage"""
        fields = [
            self.full_name, self.phone, self.job_title, self.age, 
            self.education_id, self.experience_id, self.about,
            self.email, self.address, self.country_id, self.city_id,
            self.profile_image
        ]
        filled_fields = sum(1 for field in fields if field)
        return int((filled_fields / len(fields)) * 100)
    
    def save(self, *args, **kwargs):
        """Override save to calculate profile completion"""
        self.profile_completion = self.calculate_profile_completion()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Profile({self.user.username})"

    class Meta:
        db_table = 'user_profile'
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'
        permissions = (
            ("assign_roles", "Can assign roles and manage user roles"),
            ("manage_platform", "Can manage platform settings and content"),
            ("review_candidates", "Can review and shortlist candidates"),
            ("apply_jobs", "Can apply to jobs"),
        )


class CandidateSkill(models.Model):
    """Candidate Skills - Many-to-Many relationship"""
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='skills')
    skill_name = models.CharField(max_length=100)
    proficiency = models.CharField(
        max_length=20,
        choices=[
            ('beginner', 'Beginner'),
            ('intermediate', 'Intermediate'),
            ('advanced', 'Advanced'),
            ('expert', 'Expert')
        ],
        default='intermediate'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.profile.user.username} - {self.skill_name}"
    
    class Meta:
        db_table = 'candidate_skills'
        verbose_name = 'Candidate Skill'
        verbose_name_plural = 'Candidate Skills'
        unique_together = ['profile', 'skill_name']


class CandidateEducation(models.Model):
    """Candidate Education History"""
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='education_history')
    degree = models.CharField(max_length=200)
    institution = models.CharField(max_length=300)
    field_of_study = models.CharField(max_length=200, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    is_current = models.BooleanField(default=False)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.profile.user.username} - {self.degree}"
    
    class Meta:
        db_table = 'candidate_education'
        verbose_name = 'Education History'
        verbose_name_plural = 'Education Histories'
        ordering = ['-end_date', '-start_date']


class CandidateExperience(models.Model):
    """Candidate Work Experience"""
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='work_experience')
    job_title = models.CharField(max_length=200)
    company_name = models.CharField(max_length=300)
    location = models.CharField(max_length=200, blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    is_current = models.BooleanField(default=False)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.profile.user.username} - {self.job_title}"
    
    class Meta:
        db_table = 'candidate_experience'
        verbose_name = 'Work Experience'
        verbose_name_plural = 'Work Experiences'
        ordering = ['-end_date', '-start_date']


class CandidateCertification(models.Model):
    """Candidate Certifications"""
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='certifications')
    certification_name = models.CharField(max_length=300)
    issuing_organization = models.CharField(max_length=300)
    issue_date = models.DateField()
    expiry_date = models.DateField(blank=True, null=True)
    credential_id = models.CharField(max_length=200, blank=True, null=True)
    credential_url = models.URLField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.profile.user.username} - {self.certification_name}"
    
    class Meta:
        db_table = 'candidate_certification'
        verbose_name = 'Certification'
        verbose_name_plural = 'Certifications'
        ordering = ['-issue_date']


class ResumeProcessing(models.Model):
    """Resume Processing Tracking and Results"""
    
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    )
    
    # Core Fields
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resume_processing')
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='resume_processing', null=True, blank=True)
    
    # File Information
    resume_path = models.CharField(max_length=500, help_text="Path to the uploaded resume file")
    original_filename = models.CharField(max_length=255, blank=True)
    file_size = models.IntegerField(default=0, help_text="File size in bytes")
    file_extension = models.CharField(max_length=10, blank=True)
    
    # Processing Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    processing_started_at = models.DateTimeField(null=True, blank=True)
    processing_completed_at = models.DateTimeField(null=True, blank=True)
    error_message = models.TextField(blank=True, null=True)
    
    # Extracted Data
    resume_text = models.TextField(blank=True, null=True, help_text="Full extracted text from resume")
    resume_json = models.JSONField(blank=True, null=True, help_text="Structured JSON data extracted from resume")
    
    # Quick Access Fields (extracted from JSON for faster queries)
    extracted_skills = models.TextField(blank=True, null=True, help_text="Comma-separated skills")
    extracted_email = models.EmailField(blank=True, null=True)
    extracted_phone = models.CharField(max_length=50, blank=True, null=True)
    years_of_experience = models.CharField(max_length=50, blank=True, null=True)
    sentiment_score = models.FloatField(null=True, blank=True, help_text="Resume sentiment polarity score")
    word_count = models.IntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.original_filename} ({self.status})"
    
    def get_status_badge_class(self):
        """Return Bootstrap badge class based on status"""
        status_classes = {
            'pending': 'bg-warning',
            'processing': 'bg-info',
            'completed': 'bg-success',
            'failed': 'bg-danger',
        }
        return status_classes.get(self.status, 'bg-secondary')
    
    def get_processing_duration(self):
        """Calculate processing duration in seconds"""
        if self.processing_started_at and self.processing_completed_at:
            delta = self.processing_completed_at - self.processing_started_at
            return delta.total_seconds()
        return None
    
    class Meta:
        db_table = 'resume_processing'
        verbose_name = 'Resume Processing'
        verbose_name_plural = 'Resume Processings'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['status', 'created_at']),
        ]


class ErrorLog(models.Model):
    """
    Comprehensive error logging model for tracking application errors.
    Captures internal errors only (excludes library/framework errors).
    """
    # User Information
    user = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='error_logs',
        help_text="User who encountered the error (if authenticated)"
    )
    
    # Error Details
    error_type = models.CharField(
        max_length=255,
        db_index=True,
        help_text="Type of exception (e.g., ValueError, KeyError)"
    )
    error_message = models.TextField(
        help_text="Error message from the exception"
    )
    error_traceback = models.TextField(
        help_text="Full traceback of the error"
    )
    error_hash = models.CharField(
        max_length=64,
        db_index=True,
        help_text="Unique hash for error deduplication (file+function+line+type)"
    )
    
    # Source Location (Internal Files Only)
    file_path = models.CharField(
        max_length=500,
        db_index=True,
        help_text="Relative path to the file where error occurred"
    )
    function_name = models.CharField(
        max_length=255,
        db_index=True,
        help_text="Function/method name where error occurred"
    )
    line_number = models.IntegerField(
        help_text="Line number where error occurred"
    )
    
    # Request Context
    request_method = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        help_text="HTTP method (GET, POST, PUT, DELETE, etc.)"
    )
    request_path = models.CharField(
        max_length=2000,
        blank=True,
        null=True,
        db_index=True,
        help_text="URL path that triggered the error"
    )
    request_data = models.JSONField(
        default=dict,
        blank=True,
        help_text="Request GET/POST data (sensitive data filtered)"
    )
    
    # Client Information
    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        help_text="Client IP address"
    )
    user_agent = models.TextField(
        blank=True,
        null=True,
        help_text="Browser user agent string"
    )
    
    # Response Information
    status_code = models.IntegerField(
        default=500,
        help_text="HTTP status code returned"
    )
    
    # Resolution Tracking
    is_resolved = models.BooleanField(
        default=False,
        db_index=True,
        help_text="Whether this error has been resolved"
    )
    resolved_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When the error was marked as resolved"
    )
    resolved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='resolved_errors',
        help_text="User who resolved the error"
    )
    resolution_notes = models.TextField(
        blank=True,
        null=True,
        help_text="Notes about how the error was resolved"
    )
    
    # Occurrence Tracking
    occurrence_count = models.IntegerField(
        default=1,
        help_text="Number of times this exact error has occurred"
    )
    first_occurred = models.DateTimeField(
        auto_now_add=True,
        help_text="When this error first occurred"
    )
    last_occurred = models.DateTimeField(
        auto_now=True,
        db_index=True,
        help_text="Most recent occurrence of this error"
    )
    
    # Severity Level
    SEVERITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]
    severity = models.CharField(
        max_length=20,
        choices=SEVERITY_CHOICES,
        default='medium',
        db_index=True,
        help_text="Error severity level"
    )
    
    # Environment Information
    environment = models.CharField(
        max_length=50,
        default='development',
        help_text="Environment where error occurred (development/production)"
    )
    
    # Timestamps
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        help_text="When this error record was created"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="When this error record was last updated"
    )
    
    class Meta:
        db_table = 'error_logs'
        verbose_name = 'Error Log'
        verbose_name_plural = 'Error Logs'
        ordering = ['-last_occurred']
        indexes = [
            models.Index(fields=['error_type', 'is_resolved']),
            models.Index(fields=['file_path', 'function_name']),
            models.Index(fields=['is_resolved', '-last_occurred']),
            models.Index(fields=['severity', '-created_at']),
            models.Index(fields=['error_hash', '-last_occurred']),
        ]
    
    def __str__(self):
        return f"{self.error_type} in {self.function_name} (Line {self.line_number}) - {self.last_occurred.strftime('%Y-%m-%d %H:%M:%S')}"
    
    def get_severity_badge_class(self):
        """Get Bootstrap badge class for severity level"""
        severity_classes = {
            'low': 'bg-info',
            'medium': 'bg-warning',
            'high': 'bg-danger',
            'critical': 'bg-dark'
        }
        return severity_classes.get(self.severity, 'bg-secondary')
    
    def get_short_file_path(self):
        """Get shortened file path for display"""
        if len(self.file_path) > 50:
            return '...' + self.file_path[-47:]
        return self.file_path
    
    def mark_resolved(self, user=None, notes=''):
        """Mark this error as resolved"""
        from django.utils import timezone
        self.is_resolved = True
        self.resolved_at = timezone.now()
        self.resolved_by = user
        self.resolution_notes = notes
        self.save()
    
    def increment_occurrence(self):
        """Increment occurrence count for duplicate errors"""
        self.occurrence_count += 1
        self.save(update_fields=['occurrence_count', 'last_occurred', 'updated_at'])