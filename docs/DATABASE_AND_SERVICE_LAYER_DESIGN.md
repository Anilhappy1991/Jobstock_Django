# Complete Database Design & Service Layer Implementation

## Overview
This document describes the complete database design and service layer architecture for the Jobstock Django application with three user roles: **Candidate**, **Hiring Manager**, and **RPO Admin**.

## 1. Database Models

### Core User Models

#### Profile (Extended User)
- Base profile for all users
- Fields: full_name, phone, role, work_status, job_title, age, education, experience, etc.
- One-to-One relationship with Django User model
- Calculates profile completion percentage

#### HiringManager
- Extended data for Hiring Managers
- Fields: company_name, company_website, company_size, industry, department, position
- Permissions: can_post_jobs, can_view_all_applications, can_shortlist_candidates
- Statistics: total_jobs_posted, total_hires_made

#### CandidateProfile
- Extended data for job seekers
- Fields: current_job_title, current_company, current_salary, expected_salary
- Job preferences: preferred_job_type, preferred_location, willing_to_relocate
- Statistics: total_applications, total_interviews, total_offers
- Job search status: actively_looking, open_to_offers, not_looking

#### RPOAdmin
- Extended data for RPO (Recruitment Process Outsourcing) Administrators
- Fields: organization_name, organization_website, license_number
- Permissions: can_manage_all_jobs, can_manage_candidates, can_generate_reports
- Statistics: total_placements, total_clients

### Application Models

#### JobApplication
- Links candidates to jobs they've applied for
- Status tracking: submitted, under_review, shortlisted, interview_scheduled, offered, accepted, rejected
- Interview details: interview_date, interview_location, interview_notes
- Recruiter feedback: recruiter_rating, recruiter_notes

#### ApplicationStatusHistory
- Tracks all status changes for applications
- Fields: application, status, changed_by, notes, created_at

#### SavedJob
- Allows candidates to bookmark jobs for later
- Fields: candidate, job, saved_at, notes

#### Notification
- User notification system
- Types: application, interview, status_change, new_job, message, system

## 2. Common Response Utility

### ApiResponse Class
Standardized response format for consistency across both REST API and Django templates.

**Response Structure:**
```json
{
    "success": true/false,
    "status_code": 200,
    "message": "Success message",
    "data": {...},           // Optional
    "error": "Error message", // Optional
    "error_details": {...}   // Optional
}
```

**Available Methods:**
- `ApiResponse.success(data, message)` - 200 OK
- `ApiResponse.created(data, message)` - 201 Created
- `ApiResponse.error(message, error_details, status_code)` - 400 Bad Request
- `ApiResponse.not_found(message)` - 404 Not Found
- `ApiResponse.unauthorized(message)` - 401 Unauthorized
- `ApiResponse.forbidden(message)` - 403 Forbidden
- `ApiResponse.validation_error(errors, message)` - 422 Unprocessable Entity
- `ApiResponse.server_error(message, error_details)` - 500 Internal Server Error

### DRFResponse Class
Wraps ApiResponse for Django REST Framework responses.

### DjangoResponse Class
Converts ApiResponse to:
- JsonResponse for AJAX calls
- Context dict for template rendering

## 3. Service Layer Architecture

### BaseService
Foundation class for all services with common methods:
- `get_all(filters, order_by)` - Get all records
- `get_by_id(id)` - Get single record
- `create(data)` - Create new record
- `update(id, data)` - Update record
- `delete(id)` - Delete record
- `paginate(queryset, page, page_size)` - Paginate results

### UserService
Handles user management:
- `create_user(username, email, password, role, **extra_data)` - Create user with role-specific profile
- `authenticate_user(username, password)` - Login authentication
- `get_user_by_username(username)` - Get user details

### ProfileService
Manages user profiles:
- `get_profile_by_user_id(user_id)` - Get profile with role data
- `update_profile(user_id, data)` - Update profile
- `get_user_role_data(user)` - Get role-specific data

### JobService
Handles job operations:

**Legacy Methods (backward compatibility):**
- `get_all_jobs(user, filters)` - Returns QuerySet
- `get_job_by_id(job_id, user)` - Returns Job object
- `create_job(data, user)` - Create job
- `update_job(job_id, data, user)` - Update job
- `delete_job(job_id, user)` - Delete job
- `get_dropdown_data()` - Get all dropdown options
- `get_job_statistics(user)` - Get job stats

**New API Methods (standardized responses):**
- `get_all_jobs_api(filters, page, page_size)` - Get jobs with pagination
- `get_job_details_api(job_id, user_id)` - Get job details
- `search_jobs_api(search_query, filters, page, page_size)` - Search jobs

