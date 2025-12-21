# Quick Start Guide - Service Layer & REST API

## What Has Been Implemented

### ✅ 1. Common Response Utility (`App/utils/response.py`)
- **ApiResponse**: Standardized response format
- **DRFResponse**: REST Framework wrapper
- **DjangoResponse**: Django template wrapper

### ✅ 2. Extended Database Models (`App/models_extended.py`)
- **HiringManager**: Extended data for hiring managers
- **CandidateProfile**: Extended data for candidates
- **RPOAdmin**: Extended data for RPO administrators
- **JobApplication**: Job application tracking
- **ApplicationStatusHistory**: Status change history
- **SavedJob**: Saved jobs for candidates
- **Notification**: User notification system

### ✅ 3. Service Layer (`App/services/`)
- **BaseService**: Foundation for all services
- **UserService**: User creation, authentication, profile management
- **JobService**: Job CRUD operations with API methods
- **ApplicationService**: Job application management

### ✅ 4. Django REST Framework
- Installed and configured
- Ready for API development

## Next Steps to Complete Implementation

### Step 1: Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 2: Create Django Groups
Run this in Django shell (`python manage.py shell`):
```python
from django.contrib.auth.models import Group

# Create groups for the three roles
Group.objects.get_or_create(name='Candidate')
Group.objects.get_or_create(name='Hiring Manager')
Group.objects.get_or_create(name='Rpo Admin')
```

### Step 3: Test User Creation
```python
from App.services.user_service import UserService

# Create a test candidate
response = UserService.create_user(
    username='test_candidate',
    email='candidate@test.com',
    password='H@ppy123',
    role='candidate',
    full_name='Test Candidate',
    phone='1234567890'
)

print(response)

# Create a test hiring manager
response = UserService.create_user(
    username='test_hm',
    email='hm@test.com',
    password='H@ppy123',
    role='hiring_manager',
    full_name='Test HM',
    phone='9876543210',
    company_name='Test Company'
)

print(response)
```

### Step 4: Test Authentication
```python
from App.services.user_service import UserService

response = UserService.authenticate_user('test_candidate', 'H@ppy123')

if response['success']:
    print("Login successful!")
    print(response['data'])
else:
    print("Login failed:", response['message'])
```

### Step 5: Test Job Operations
```python
from App.services.job_service import JobService

# Get all jobs
response = JobService.get_all_jobs_api(
    filters={'is_active': True},
    page=1,
    page_size=10
)

print(response)
```

## How to Use in Your Views

### Example 1: Django Template View
```python
from django.shortcuts import render
from App.services.job_service import JobService
from App.utils.response import DjangoResponse

def job_list(request):
    # Call service
    response = JobService.get_all_jobs_api(
        filters=request.GET.dict(),
        page=int(request.GET.get('page', 1))
    )
    
    # Convert to template context
    context = DjangoResponse.context(response)
    
    # Add additional context if needed
    context['title'] = 'Job Listings'
    
    return render(request, 'jobs/list.html', context)
```

### Example 2: AJAX/JSON Response
```python
from django.views import View
from django.http import JsonResponse
from App.services.job_service import JobService
from App.utils.response import DjangoResponse

class JobListAjaxView(View):
    def get(self, request):
        response = JobService.get_all_jobs_api(
            filters=request.GET.dict(),
            page=int(request.GET.get('page', 1))
        )
        return DjangoResponse.json(response)
```

### Example 3: REST API View
```python
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from App.services.job_service import JobService
from App.utils.response import DRFResponse

class JobListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        response = JobService.get_all_jobs_api(
            filters=request.query_params.dict(),
            page=int(request.GET.get('page', 1))
        )
        return DRFResponse.send(response)
```

## Template Usage

### In Your HTML Template
```html
{% if response.success %}
    <div class="alert alert-success">
        {{ response.message }}
    </div>
    
    {% for job in response.data.items %}
        <div class="job-card">
            <h3>{{ job.title }}</h3>
            <p>{{ job.job_summary }}</p>
        </div>
    {% endfor %}
    
    <!-- Pagination -->
    <div class="pagination">
        {% if response.data.pagination.has_previous %}
            <a href="?page={{ response.data.pagination.page|add:-1 }}">Previous</a>
        {% endif %}
        
        Page {{ response.data.pagination.page }} of {{ response.data.pagination.total_pages }}
        
        {% if response.data.pagination.has_next %}
            <a href="?page={{ response.data.pagination.page|add:1 }}">Next</a>
        {% endif %}
    </div>
{% else %}
    <div class="alert alert-danger">
        {{ response.error }}
        {% if response.error_details %}
            <ul>
                {% for key, errors in response.error_details.items %}
                    <li>{{ key }}: {{ errors }}</li>
                {% endfor %}
            </ul>
        {% endif %}
    </div>
{% endif %}
```

## API Response Format

All API responses follow this structure:

```json
{
    "success": true,
    "status_code": 200,
    "message": "Jobs retrieved successfully",
    "data": {
        "items": [...],
        "pagination": {
            "page": 1,
            "page_size": 10,
            "total_count": 25,
            "total_pages": 3,
            "has_next": true,
            "has_previous": false
        }
    }
}
```

Error responses:
```json
{
    "success": false,
    "status_code": 400,
    "message": "Validation failed",
    "error": "Validation failed",
    "error_details": {
        "email": ["Email already exists"]
    }
}
```

## Common Service Methods

### UserService
- `create_user(username, email, password, role, **extra_data)`
- `authenticate_user(username, password)`
- `get_user_by_username(username)`

### ProfileService
- `get_profile_by_user_id(user_id)`
- `update_profile(user_id, data)`

### JobService
- `get_all_jobs_api(filters, page, page_size)`
- `get_job_details_api(job_id, user_id)`
- `search_jobs_api(search_query, filters, page, page_size)`

### ApplicationService
- `apply_for_job(user_id, job_id, cover_letter, resume)`
- `get_candidate_applications(user_id, page, page_size)`
- `get_job_applications(job_id, user_id, page, page_size)`
- `update_application_status(application_id, user_id, new_status, notes)`
- `save_job(user_id, job_id, notes)`
- `get_saved_jobs(user_id, page, page_size)`

## Testing Checklist

- [ ] Run migrations
- [ ] Create user groups
- [ ] Test creating users for all roles
- [ ] Test user authentication
- [ ] Test job operations
- [ ] Test application operations
- [ ] Update existing views to use services
- [ ] Test API endpoints
- [ ] Update templates to use standardized responses

## Benefits

1. ✅ **Consistent Responses**: Same format everywhere
2. ✅ **Reusable Code**: Services work for both API and templates
3. ✅ **Easy Testing**: Test services independently
4. ✅ **Better Error Handling**: Standardized error responses
5. ✅ **Scalable**: Easy to add new features
6. ✅ **Maintainable**: Changes in one place
7. ✅ **Type Safety**: Clear return types
8. ✅ **Documentation**: Self-documenting with clear responses
