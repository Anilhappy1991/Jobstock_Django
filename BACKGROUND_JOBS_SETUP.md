# Background Job Setup Instructions

## File Structure Created:
```
Jobstock/
├── celery.py                    # Celery configuration
├── __init__.py                  # Updated to load Celery
└── settings.py                  # Updated with Celery & processing config

App/
├── tasks.py                     # Background tasks (NEW)
└── views_tasks.py              # Views for triggering tasks (NEW)

templates/
└── pages/
    └── task_status.html        # Task status page (NEW)

requirements.txt                 # Updated with new packages
```

## Installation Steps:

### 1. Install Redis (Required for Celery)
**Windows:**
```powershell
# Download and install Redis from:
# https://github.com/microsoftarchive/redis/releases
# OR use WSL/Docker
```

**Alternative - Use Django-Q (No Redis Required):**
If you prefer not to use Redis, see the alternative section below.

### 2. Install Python Packages
```bash
pip install -r requirements.txt

# Download SpaCy language model
python -m spacy download en_core_web_sm
```

### 3. Run Database Migrations
```bash
python manage.py migrate
```

### 4. Add URL Routes
Add to `App/urls.py`:
```python
from .views_tasks import (
    trigger_resume_processing,
    check_task_status,
    task_status_page,
    trigger_job_matching
)

urlpatterns = [
    # ... existing urls ...
    
    # Background task URLs
    path('trigger-resume-processing/', trigger_resume_processing, name='trigger_resume_processing'),
    path('trigger-job-matching/', trigger_job_matching, name='trigger_job_matching'),
    path('task-status/<str:task_id>/', check_task_status, name='task_status'),
    path('task-status-page/<str:task_id>/', task_status_page, name='task_status_page'),
]
```

### 5. Start Celery Worker
Open a new terminal and run:
```bash
cd C:\RandR\Jobstock_Django_v1.0.0\Jobstock_Django
celery -A Jobstock worker --loglevel=info --pool=solo
```

### 6. Start Celery Beat (Optional - for scheduled tasks)
Open another terminal:
```bash
celery -A Jobstock beat --loglevel=info
```

### 7. Start Django Development Server
```bash
python manage.py runserver
```

## Usage Examples:

### 1. Trigger Resume Processing After Upload
Update your resume upload view in `App/views.py`:
```python
from .tasks import process_resume_document

def candidate_profile_detail(request, username):
    # ... existing code ...
    
    if request.method == 'POST' and form_type == 'resume':
        # ... save resume ...
        
        if profile.resume:
            # Trigger background processing
            task = process_resume_document.delay(
                profile.resume.path,
                profile.id
            )
            messages.success(
                request,
                f'Resume uploaded! Processing in background. Task ID: {task.id}'
            )
            return redirect('App:task_status_page', task_id=task.id)
```

### 2. Add Button to Manually Trigger Processing
Add to `candidate-profile.html`:
```html
{% if profile.resume %}
<form method="POST" action="{% url 'App:trigger_resume_processing' %}" class="d-inline">
    {% csrf_token %}
    <button type="submit" class="btn btn-info">
        <i class="fas fa-cog"></i> Analyze Resume
    </button>
</form>
{% endif %}
```

### 3. Check Task Status via AJAX
```javascript
function checkTaskStatus(taskId) {
    fetch(`/app/task-status/${taskId}/`)
        .then(response => response.json())
        .then(data => {
            console.log('Task status:', data);
            if (data.status === 'SUCCESS') {
                console.log('Results:', data.result);
            }
        });
}
```

## Available Background Tasks:

### 1. `process_resume_document(resume_path, profile_id)`
- Analyzes document layout using LayoutParser
- Extracts entities using SpaCy
- Performs deep analysis with Transformers
- Returns comprehensive results

### 2. `process_job_description(job_description_text, job_id)`
- Extracts entities from job descriptions
- Analyzes requirements
- Returns structured data

### 3. `match_resume_to_jobs(profile_id, job_ids)`
- Matches resume against multiple jobs
- Calculates match scores
- Returns ranked results

### 4. `cleanup_temp_files()` (Scheduled)
- Cleans up temporary processing files
- Runs automatically every 24 hours

## Monitoring Tasks:

### Django Admin
Access: http://localhost:8000/admin/
- View periodic tasks: Django Celery Beat > Periodic tasks
- View task results: Django Celery Results > Task results

### Command Line
```bash
# View active tasks
celery -A Jobstock inspect active

# View registered tasks
celery -A Jobstock inspect registered

# View task stats
celery -A Jobstock inspect stats
```

## Alternative: Django-Q (No Redis Required)

If you prefer not to use Redis, you can use Django-Q instead:

1. Install: `pip install django-q`
2. Add to INSTALLED_APPS: `'django_q'`
3. Configure in settings.py:
```python
Q_CLUSTER = {
    'name': 'Jobstock',
    'workers': 4,
    'timeout': 90,
    'retry': 120,
    'queue_limit': 50,
    'bulk': 10,
    'orm': 'default',
}
```
4. Run: `python manage.py qcluster`

## Troubleshooting:

### Issue: "No module named 'celery'"
Solution: `pip install celery redis`

### Issue: "Cannot connect to Redis"
Solution: Ensure Redis server is running

### Issue: "Model not found"
Solution: Run SpaCy download command:
```bash
python -m spacy download en_core_web_sm
```

### Issue: Tasks not executing
Solution: Check Celery worker is running and logs for errors

## Production Deployment:

For production, use:
1. Supervisor or systemd to manage Celery workers
2. Redis in production mode or RabbitMQ
3. Separate worker machines for heavy processing
4. Configure proper logging and monitoring

## Next Steps:

1. Integrate OCR (pytesseract) for actual text extraction from PDFs
2. Add more sophisticated matching algorithms
3. Store results in database for caching
4. Add real-time notifications using WebSockets
5. Implement retry logic for failed tasks