### ApplicationService
Manages job applications:
- `apply_for_job(user_id, job_id, cover_letter, resume)` - Submit application
- `get_candidate_applications(user_id, page, page_size)` - Get candidate's applications
- `get_job_applications(job_id, user_id, page, page_size)` - Get applications for a job
- `update_application_status(application_id, user_id, new_status, notes)` - Update status
- `save_job(user_id, job_id, notes)` - Save job for later
- `get_saved_jobs(user_id, page, page_size)` - Get saved jobs

## 4. Usage Examples

### Creating a User
```python
from App.services.user_service import UserService

# Create Candidate
response = UserService.create_user(
    username='john_doe',
    email='john@example.com',
    password='secure_password',
    role='candidate',
    full_name='John Doe',
    phone='1234567890'
)

# Create Hiring Manager
response = UserService.create_user(
    username='jane_manager',
    email='jane@company.com',
    password='secure_password',
    role='hiring_manager',
    full_name='Jane Manager',
    phone='9876543210',
    company_name='Tech Corp'
)

# Create RPO Admin
response = UserService.create_user(
    username='admin_rpo',
    email='admin@rpo.com',
    password='secure_password',
    role='rpo_admin',
    full_name='RPO Admin',
    phone='5555555555',
    organization_name='Recruitment Solutions Inc'
)
```

### Authenticating User
```python
response = UserService.authenticate_user('john_doe', 'secure_password')

if response['success']:
    user_data = response['data']
    print(f"Welcome {user_data['profile']['full_name']}")
```

### Getting Jobs (in Django View)
```python
from App.services.job_service import JobService
from App.utils.response import DjangoResponse

def job_list_view(request):
    # Get jobs using service
    response = JobService.get_all_jobs_api(
        filters={'job_type': 'full-time'},
        page=1,
        page_size=10
    )
    
    # Convert to template context
    context = DjangoResponse.context(response)
    return render(request, 'jobs/list.html', context)
```

### Getting Jobs (REST API View)
```python
from rest_framework.views import APIView
from App.services.job_service import JobService
from App.utils.response import DRFResponse

class JobListAPIView(APIView):
    def get(self, request):
        response = JobService.get_all_jobs_api(
            filters=request.query_params.dict(),
            page=int(request.GET.get('page', 1)),
            page_size=int(request.GET.get('page_size', 10))
        )
        return DRFResponse.send(response)
```

### Applying for a Job
```python
from App.services.application_service import ApplicationService

response = ApplicationService.apply_for_job(
    user_id=request.user.id,
    job_id=123,
    cover_letter="I am interested in this position...",
    resume=request.FILES.get('resume')
)

if response['success']:
    messages.success(request, response['message'])
```

## 5. Permissions by Role

### Candidate
- ✅ View jobs
- ✅ Apply for jobs
- ✅ Save jobs
- ✅ View own applications
- ✅ Update own profile
- ❌ Post jobs
- ❌ View other applications

### Hiring Manager
- ✅ View jobs
- ✅ Post jobs
- ✅ Edit own jobs
- ✅ View applications for own jobs
- ✅ Update application status
- ✅ Shortlist candidates
- ❌ View all jobs' applications (only own)

### RPO Admin
- ✅ View all jobs
- ✅ Post jobs
- ✅ Edit all jobs
- ✅ View all applications
- ✅ Update all application statuses
- ✅ Manage candidates
- ✅ Manage hiring managers
- ✅ Generate reports

## 6. File Locations

```
App/
├── models.py                       # Existing models (Job, Profile, etc.)
├── models_extended.py              # New role-based models
├── utils/
│   └── response.py                 # ApiResponse, DRFResponse, DjangoResponse
└── services/
    ├── base_service.py             # BaseService foundation
    ├── user_service.py             # UserService, ProfileService
    ├── job_service.py              # JobService (enhanced with API methods)
    └── application_service.py      # ApplicationService
```

## 7. Next Steps

1. ✅ Install Django REST Framework: `pip install djangorestframework`
2. ✅ Add to INSTALLED_APPS in settings.py
3. ✅ Run migrations: `python manage.py makemigrations` and `python manage.py migrate`
4. Create REST API viewsets and serializers
5. Create API URL routing
6. Update existing Django views to use service layer
7. Test all functionality

## 8. Benefits of This Architecture

1. **Separation of Concerns**: Business logic in services, not in views
2. **Reusability**: Same service used by both REST API and Django templates
3. **Consistency**: Standardized response format everywhere
4. **Testability**: Easy to unit test services independently
5. **Maintainability**: Changes in one place affect both REST and template views
6. **Scalability**: Easy to add new roles and features
7. **Error Handling**: Centralized error handling with detailed responses
