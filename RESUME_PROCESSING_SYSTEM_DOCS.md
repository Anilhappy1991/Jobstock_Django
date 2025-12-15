# Resume Processing System - Complete Documentation

## Overview

This system automatically processes uploaded resumes, extracts structured data, and stores results in the database. It integrates seamlessly with the Django candidate profile system.

---

## Features

✅ **Automatic Processing**: Resumes are automatically queued for processing on upload  
✅ **Data Extraction**: Extracts skills, contact info, experience, entities, and sentiment  
✅ **Database Storage**: All extracted data stored in `ResumeProcessing` model  
✅ **Status Tracking**: Real-time status updates (pending → processing → completed/failed)  
✅ **Profile Integration**: Displays processing results on candidate profile page  
✅ **File Support**: PDF, DOCX, DOC, TXT files up to 5MB  
✅ **History Tracking**: Maintains history of all processed resumes per user  

---

## Database Model: ResumeProcessing

### Core Fields

| Field | Type | Description |
|-------|------|-------------|
| `user` | ForeignKey | User who uploaded the resume |
| `profile` | ForeignKey | User's profile (optional) |
| `resume_path` | CharField | Full path to resume file |
| `original_filename` | CharField | Original uploaded filename |
| `file_size` | IntegerField | File size in bytes |
| `file_extension` | CharField | .pdf, .docx, .doc, .txt |
| `status` | CharField | pending, processing, completed, failed |
| `resume_text` | TextField | Full extracted text content |
| `resume_json` | JSONField | Structured extracted data |

### Extracted Quick-Access Fields

| Field | Type | Description |
|-------|------|-------------|
| `extracted_skills` | TextField | Comma-separated list of skills |
| `extracted_email` | EmailField | Primary email from resume |
| `extracted_phone` | CharField | Primary phone number |
| `years_of_experience` | CharField | Years mentioned in resume |
| `sentiment_score` | FloatField | Sentiment polarity (-1 to 1) |
| `word_count` | IntegerField | Total word count |

### JSON Structure (resume_json field)

```json
{
  "contact_info": {
    "emails": ["user@example.com"],
    "phones": ["+1234567890"],
    "linkedin": ["linkedin.com/in/user"],
    "github": ["github.com/user"]
  },
  "skills": {
    "total_skills": 19,
    "skills": ["Python", "Django", "React", "AWS", ...],
    "experience_years": [14, 5, 3]
  },
  "entities": {
    "total_entities": 153,
    "persons": ["John Doe", ...],
    "organizations": ["Google", "Microsoft", ...],
    "locations": ["New York", "California", ...]
  },
  "statistics": {
    "character_count": 7497,
    "word_count": 1313,
    "sentence_count": 27,
    "unique_words": 393,
    "most_common_words": [
      {"word": "python", "count": 4},
      ...
    ]
  },
  "sentiment": {
    "sentiment_label": "positive",
    "polarity": 0.156,
    "subjectivity": 0.381
  }
}
```

---

## Workflow

### 1. Resume Upload (Automatic Entry Creation)

**Location**: `App/views.py` - `candidate_profile_detail()` function

When a candidate uploads a resume through the profile page:

```python
# In views.py - resume upload handling
if 'resume' in request.FILES:
    resume_file = request.FILES['resume']
    ResumeProcessing.objects.create(
        user=request.user,
        profile=profile,
        resume_path=saved_profile.resume.path,
        original_filename=resume_file.name,
        file_size=resume_file.size,
        file_extension=os.path.splitext(resume_file.name)[1].lower(),
        status='pending'  # ← Initial status
    )
```

**Result**: Database entry created with `status='pending'`

### 2. Processing Methods

You have **3 options** to process pending resumes:

#### Option A: Management Command (Recommended)

```bash
# Process all pending resumes
python manage.py process_resumes

# Process for specific user
python manage.py process_resumes --user john_doe

# Reprocess all (including completed)
python manage.py process_resumes --all
```

**Best for**: Scheduled cron jobs, manual processing, CI/CD pipelines

#### Option B: Automatic File Watcher

```bash
# Start the file watcher (runs continuously)
python auto_process_resumes.py
```

**Best for**: Development, real-time processing, monitoring folder drops

#### Option C: Celery Background Tasks (Future Enhancement)

```python
# In views.py (after implementing Celery tasks)
from App.tasks_simple import process_resume_simple

if 'resume' in request.FILES:
    # ... create ResumeProcessing record ...
    
    # Trigger async processing
    process_resume_simple.delay(resume_record.id)
```

