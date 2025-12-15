# Candidate Resume Storage

This directory stores uploaded candidate resumes.

## Supported File Formats
- **PDF** (.pdf) - Recommended format
- **Microsoft Word** (.doc, .docx)
- **Plain Text** (.txt)

## File Size Limit
Maximum file size: **5 MB**

## File Naming
Files are automatically named by Django using the format:
- `{original_filename}_{random_hash}.{extension}`

## Security Notes
- All uploaded files are validated for type and size
- Only authenticated users can upload resumes
- Files are stored outside the web root for security
- Access to files is controlled through Django views

## Directory Structure
```
data/
└── candidate-resume/
    ├── README.md (this file)
    └── {user uploaded resumes}
```

## Important
- Do not manually edit or delete files in this directory
- Ensure proper file permissions are set in production
- Regular backups should include this directory
