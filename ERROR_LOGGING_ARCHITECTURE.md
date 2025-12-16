# ERROR LOGGING SYSTEM - Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         DJANGO APPLICATION                                   │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                          VIEW LAYER                                   │  │
│  │                                                                       │  │
│  │  def my_view(request):                                               │  │
│  │      result = 10 / 0  ← Exception occurs!                           │  │
│  │                                                                       │  │
│  └──────────────────────────┬───────────────────────────────────────────┘  │
│                             │                                               │
│                             ↓                                               │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                    MIDDLEWARE LAYER                                   │  │
│  │                                                                       │  │
│  │  ErrorLoggingMiddleware.process_exception()                          │  │
│  │      ├─ Extract exception details                                    │  │
│  │      ├─ Get traceback                                                │  │
│  │      ├─ Find internal frame (filter libraries)                       │  │
│  │      │   ├─ ✅ App/ → INTERNAL (log this)                           │  │
│  │      │   ├─ ✅ Jobstock/ → INTERNAL (log this)                      │  │
│  │      │   ├─ ❌ site-packages/ → LIBRARY (skip)                      │  │
│  │      │   └─ ❌ django/ → FRAMEWORK (skip)                           │  │
│  │      ├─ Extract: file, function, line number                        │  │
│  │      ├─ Get request data (filter sensitive fields)                  │  │
│  │      ├─ Get user info (if authenticated)                            │  │
│  │      ├─ Generate error hash for deduplication                       │  │
│  │      └─ Save to database                                            │  │
│  │                                                                       │  │
│  └──────────────────────────┬───────────────────────────────────────────┘  │
│                             │                                               │
│                             ↓                                               │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                     DATABASE LAYER                                    │  │
│  │                                                                       │  │
│  │  error_hash = SHA256(file + function + line + type)                 │  │
│  │                                                                       │  │
│  │  ┌─── Check if error exists? ──────────────────────────────────┐    │  │
│  │  │                                                              │    │  │
│  │  │  YES: Existing Error Found                                  │    │  │
│  │  │  ├─ occurrence_count += 1                                   │    │  │
│  │  │  ├─ last_occurred = NOW                                     │    │  │
│  │  │  └─ Save (update)                                           │    │  │
│  │  │                                                              │    │  │
│  │  │  NO: New Error                                              │    │  │
│  │  │  ├─ Create ErrorLog record                                  │    │  │
│  │  │  ├─ occurrence_count = 1                                    │    │  │
│  │  │  ├─ first_occurred = NOW                                    │    │  │
│  │  │  ├─ last_occurred = NOW                                     │    │  │
│  │  │  └─ Save (insert)                                           │    │  │
│  │  │                                                              │    │  │
│  │  └──────────────────────────────────────────────────────────────┘    │  │
│  │                                                                       │  │
│  │  ErrorLog Table:                                                     │  │
│  │  ┌─────────────────────────────────────────────────────────────┐    │  │
│  │  │ id | error_type | file_path | function_name | line_number  │    │  │
│  │  │ 1  | ValueError | App/views.py | my_view | 123             │    │  │
│  │  │ 2  | KeyError   | App/utils.py | process | 45              │    │  │
│  │  └─────────────────────────────────────────────────────────────┘    │  │
│  │                                                                       │  │
│  └───────────────────────────────────────────────────────────────────────┘ │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────────────┐
│                          MANUAL LOGGING                                      │
│                                                                              │
│  from App.utils import log_error                                            │
│                                                                              │
│  def my_function(request):                                                  │
│      try:                                                                   │
│          risky_operation()                                                  │
│      except Exception as e:                                                 │
│          log_error(e, request=request, severity='high')  ← Manual log      │
│                                                                              │
│  ↓                                                                           │
│  log_error() function                                                       │
│      ├─ Extract exception details                                           │
│      ├─ Get traceback                                                       │
│      ├─ Find internal frame                                                 │
│      ├─ Generate error hash                                                 │
│      ├─ Check for existing error                                            │
│      └─ Save to database                                                    │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────────────┐
│                          ADMIN INTERFACE                                     │
│                                                                              │
│  http://localhost:8000/admin/App/errorlog/                                 │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────┐    │
│  │  ERROR LOGS                                                         │    │
│  │                                                                     │    │
│  │  Filters:                      Search:                              │    │
│  │  [ ] Severity                  [____________________] [Search]     │    │
│  │  [ ] Status                                                         │    │
│  │  [ ] Date                      Actions:                             │    │
│  │                                [ ] Mark as resolved                 │    │
│  │  ┌─────────────────────────────────────────────────────────────┐   │    │
│  │  │ Type       │ Message      │ Function │ Line │ Occurred     │   │    │
│  │  ├─────────────────────────────────────────────────────────────┤   │    │
│  │  │ ValueError │ Invalid data │ my_view  │ 123  │ 2 mins ago   │   │    │
│  │  │ KeyError   │ Missing key  │ process  │ 45   │ 5 mins ago   │   │    │
│  │  │ TypeError  │ Wrong type   │ handler  │ 67   │ 10 mins ago  │   │    │
│  │  └─────────────────────────────────────────────────────────────┘   │    │
│  │                                                                     │    │
│  │  Click row to view:                                                 │    │
│  │  - Full traceback                                                   │    │
│  │  - Request details                                                  │    │
│  │  - User information                                                 │    │
│  │  - Resolution options                                               │    │
│  │                                                                     │    │
│  └────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────────────┐
│                      DATA FLOW DIAGRAM                                       │
│                                                                              │
│  Request → View → Exception                                                 │
│      ↓                                                                       │
│  Middleware → Extract Details                                               │
│      ↓                                                                       │
│  Filter → Internal Code Only                                                │
│      ↓                                                                       │
│  Hash → Check Duplicate                                                     │
│      ↓                                                                       │
│  Database → Save/Update                                                     │
│      ↓                                                                       │
│  Admin → View/Manage                                                        │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────────────┐
│                     ERROR FILTERING LOGIC                                    │
│                                                                              │
│  Traceback:                                                                 │
│    Frame 1: site-packages/django/core/handlers/base.py ← SKIP (library)    │
│    Frame 2: site-packages/django/views/generic/base.py ← SKIP (library)    │
│    Frame 3: App/views.py (my_view, line 123)          ← LOG THIS! ✅       │
│    Frame 4: App/utils.py (helper, line 45)            ← Also internal      │
│                                                                              │
│  Selected Frame: Frame 3 (first internal frame)                             │
│    file_path: App/views.py                                                  │
│    function_name: my_view                                                   │
│    line_number: 123                                                         │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────────────┐
│                    DEDUPLICATION EXAMPLE                                     │
│                                                                              │
│  Time 10:00 - Error Occurs:                                                 │
│    ZeroDivisionError in App/views.py:123 (my_view)                         │
│    Hash: abc123... → NEW ERROR                                              │
│    Database: Create record (ID=1, occurrence_count=1)                       │
│                                                                              │
│  Time 10:05 - Same Error Occurs:                                            │
│    ZeroDivisionError in App/views.py:123 (my_view)                         │
│    Hash: abc123... → EXISTING ERROR FOUND!                                  │
│    Database: Update record (ID=1, occurrence_count=2, last_occurred=now)   │
│                                                                              │
│  Time 10:10 - Same Error Occurs:                                            │
│    ZeroDivisionError in App/views.py:123 (my_view)                         │
│    Hash: abc123... → EXISTING ERROR FOUND!                                  │
│    Database: Update record (ID=1, occurrence_count=3, last_occurred=now)   │
│                                                                              │
│  Result: 1 database record with occurrence_count=3                          │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────────────┐
│                    SECURITY: SENSITIVE DATA FILTERING                        │
│                                                                              │
│  Original Request Data:                                                     │
│  {                                                                           │
│      'username': 'john_doe',                                                │
│      'password': 'secret123',      ← SENSITIVE!                            │
│      'email': 'john@example.com',                                           │
│      'api_key': 'xyz789',          ← SENSITIVE!                            │
│      'city': 'New York'                                                     │
│  }                                                                           │
│                                                                              │
│  ↓ Filter Sensitive Fields                                                  │
│                                                                              │
│  Stored in Database:                                                        │
│  {                                                                           │
│      'username': 'john_doe',                                                │
│      'password': '***FILTERED***',  ← PROTECTED! ✅                        │
│      'email': 'john@example.com',                                           │
│      'api_key': '***FILTERED***',   ← PROTECTED! ✅                        │
│      'city': 'New York'                                                     │
│  }                                                                           │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────────────┐
│                        COMPONENT INTERACTION                                 │
│                                                                              │
│                        ┌─────────────┐                                      │
│                        │   REQUEST   │                                      │
│                        └──────┬──────┘                                      │
│                               │                                             │
│                               ↓                                             │
│                        ┌─────────────┐                                      │
│                        │    VIEW     │                                      │
│                        └──────┬──────┘                                      │
│                               │                                             │
│                        ┌──────┴──────┐                                      │
│                        │             │                                      │
│                   Exception     Manual log_error()                          │
│                        │             │                                      │
│                        ↓             ↓                                      │
│              ┌──────────────────────────────┐                               │
│              │    ERROR PROCESSING          │                               │
│              │  (Middleware or Utility)     │                               │
│              └──────────┬───────────────────┘                               │
│                         │                                                   │
│          ┌──────────────┼──────────────┐                                    │
│          ↓              ↓              ↓                                    │
│   ┌──────────┐   ┌──────────┐   ┌──────────┐                               │
│   │ Extract  │   │  Filter  │   │ Generate │                               │
│   │ Details  │   │ Internal │   │   Hash   │                               │
│   └────┬─────┘   └────┬─────┘   └────┬─────┘                               │
│        │              │              │                                      │
│        └──────────────┴──────────────┘                                      │
│                       │                                                     │
│                       ↓                                                     │
│              ┌─────────────────┐                                            │
│              │    DATABASE     │                                            │
│              │   (ErrorLog)    │                                            │
│              └────────┬────────┘                                            │
│                       │                                                     │
│                       ↓                                                     │
│              ┌─────────────────┐                                            │
│              │  ADMIN PANEL    │                                            │
│              │  (View/Manage)  │                                            │
│              └─────────────────┘                                            │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

