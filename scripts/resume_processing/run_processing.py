"""
Different ways to run 'python manage.py process_resumes' programmatically
"""
import os
import sys
import subprocess
import threading
from pathlib import Path

# Get project paths
BASE_DIR = Path(__file__).parent
MANAGE_PY = BASE_DIR / 'manage.py'
PYTHON_EXE = sys.executable


# Method 1: Direct subprocess call (blocking)
def run_process_resumes_blocking(username=None):
    """
    Run the process_resumes command and wait for completion.
    Use this when you want to wait for processing to finish.
    """
    cmd = [PYTHON_EXE, str(MANAGE_PY), 'process_resumes']
    
    if username:
        cmd.extend(['--user', username])
    
    try:
        result = subprocess.run(
            cmd,
            cwd=str(BASE_DIR),
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        print("STDOUT:", result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print("Processing timed out after 5 minutes")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False


# Method 2: Background subprocess (non-blocking)
def run_process_resumes_background(username=None):
    """
    Run the process_resumes command in background without waiting.
    Use this in web views to avoid blocking the response.
    """
    cmd = [PYTHON_EXE, str(MANAGE_PY), 'process_resumes']
    
    if username:
        cmd.extend(['--user', username])
    
    try:
        subprocess.Popen(
            cmd,
            cwd=str(BASE_DIR),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True  # Detach from parent process
        )
        print(f"Processing started in background for user: {username or 'all'}")
        return True
    except Exception as e:
        print(f"Error starting background process: {e}")
        return False


# Method 3: Threading (non-blocking, with error handling)
def run_process_resumes_thread(username=None):
    """
    Run the process_resumes command in a separate thread.
    Use this when you want non-blocking execution with better error handling.
    """
    def process_in_thread():
        cmd = [PYTHON_EXE, str(MANAGE_PY), 'process_resumes']
        if username:
            cmd.extend(['--user', username])
        
        try:
            result = subprocess.run(
                cmd,
                cwd=str(BASE_DIR),
                capture_output=True,
                text=True,
                timeout=300
            )
            if result.returncode == 0:
                print(f"✅ Processing completed successfully for: {username or 'all users'}")
            else:
                print(f"❌ Processing failed with code: {result.returncode}")
                print(result.stderr)
        except Exception as e:
            print(f"❌ Thread processing error: {e}")
    
    thread = threading.Thread(target=process_in_thread, daemon=True)
    thread.start()
    print(f"Processing thread started for user: {username or 'all'}")
    return True


# Method 4: Direct Django management command call (within Django)
def run_process_resumes_django(username=None):
    """
    Call the management command directly using Django's call_command.
    Use this when already within a Django context (e.g., in views, signals).
    Requires: from django.core.management import call_command
    """
    try:
        from django.core.management import call_command
        
        kwargs = {}
        if username:
            kwargs['user'] = username
        
        call_command('process_resumes', **kwargs)
        print(f"✅ Processing completed for: {username or 'all users'}")
        return True
    except Exception as e:
        print(f"❌ Django command error: {e}")
        return False


# Method 5: Queue-based processing (best for production)
def run_process_resumes_queue(username=None):
    """
    Add processing task to a queue (Celery/Redis/RQ).
    Best for production with high volume.
    
    Example with Celery:
    from App.tasks import process_pending_resumes
    process_pending_resumes.delay(username=username)
    """
    print("⚠️  Queue-based processing requires Celery/Redis setup")
    print("   See: App/tasks_simple.py for Celery task implementation")
    return False


# Usage examples
if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Run resume processing')
    parser.add_argument('--method', choices=['blocking', 'background', 'thread', 'django'], 
                       default='thread', help='Processing method')
    parser.add_argument('--user', type=str, help='Process for specific user')
    
    args = parser.parse_args()
    
    print("=" * 80)
    print(f"RUNNING RESUME PROCESSING - Method: {args.method.upper()}")
    print("=" * 80)
    print()
    
    if args.method == 'blocking':
        success = run_process_resumes_blocking(args.user)
        print(f"\n{'✅ Success' if success else '❌ Failed'}")
    
    elif args.method == 'background':
        run_process_resumes_background(args.user)
        print("\n✅ Background process started (check logs for completion)")
    
    elif args.method == 'thread':
        run_process_resumes_thread(args.user)
        print("\n✅ Thread started (will complete in background)")
        # Keep main thread alive briefly to see results
        import time
        time.sleep(2)
    
    elif args.method == 'django':
        run_process_resumes_django(args.user)
    
    print("\nDone!")
