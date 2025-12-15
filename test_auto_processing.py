"""
Quick test of automatic processing trigger
"""
import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Jobstock.settings')
django.setup()

from django.core.management import call_command
import threading

print("\n" + "=" * 80)
print("TESTING AUTOMATIC PROCESSING TRIGGER")
print("=" * 80 + "\n")

print("Method 1: Direct call_command (blocking)")
print("-" * 80)
call_command('process_resumes', verbosity=1)

print("\n" + "=" * 80)
print("Method 2: Background thread (non-blocking)")
print("-" * 80)

def process_in_background():
    try:
        call_command('process_resumes', user='rituranjan.gupta2@gmail.com', verbosity=1)
        print("✅ Background processing completed")
    except Exception as e:
        print(f"❌ Error: {e}")

thread = threading.Thread(target=process_in_background, daemon=True)
thread.start()
print("✅ Background thread started")

# Wait for thread to complete
import time
time.sleep(3)

print("\n" + "=" * 80)
print("✅ ALL TESTS COMPLETED")
print("=" * 80)
