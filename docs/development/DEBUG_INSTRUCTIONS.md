# Debug Instructions for Job Submission

## Server-Side Debugging

### Debug Logs Location
All debug logs are written to two places:
1. **Console/Terminal** - Where you run `python manage.py runserver`
2. **Log File** - `debug.log` in the project root directory

### What Gets Logged
When you submit a job, the following information is automatically logged:

1. **Initial Request**
   - HTTP Method (GET/POST)
   - Current user and authentication status

2. **Form Submission (POST)**
   - All POST data fields and their values
   - Uploaded files (name and size)
   - Dropdown selections

3. **Job Creation**
   - Job title
   - Company logo (if uploaded)
   - Salary range
   - All field values being saved

4. **Database Save**
   - Success confirmation with Job ID
   - Or error details with full traceback

### How to View Debug Logs

#### Method 1: Terminal Output
```bash
# Run the development server
python manage.py runserver

# Watch the terminal for logs when you submit a job
# Look for lines starting with [INFO] or [ERROR]
```

#### Method 2: Log File
```bash
# View the log file in real-time
Get-Content debug.log -Wait -Tail 50

# Or open debug.log in VS Code
code debug.log
```

### Example Debug Output
```
================================================================================
[INFO] 2025-12-19 10:30:45 views EMPLOYER SUBMIT JOB VIEW CALLED
[INFO] 2025-12-19 10:30:45 views Method: POST
[INFO] 2025-12-19 10:30:45 views User: admin
[INFO] 2025-12-19 10:30:45 views Authenticated: True
--------------------------------------------------------------------------------
[INFO] 2025-12-19 10:30:45 views POST REQUEST RECEIVED - FORM SUBMITTED
[INFO] 2025-12-19 10:30:45 views POST Data:
[INFO] 2025-12-19 10:30:45 views   job_title: Senior Python Developer
[INFO] 2025-12-19 10:30:45 views   job_category: software_development
[INFO] 2025-12-19 10:30:45 views   min_salary: 50000
--------------------------------------------------------------------------------
[INFO] 2025-12-19 10:30:45 views CREATING JOB OBJECT
[INFO] 2025-12-19 10:30:45 views Job Title: Senior Python Developer
[INFO] 2025-12-19 10:30:45 views Salary Range: $50000 - $80000
--------------------------------------------------------------------------------
[INFO] 2025-12-19 10:30:45 views SAVING JOB TO DATABASE
[INFO] 2025-12-19 10:30:45 views ✓ JOB SAVED SUCCESSFULLY - ID: 42
================================================================================
```

## Client-Side Debugging (Browser)

### Debug Button Features
Click the yellow "Debug Save" button to:
1. View form data in browser console (F12)
2. See alert with job title, category, and type
3. Optionally submit the form after review

### How to Use
1. Fill out the job submission form
2. Click "Debug Save" button (yellow)
3. Check browser alert for basic info
4. Press F12 to open Developer Tools
5. Go to "Console" tab
6. Review all form field values
7. Click OK in the confirmation dialog to submit

### Browser Console Output
```javascript
=== DEBUG: Form Data ===
job_title: Senior Python Developer
job_category: software_development
job_type: full_time
min_salary: 50000
max_salary: 80000
...
```

## Troubleshooting

### No Logs Appearing?
1. Check if DEBUG=True in settings.py
2. Restart the development server
3. Check file permissions for debug.log

### Form Not Submitting?
1. Check browser console for JavaScript errors
2. Review debug.log for server-side errors
3. Verify all required fields are filled

### Debug Breakpoints
The code includes marked sections:
```python
# ===== DEBUG BREAKPOINT START =====
# ... debug code here ...
# ===== DEBUG BREAKPOINT END =====
```

You can add additional logging or set IDE breakpoints at these locations.

## IDE Debugging (VS Code)

To set actual breakpoints in VS Code:

1. Open `App/views.py`
2. Find `employer_submit_job` function (line ~453)
3. Click left margin to set breakpoint at lines:
   - Line 465: When POST request starts
   - Line 510: Before saving to database
   - Line 520: After successful save
   - Line 528: Error handling

4. Run Django with debugger:
   - Press F5 or go to Run > Start Debugging
   - Select "Python: Django" configuration

5. Submit a job and code will pause at breakpoints

## Tips
- Keep terminal visible while testing to see real-time logs
- Use browser console for front-end validation
- Check debug.log for historical debugging data
- Clear debug.log periodically to avoid large files