**Best for**: Production environments with high volume

### 3. Status Updates

The processing flow updates the status automatically:

1. **pending** → Record created, awaiting processing
2. **processing** → Processing started, `processing_started_at` set
3. **completed** → Success, all data extracted and saved
4. **failed** → Error occurred, check `error_message` field

### 4. Viewing Results

**Candidate Profile Page**: `templates/pages/candidate-profile.html`

Shows:
- Latest processing status badge
- Extracted skills count, word count, experience years, sentiment
- List of all extracted skills as badges
- Contact information found
- Processing history table

**Django Admin**: `/admin/App/resumeprocessing/`

Full admin interface to:
- View all processing records
- Filter by status, user, date
- Search by filename, email, phone
- View complete JSON data
- Manually update records

---

## File Structure

```
Jobstock_Django/
├── App/
│   ├── models.py              # ResumeProcessing model
│   ├── views.py               # Upload handling + status display
│   ├── admin.py               # Admin interface
│   ├── tasks_simple.py        # Processing logic (SimpleDocumentProcessor)
│   ├── management/
│   │   └── commands/
│   │       └── process_resumes.py  # Management command
│   └── migrations/
│       └── 0008_resumeprocessing.py  # Database migration
│
├── templates/pages/
│   └── candidate-profile.html  # Profile page with status display
│
├── data/candidate-resume/
│   ├── process/               # Processed files moved here
│   └── results/               # JSON/TXT extraction results
│
├── auto_process_resumes.py    # File watcher script
├── test_integration.py        # Integration test
└── process_resume_folder.py   # Batch processing script
```

---

## Usage Examples

### Example 1: Upload Resume via Django

1. Login as candidate
2. Go to Profile → Resume Upload
3. Select PDF/DOCX file and click "Upload Resume"
4. Success message: "Resume uploaded successfully! Processing will start automatically."
5. Record created with `status='pending'`

### Example 2: Process Pending Resumes

```bash
# Run the management command
python manage.py process_resumes
```

**Output**:
```
================================================================================
PROCESSING PENDING RESUMES
================================================================================

Found 1 resume(s) to process.

--------------------------------------------------------------------------------
Processing: john_resume.pdf
User: john_doe
Status: pending
✅ Successfully processed!
   Skills: 19
   Words: 1313
   Sentiment: positive

================================================================================
PROCESSING COMPLETE
================================================================================
✅ Successfully processed: 1
❌ Failed: 0
📊 Total: 1
```

### Example 3: Query Processed Resumes

```python
from App.models import ResumeProcessing

# Get all completed resumes for a user
completed = ResumeProcessing.objects.filter(
    user__username='john_doe',
    status='completed'
).order_by('-created_at')

# Access extracted data
for record in completed:
    print(f"File: {record.original_filename}")
    print(f"Skills: {record.resume_json['skills']['skills']}")
    print(f"Email: {record.extracted_email}")
    print(f"Words: {record.word_count}")
    print(f"Sentiment: {record.resume_json['sentiment']['sentiment_label']}")
```

### Example 4: Get Latest Resume for User

```python
latest = ResumeProcessing.objects.filter(
    user=request.user,
    status='completed'
).order_by('-created_at').first()

if latest:
    skills_count = latest.resume_json['skills']['total_skills']
    sentiment = latest.resume_json['sentiment']['sentiment_label']
```

---

## Admin Interface

### Viewing Records

1. Login to Django admin: `/admin/`
2. Navigate to: **App** → **Resume Processings**

### List View Shows:
- User
- Original filename
- Status (colored badge)
- File size
- Word count
- Created date
- Processing completion date

### Detail View Sections:
1. **User Information**: User, Profile
2. **File Information**: Path, filename, size, extension
3. **Processing Status**: Status, timestamps, error message
4. **Extracted Data**: Full text, JSON (collapsible)
5. **Quick Access Fields**: Skills, email, phone, experience, sentiment

### Filtering & Searching:
- Filter by: Status, Created date
- Search: Username, filename, email, phone

---

## Scheduled Processing (Production)

### Option 1: Cron Job (Linux/Mac)

```bash
# Edit crontab
crontab -e

# Add line to process every 5 minutes
*/5 * * * * cd /path/to/Jobstock_Django && /path/to/venv/bin/python manage.py process_resumes >> /var/log/resume_processing.log 2>&1
```

### Option 2: Windows Task Scheduler