## File Structure

```
Jobstock_Django/
│
├── App/
│   ├── models.py                    ← ErrorLog model (28 fields)
│   ├── middleware.py                ← ErrorLoggingMiddleware (NEW)
│   ├── utils.py                     ← log_error(), get_last_error(), etc.
│   ├── admin.py                     ← ErrorLogAdmin (enhanced)
│   ├── views.py                     ← Your views (unchanged)
│   │
│   └── migrations/
│       └── 0009_errorlog.py         ← Database migration (NEW)
│
├── Jobstock/
│   └── settings.py                  ← Middleware registered
│
├── ERROR_LOGGING_GUIDE.md           ← Complete documentation (NEW)
├── ERROR_LOGGING_QUICK_REFERENCE.md ← Quick reference (NEW)
├── ERROR_LOGGING_ARCHITECTURE.md    ← This file (NEW)
└── test_error_logging.py            ← Test suite (NEW)
```

## Component Responsibilities

| Component | Responsibility | Type |
|-----------|---------------|------|
| **ErrorLog Model** | Data structure, methods, database schema | Model |
| **ErrorLoggingMiddleware** | Automatic error capture, filtering, processing | Middleware |
| **log_error()** | Manual error logging, deduplication | Utility |
| **get_last_error()** | Retrieve most recent error | Utility |
| **get_error_summary()** | Error statistics and analytics | Utility |
| **ErrorLogAdmin** | View, manage, export errors | Admin |

## System Benefits

✅ **Automatic** - No code changes needed in views
✅ **Smart** - Filters out library errors automatically  
✅ **Efficient** - Deduplicates errors by hash
✅ **Secure** - Filters sensitive data
✅ **Comprehensive** - Tracks 28+ fields per error
✅ **Manageable** - Full admin interface
✅ **Flexible** - Manual logging available
✅ **Production-Ready** - Tested and documented
