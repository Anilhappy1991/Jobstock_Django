# Resume Processing Service - Generic & Reusable Implementation

## Overview
Created a generic, reusable resume processing service that extracts data from resumes and stores it in the database. This service is used by both:
- **Candidate Profile Upload** (`/candidate-profile/`)
- **RPO Bulk Resume Upload** (`/rpo-resume-upload/`)

## Architecture

### Service Layer Pattern
```
Views/API → Service Layer → Models/Database
```

### Key Components

#### 1. ResumeProcessingService (Generic)
**File:** `App/services/resume_processing_service.py`

**Purpose:** Generic resume processing logic reusable across the application

**Key Methods:**

```python
# Create database record
create_resume_record(user, file_path, original_filename, file_size, file_extension, profile=None)
→ Returns: ResumeProcessing instance

# Extract all data from resume
extract_resume_data(file_path)
→ Returns: Dict with text, contact_info, skills, entities, statistics, sentiment, metadata

# Update database record with extracted data
update_resume_record(resume_record, extracted_data)
→ Returns: Updated ResumeProcessing instance

# Complete processing workflow (single resume)
process_resume(file_path, user, resume_record_id=None, profile=None)
→ Returns: {'success': bool, 'resume_record': obj, 'extracted_data': dict, 'error': str}

# Batch processing (multiple resumes)
process_multiple_resumes(resume_records, verbose=False)
→ Returns: {'total': int, 'successful': int, 'failed': int, 'results': list}
```

**Data Extracted:**
- **Text:** Full resume text
- **Contact Info:** Emails, phone numbers
- **Skills:** Technical skills, experience years
- **Entities:** Named entities (ORG, PERSON, GPE, etc.)
- **Statistics:** Word count, sentence count, reading level
- **Sentiment:** Polarity and sentiment label

#### 2. ResumeUploadService (File Handling)
**File:** `App/services/resume_upload_service.py`

**Purpose:** Handle file uploads, validation, and storage

**Key Methods:**

```python
# Validate uploaded file
validate_file(file)
→ Returns: {'valid': bool, 'error': str}

# Get upload path with username_userID structure
get_upload_path(user)
→ Returns: (absolute_path, relative_path) tuple

# Save file to disk
save_resume_file(file, user)
→ Returns: {'success': bool, 'filename': str, 'file_path': str, 'relative_path': str}

# Upload multiple resumes
upload_resumes(files, user)
→ Returns: ApiResponse with results

# Process pending resumes (NEW)
process_pending_resumes(user, resume_ids=None)
→ Returns: ApiResponse with processing results

# Process single resume (NEW)
process_single_resume(resume_id, user)
→ Returns: ApiResponse with processing result
```

**File Storage Structure:**
```
/Data/resume/YYYYMMDD/username_userID/filename.ext
```

**Database Storage:**
```
Relative path: Data/resume/20251221/johndoe_5/resume.pdf
```

## Usage Examples

### 1. Candidate Profile Upload (Single Resume)
**Location:** `App/views/candidate_views.py`

```python
# When user uploads resume in profile
if 'resume' in request.FILES:
    resume_file = request.FILES['resume']
    
    # Create database record
    resume_record = ResumeProcessing.objects.create(
        user=request.user,
        profile=profile,
        resume_path=saved_profile.resume.path,
        original_filename=resume_file.name,
        file_size=resume_file.size,
        file_extension=os.path.splitext(resume_file.name)[1].lower(),
        status='pending'
    )
    
    # Trigger background processing
    def process_in_background():
        call_command('process_resumes', user=request.user.username, verbosity=0)
    
    thread = threading.Thread(target=process_in_background, daemon=True)
    thread.start()
```

### 2. RPO Bulk Upload (Multiple Resumes)
**Location:** `App/views/rpo_admin_views.py`

```python
# Upload multiple files
files = request.FILES.getlist('resumes')
result = ResumeUploadService.upload_resumes(files, request.user)
# Files saved, database records created with status='pending'

# Process all pending resumes
result = ResumeUploadService.process_pending_resumes(request.user)
# Extracts data from each resume one by one

# Process specific resumes
resume_ids = [1, 2, 3]
result = ResumeUploadService.process_pending_resumes(request.user, resume_ids)
```

### 3. REST API Usage
```python
from App.services.resume_processing_service import ResumeProcessingService

# Initialize service
service = ResumeProcessingService()

# Process single resume
result = service.process_resume(
    file_path='/absolute/path/to/resume.pdf',
    user=user_instance,
    resume_record_id=123
)

if result['success']:
    extracted_data = result['extracted_data']
    print(f"Extracted {extracted_data['metadata']['total_skills']} skills")
else:
    print(f"Error: {result['error']}")
```

### 4. Background Task/Celery
```python
from App.services.resume_processing_service import ResumeProcessingService
from App.models import ResumeProcessing

# Get pending resumes
pending_resumes = ResumeProcessing.objects.filter(status='pending')

# Process in batch
service = ResumeProcessingService()
results = service.process_multiple_resumes(
    resume_records=list(pending_resumes),
    verbose=True  # Print progress
)

print(f"Processed: {results['successful']}/{results['total']}")
```

## New Features Added

### 1. RPO Dashboard - Process All Pending Button
**Template:** `templates/Pages/RPO-Admin/dashboard.html`

```html
{% if stats.pending > 0 %}
<form method="POST" action="{% url 'App:rpo_process_resumes' %}">
    {% csrf_token %}
    <button type="submit" class="btn btn-success">
        Process All Pending ({{ stats.pending }})
    </button>
</form>
{% endif %}
```

### 2. Resume View - Process Now Button
**Template:** `templates/Pages/RPO-Admin/resume_view.html`

