# Windows-Compatible Background Jobs Setup

## ✅ Installation Complete!

All packages have been installed successfully with Windows-compatible alternatives.

## Files Structure:

```
Jobstock/
├── celery.py                    # Celery configuration
├── __init__.py                  # Celery initialization  
└── settings.py                  # Updated with Celery config

App/
├── tasks_simple.py             # Simplified tasks (USE THIS)
├── tasks.py                     # Original (requires build tools)
└── views_tasks.py              # Task trigger views

templates/pages/
└── task_status.html            # Status monitoring page
```

## Quick Start (3 Steps):

### 1. Run Migrations
```powershell
python manage.py migrate
```

### 2. Add URLs to App/urls.py
Add these imports and URLs:

```python
from .views_tasks import (
    trigger_resume_processing,
    check_task_status,
    task_status_page,
)

urlpatterns = [
    # ... existing patterns ...
    
    # Background task URLs
    path('process-resume/', trigger_resume_processing, name='trigger_resume_processing'),
    path('task-status/<str:task_id>/', check_task_status, name='task_status'),
    path('task-status-page/<str:task_id>/', task_status_page, name='task_status_page'),
]
```

### 3. Update views_tasks.py to use simple tasks
Change the import at the top of `App/views_tasks.py`:

```python
# Change this line:
from .tasks import process_resume_document

# To this:
from .tasks_simple import process_resume_simple as process_resume_document
```

## Running the System:

### Option A: Redis + Celery (Recommended for Production)

**Terminal 1 - Start Redis:**
```powershell
# Download Redis for Windows from:
# https://github.com/microsoftarchive/redis/releases
# Then run:
redis-server
```

**Terminal 2 - Start Celery Worker:**
```powershell
celery -A Jobstock worker --loglevel=info --pool=solo
```

**Terminal 3 - Start Django:**
```powershell
python manage.py runserver
```

### Option B: Django-Q (No Redis Required)

**Install:**
```powershell
pip install django-q
```

**Add to INSTALLED_APPS in settings.py:**
```python
INSTALLED_APPS = [
    # ... existing apps ...
    'django_q',
]
```

**Add to settings.py:**
```python
Q_CLUSTER = {
    'name': 'Jobstock',
    'workers': 4,
    'timeout': 300,
    'retry': 360,
    'queue_limit': 50,
    'bulk': 10,
    'orm': 'default',
}
```

**Run migrations:**
```powershell
python manage.py migrate
```

**Start Django-Q (Terminal 1):**
```powershell
python manage.py qcluster
```

**Start Django (Terminal 2):**
```powershell
python manage.py runserver
```

## Usage:

### Auto-trigger on resume upload
Update your `candidate_profile_detail` view in `App/views.py`:

```python
from .tasks_simple import process_resume_simple

def candidate_profile_detail(request, username):
    # ... existing code ...
    
    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        
        if form_type == 'resume':
            form_resume = ResumeUploadForm(request.POST, request.FILES, instance=profile)
            if form_resume.is_valid():
                form_resume.save()
                
                # Trigger background processing
                task = process_resume_simple.delay(
                    profile.resume.path,
                    profile.id
                )
                
                messages.success(
                    request,
                    'Resume uploaded successfully! Processing in background.'
                )
                return redirect('App:task_status_page', task_id=task.id)
```

### Manual trigger button
Add to `candidate-profile.html` in the resume section:

```html
{% if profile.resume %}
<form method="POST" action="{% url 'App:trigger_resume_processing' %}" class="mt-2">
    {% csrf_token %}
    <button type="submit" class="btn btn-info btn-sm">
        <i class="fas fa-cog"></i> Analyze Resume
    </button>
</form>
{% endif %}
```

## What the System Does:

### ✅ Text Extraction:
- PDF files (using pdfplumber + PyPDF2)
- DOCX files (using python-docx)
- TXT files (direct reading)

### ✅ Information Extraction:
- **Contact Info**: Emails, phone numbers, LinkedIn, GitHub
- **Named Entities**: Names, organizations, locations (using NLTK)
- **Skills**: Tech skills, programming languages, frameworks
- **Experience**: Years of experience extraction

### ✅ Analysis:
- **Text Statistics**: Word count, sentence count, readability
- **Sentiment Analysis**: Document tone using TextBlob
- **Keyword Extraction**: Most common terms

## Testing:

### 1. Upload a resume through the candidate profile page

### 2. Check task status:
```javascript
// In browser console
fetch('/app/task-status/<task-id>/')
    .then(r => r.json())
    .then(data => console.log(data));
```

### 3. View results in task status page:
Navigate to `/app/task-status-page/<task-id>/`

## Troubleshooting:

### Error: "No module named 'nltk_data'"
```powershell
python -c "import nltk; nltk.download('punkt'); nltk.download('averaged_perceptron_tagger'); nltk.download('maxent_ne_chunker'); nltk.download('words'); nltk.download('stopwords')"
```

### Error: "Connection refused" (Celery/Redis)
- Make sure Redis is running
- Or use Django-Q instead (no Redis needed)

### Error: "Task not found"
- Ensure Celery worker is running
- Check worker logs for errors

## Advanced Features (Optional):

### Install ML libraries later (if you get build tools):

```powershell
# Install Visual Studio Build Tools first from:
# https://visualstudio.microsoft.com/downloads/

# Then install:
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
pip install transformers
pip install spacy
python -m spacy download en_core_web_sm
```

Then you can switch to using `App/tasks.py` for advanced ML features.

## Next Steps:

1. ✅ Install packages - DONE
2. ⏳ Run migrations
3. ⏳ Add URLs
4. ⏳ Choose Redis+Celery OR Django-Q
5. ⏳ Test with a sample resume

## Support:

- Celery Docs: https://docs.celeryq.dev/
- Django-Q Docs: https://django-q.readthedocs.io/
- NLTK Docs: https://www.nltk.org/
