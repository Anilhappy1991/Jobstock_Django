# Tests Directory

This directory contains all test files for the Jobstock Django project.

## Test Files

- `test_auto_processing.py` - Tests for automated resume processing
- `test_resume_processing.py` - Resume processing unit tests
- `test_integration.py` - Integration tests
- `test_resume_results.json` - Test results data
- `test_resume.txt` - Sample test resume

## Running Tests

### Run all tests
```bash
python manage.py test
```

### Run specific test file
```bash
python -m pytest tests/test_resume_processing.py
```

### Run with coverage
```bash
pytest --cov=App tests/
```

## Writing Tests

Follow Django testing best practices:
- Use Django TestCase for database tests
- Use unittest.mock for external dependencies
- Write descriptive test names
- Include docstrings

## Test Data

Test data files are stored here for testing purposes. Do not commit sensitive or production data.
