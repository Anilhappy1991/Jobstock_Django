# Scripts Directory

Utility scripts for the Jobstock Django project.

## Directory Structure

### resume_processing/
Scripts for processing candidate resumes:
- `auto_process_resumes.py` - Batch process resumes automatically
- `process_resume_folder.py` - Process all resumes in a folder
- `extract_resume_data.py` - Extract structured data from resumes
- `diagnose_resumes.py` - Diagnose resume processing issues
- `run_processing.py` - Main resume processing runner

**Usage:**
```bash
python scripts/resume_processing/auto_process_resumes.py
```

### utilities/
General utility scripts:
- `check_records.py` - Check database records integrity
- `check_users.py` - Verify user accounts
- `create_project_excel.py` - Generate project Excel reports
- `verify_dropdowns.py` - Verify dropdown data consistency

**Usage:**
```bash
python scripts/utilities/check_users.py
```

## Running Scripts

All scripts should be run from the project root directory:

```bash
# From project root
cd C:\RandR\Jobstock_Django_v1.0.0\Jobstock_Django

# Run a script
python scripts/resume_processing/auto_process_resumes.py
```

## Adding New Scripts

1. Place scripts in appropriate subdirectory
2. Add docstrings and usage instructions
3. Update this README
4. Test thoroughly before committing