1. Open Task Scheduler
2. Create Basic Task
3. Trigger: Daily, repeat every 5 minutes
4. Action: Start a program
   - Program: `C:\path\to\venv\Scripts\python.exe`
   - Arguments: `manage.py process_resumes`
   - Start in: `C:\path\to\Jobstock_Django`

### Option 3: Celery Beat (Best for High Volume)

```python
# In settings.py
from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    'process-pending-resumes': {
        'task': 'App.tasks.process_pending_resumes',
        'schedule': crontab(minute='*/5'),  # Every 5 minutes
    },
}
```

---

## Testing

### Test Integration

```bash
python test_integration.py
```

**Tests**:
- ✅ User and profile creation
- ✅ ResumeProcessing record creation
- ✅ Status transitions (pending → processing → completed)
- ✅ Data extraction and storage
- ✅ JSON structure validation
- ✅ Query operations

### Test with Real Upload

1. Start Django server: `python manage.py runserver`
2. Login as candidate
3. Upload resume through profile page
4. Run: `python manage.py process_resumes`
5. Refresh profile page to see results

---

## Troubleshooting

### Issue: Status stuck on "pending"

**Solution**: Run the processing command
```bash
python manage.py process_resumes
```

### Issue: "File not found" error

**Cause**: Resume file was moved or deleted after upload

**Solution**: Update `resume_path` in database or re-upload

### Issue: No skills extracted

**Possible Causes**:
- Resume format is image-based PDF (no text layer)
- Resume is encrypted
- Text extraction failed

**Solution**: Check `resume_text` field for content. If empty, file couldn't be parsed.

### Issue: Timezone warnings

**Solution**: Use `django.utils.timezone.now()` instead of `datetime.now()`

---

## Performance Considerations

### Batch Processing

```python
# Process in chunks to avoid memory issues
CHUNK_SIZE = 50
pending = ResumeProcessing.objects.filter(status='pending')
for i in range(0, pending.count(), CHUNK_SIZE):
    chunk = pending[i:i+CHUNK_SIZE]
    for record in chunk:
        # Process...
```

### Async with Celery

For high-volume sites, implement Celery tasks:

```python
# In tasks_simple.py
@shared_task
def process_resume_record(record_id):
    record = ResumeProcessing.objects.get(id=record_id)
    # ... processing logic ...
```

---

## API Endpoints (Future Enhancement)

### Get Processing Status

```python
# In urls.py
path('api/resume-status/<int:pk>/', views.resume_status_api, name='resume_status_api'),

# In views.py
@login_required
def resume_status_api(request, pk):
    record = get_object_or_404(ResumeProcessing, pk=pk, user=request.user)
    return JsonResponse({
        'status': record.status,
        'progress': 100 if record.status == 'completed' else 0,
        'skills_count': record.resume_json.get('skills', {}).get('total_skills', 0) if record.resume_json else 0,
        'error': record.error_message
    })
```

---

## Security Notes

- ✅ Only authenticated users can upload resumes
- ✅ Users can only view their own processing records
- ✅ File type and size validated on upload
- ✅ Paths sanitized to prevent directory traversal
- ⚠️ Consider encrypting sensitive data in `resume_text` field
- ⚠️ Consider GDPR compliance for storing resume content

---

## Maintenance

### Clean Up Old Records

```python
# Delete processed resumes older than 1 year
from datetime import timedelta
from django.utils import timezone

cutoff = timezone.now() - timedelta(days=365)
ResumeProcessing.objects.filter(
    created_at__lt=cutoff,
    status='completed'
).delete()
```

### Monitor Failed Processing

```python
# Get failed processing attempts
failed = ResumeProcessing.objects.filter(status='failed')
for record in failed:
    print(f"{record.user.username}: {record.error_message}")
```

---

## Summary

This system provides a complete, production-ready solution for resume processing with:

1. **Seamless Integration**: Works with existing Django profile system
2. **Flexible Processing**: Multiple processing methods (command, watcher, Celery)
3. **Rich Data Extraction**: Skills, contacts, entities, sentiment, statistics
4. **User-Friendly**: Status display on profile page with visual indicators
5. **Admin-Friendly**: Comprehensive admin interface for monitoring
6. **Scalable**: Ready for async processing with Celery

**Next Steps**:
- Enable automatic background processing with Celery
- Add email notifications when processing completes
- Implement resume-to-job matching based on extracted skills
- Create analytics dashboard for HR team
