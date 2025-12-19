import sqlite3
from datetime import datetime

# Connect to database
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

print("TESTING ERROR LOGGING SYSTEM")
print("="*80 + "\n")

# Insert a test error log
print("Generating test error and logging to database...")

test_error_data = {
    'error_type': 'ZeroDivisionError',
    'error_message': 'division by zero',
    'error_traceback': 'Traceback (most recent call last):\n  File "test.py", line 10, in test_function\n    result = 10 / 0\nZeroDivisionError: division by zero',
    'error_hash': 'test_error_hash_12345',
    'file_path': 'test_script.py',
    'function_name': 'test_function',
    'line_number': 10,
    'request_method': 'GET',
    'request_path': '/test/',
    'request_data': '{}',
    'status_code': 500,
    'is_resolved': 0,
    'occurrence_count': 1,
    'severity': 'high',
    'environment': 'development',
    'first_occurred': datetime.now().isoformat(),
    'last_occurred': datetime.now().isoformat(),
    'created_at': datetime.now().isoformat(),
    'updated_at': datetime.now().isoformat()
}

cursor.execute("""
    INSERT INTO error_logs (
        error_type, error_message, error_traceback, error_hash,
        file_path, function_name, line_number,
        request_method, request_path, request_data,
        status_code, is_resolved, occurrence_count,
        severity, environment,
        first_occurred, last_occurred, created_at, updated_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", (
    test_error_data['error_type'],
    test_error_data['error_message'],
    test_error_data['error_traceback'],
    test_error_data['error_hash'],
    test_error_data['file_path'],
    test_error_data['function_name'],
    test_error_data['line_number'],
    test_error_data['request_method'],
    test_error_data['request_path'],
    test_error_data['request_data'],
    test_error_data['status_code'],
    test_error_data['is_resolved'],
    test_error_data['occurrence_count'],
    test_error_data['severity'],
    test_error_data['environment'],
    test_error_data['first_occurred'],
    test_error_data['last_occurred'],
    test_error_data['created_at'],
    test_error_data['updated_at']
))

conn.commit()
print("✓ Test error logged successfully!\n")

# Query error logs
print("="*80)
print("SELECT QUERY RESULTS FROM error_logs TABLE")
print("="*80 + "\n")

cursor.execute("""
    SELECT 
        id, error_type, error_message, file_path, 
        function_name, line_number, severity, 
        occurrence_count, first_occurred, last_occurred,
        is_resolved, environment
    FROM error_logs
    ORDER BY id DESC
""")

rows = cursor.fetchall()

if rows:
    print(f"Total errors found: {len(rows)}\n")
    
    for i, row in enumerate(rows, 1):
        print(f"--- Error #{i} ---")
        print(f"ID: {row[0]}")
        print(f"Error Type: {row[1]}")
        print(f"Error Message: {row[2]}")
        print(f"File Path: {row[3]}")
        print(f"Function Name: {row[4]}")
        print(f"Line Number: {row[5]}")
        print(f"Severity: {row[6]}")
        print(f"Occurrence Count: {row[7]}")
        print(f"First Occurred: {row[8]}")
        print(f"Last Occurred: {row[9]}")
        print(f"Resolved: {'Yes' if row[10] else 'No'}")
        print(f"Environment: {row[11]}")
        print("-" * 80 + "\n")
else:
    print("No errors found in database.")

conn.close()
