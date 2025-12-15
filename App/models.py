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


class Job(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    price = models.CharField(max_length=255)
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