import sqlite3

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# Check for error_logs table
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE '%error%';")
print("Tables with 'error' in name:", cursor.fetchall())

# List all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
all_tables = cursor.fetchall()
print("\nAll tables in database:")
for table in all_tables:
    print(f"  - {table[0]}")

conn.close()