```html
{% if resume.status == 'pending' or resume.status == 'failed' %}
<form method="POST" action="{% url 'App:rpo_process_single_resume' resume.id %}">
    {% csrf_token %}
    <button type="submit" class="btn btn-sm btn-success">
        Process Now
    </button>
</form>
{% endif %}
```

### 3. New URL Endpoints
**File:** `App/urls.py`

```python
# Process all pending resumes for user
path("rpo-process-resumes/", views.rpo_process_resumes, name="rpo_process_resumes"),

# Process single specific resume
path("rpo-process-resume/<int:resume_id>/", views.rpo_process_single_resume, name="rpo_process_single_resume"),
```

## Processing Workflow

### Single Resume Processing
```
1. User uploads resume → File saved to disk
2. Database record created (status='pending')
3. User clicks "Process Now" or "Process All Pending"
4. ResumeProcessingService.process_resume() called
5. Status updated to 'processing'
6. Text extracted from file
7. Data extraction:
   - Contact info (email, phone)
   - Skills identification
   - Named entity recognition
   - Text statistics
   - Sentiment analysis
8. Database updated with extracted data
9. Status updated to 'completed' or 'failed'
```

### Batch Processing (Multiple Resumes)
```
1. Multiple files uploaded → All saved to disk
2. Multiple database records created (all status='pending')
3. User clicks "Process All Pending"
4. ResumeProcessingService.process_multiple_resumes() called
5. For each resume:
   - Extract data
   - Update database
   - Track success/failure
6. Return summary: {total, successful, failed}
```

## Database Schema

### ResumeProcessing Model
```python
class ResumeProcessing(models.Model):
    user = ForeignKey(User)
    profile = ForeignKey(Profile, null=True)
    resume_path = CharField()  # Relative path
    original_filename = CharField()
    file_size = IntegerField()
    file_extension = CharField()
    
    # Processing status
    status = CharField()  # pending, processing, completed, failed
    processing_started_at = DateTimeField(null=True)
    processing_completed_at = DateTimeField(null=True)
    error_message = TextField(null=True)
    
    # Extracted data
    resume_text = TextField(null=True)
    resume_json = JSONField(null=True)  # Full extraction results
    extracted_skills = TextField(null=True)
    extracted_email = CharField(null=True)
    extracted_phone = CharField(null=True)
    years_of_experience = CharField(null=True)
    sentiment_score = FloatField(null=True)
    word_count = IntegerField(null=True)
    
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
```

## Error Handling

### File Validation Errors
- Invalid file type (not PDF, DOCX, DOC, TXT)
- File too large (> 10MB)
- No file provided

### Processing Errors
- File not found on disk
- Text extraction failed
- Text too short (< 50 characters)
- General processing exceptions

All errors are:
1. Logged to database (error_message field)
2. Status set to 'failed'
3. Returned in ApiResponse
4. Displayed to user via messages

## Benefits of This Architecture

### 1. Reusability
- Same processing logic for candidate profile and RPO bulk upload
- Can be used in REST APIs, views, background tasks, CLI commands
- No code duplication

### 2. Maintainability
- Single source of truth for resume processing
- Easy to update extraction logic in one place
- Clear separation of concerns

### 3. Flexibility
- Process single resume or batch
- Synchronous or asynchronous processing
- Works with any file path structure

### 4. Testability
- Service methods are pure functions
- Easy to unit test
- Mock dependencies easily

### 5. Scalability
- Can move to Celery tasks easily
- Supports batch processing
- Efficient database updates

## Testing

### Test Single Resume Processing
```bash
python manage.py shell

from App.services.resume_processing_service import ResumeProcessingService
from django.contrib.auth.models import User

user = User.objects.get(username='testuser')
service = ResumeProcessingService()

result = service.process_resume(
    file_path='/path/to/test/resume.pdf',
    user=user
)

print(result['success'])
print(result['extracted_data']['metadata'])
```

### Test Batch Processing
```bash
python manage.py process_resumes --user username
```

### Test via Web Interface
1. Login as RPO admin
2. Upload multiple resumes at `/rpo-resume-upload/`
3. Go to dashboard at `/rpo-dashboard/`
4. Click "Process All Pending" button
5. Check resume details for extracted data

## Future Enhancements

1. **Async Processing with Celery**
   - Move processing to background tasks
   - Show real-time progress with websockets

2. **Advanced Extraction**
   - Education history extraction
   - Work experience timeline
   - Certifications and awards

3. **Matching Engine**
   - Match resumes to job requirements
   - Scoring and ranking
   - AI-powered recommendations

4. **Bulk Operations**
   - Download multiple resumes as ZIP
   - Bulk delete
   - Bulk re-process

5. **Analytics Dashboard**
   - Processing statistics
   - Success/failure rates
   - Common extraction patterns

## Files Modified/Created

### Created:
- `App/services/resume_processing_service.py` - Generic processing service

### Modified:
- `App/services/resume_upload_service.py` - Added processing methods
- `App/views/rpo_admin_views.py` - Added processing endpoints
- `App/urls.py` - Added processing URLs
- `templates/Pages/RPO-Admin/dashboard.html` - Added process button
- `templates/Pages/RPO-Admin/resume_view.html` - Added process button

### Existing (Reused):
- `App/tasks_simple.py` - SimpleDocumentProcessor class
- `App/models.py` - ResumeProcessing model
- `App/management/commands/process_resumes.py` - CLI command

## Conclusion

This implementation provides a robust, reusable resume processing system that:
- ✅ Extracts data from resumes automatically
- ✅ Stores structured data in database
- ✅ Works with single and batch uploads
- ✅ Supports both Django templates and REST APIs
- ✅ Follows service layer pattern
- ✅ Handles errors gracefully
- ✅ Provides user feedback via UI
- ✅ Maintains code reusability and maintainability
