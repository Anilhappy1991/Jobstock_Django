from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

# Create your models here.

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


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=30, blank=True)
    work_status = models.CharField(max_length=20, choices=WORK_STATUS_CHOICES, default='findjob')
    ROLE_CHOICES = (
        ('rpo_admin', 'RPO Admin'),
        ('hiring_manager', 'Hiring Manager'),
        ('candidate', 'Candidate'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='candidate')

    def __str__(self):
        return f"Profile({self.user.username})"

    class Meta:
        permissions = (
            ("assign_roles", "Can assign roles and manage user roles"),
            ("manage_platform", "Can manage platform settings and content"),
            ("review_candidates", "Can review and shortlist candidates"),
            ("apply_jobs", "Can apply to jobs"),
        )