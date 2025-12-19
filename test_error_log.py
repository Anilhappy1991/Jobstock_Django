import os
import django
import sys

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Jobstock.settings')
django.setup()

from App.models import ErrorLog
import traceback
import hashlib

def generate_test_error():
    """Generate a test error and log it"""
    try:
        # Intentionally cause an error
        result = 10 / 0  # This will raise ZeroDivisionError
    except Exception as e:
        # Get error details
        tb = traceback.format_exc()
        tb_lines = traceback.extract_tb(sys.exc_info()[2])
        last_frame = tb_lines[-1]
        
        # Create error hash
        error_hash = hashlib.md5(
            f"{last_frame.filename}{last_frame.name}{last_frame.lineno}{type(e).__name__}".encode()
        ).hexdigest()
        
        # Log the error
        error_log = ErrorLog.objects.create(
            error_type=type(e).__name__,
            error_message=str(e),
            error_traceback=tb,
            error_hash=error_hash,
            file_path=last_frame.filename,
            function_name=last_frame.name,
            line_number=last_frame.lineno,
            severity='high',
            environment='development'
        )
        
        print("✓ Error logged successfully!")
        print(f"  Error ID: {error_log.id}")
        print(f"  Error Type: {error_log.error_type}")
        print(f"  Error Message: {error_log.error_message}")
        print(f"  File: {error_log.file_path}")
        print(f"  Function: {error_log.function_name}")
        print(f"  Line: {error_log.line_number}")
        return error_log.id

def query_error_logs():
    """Query and display error logs from database"""
    print("\n" + "="*80)
    print("QUERYING ERROR LOGS FROM DATABASE")
    print("="*80 + "\n")
    
    # Get all error logs
    errors = ErrorLog.objects.all().order_by('-created_at')
    
    if errors.exists():
        print(f"Total errors in database: {errors.count()}\n")
        
        for i, error in enumerate(errors, 1):
            print(f"--- Error #{i} ---")
            print(f"ID: {error.id}")
            print(f"Type: {error.error_type}")
            print(f"Message: {error.error_message}")
            print(f"File: {error.file_path}")
            print(f"Function: {error.function_name}")
            print(f"Line Number: {error.line_number}")
            print(f"Severity: {error.severity}")
            print(f"Occurrence Count: {error.occurrence_count}")
            print(f"First Occurred: {error.first_occurred}")
            print(f"Last Occurred: {error.last_occurred}")
            print(f"Resolved: {error.is_resolved}")
            print("-" * 80 + "\n")
    else:
        print("No errors found in database.")

if __name__ == "__main__":
    print("TESTING ERROR LOGGING SYSTEM")
    print("="*80 + "\n")
    
    # Generate and log a test error
    generate_test_error()
    
    # Query and display all errors
    query_error_logs()
