# Jobstock Django - Job Recruitment Platform

A comprehensive Django-based recruitment platform for managing jobs, candidates, employers, and resume processing.

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+ ([Download](https://www.python.org/downloads/))
- pip package manager ([Install](https://pypi.org/project/pip/))
- Docker Desktop (optional, for containerized deployment)

### Installation

1. **Create virtual environment**
   ```bash
   python -m venv venv0
   # Windows
   venv0\Scripts\activate
   # Linux/Mac
   source venv0/bin/activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run migrations**
   ```bash
   python manage.py migrate
   ```

4. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

5. **Run development server**
   ```bash
   python manage.py runserver
   ```

6. **Access the application**
   - Application: http://localhost:8000
   - Admin Panel: http://localhost:8000/admin

---

## 🐳 Docker Deployment

For containerized deployment with separated frontend/backend:

```bash
# Windows
setup-docker.bat

# Linux/Mac
chmod +x setup-docker.sh && ./setup-docker.sh
```

**📖 See:** [docs/START_HERE.md](docs/START_HERE.md) for complete Docker documentation

---

## 📁 Project Structure

```
Jobstock_Django/
├── App/                          # Main Django application
├── Jobstock/                     # Django project settings
├── core/                         # Core utilities
├── static/                       # Static files (CSS, JS, images)
├── templates/                    # HTML templates
├── data/                         # Media and uploads
├── docs/                         # 📚 All Documentation
│   ├── START_HERE.md             # Documentation index
│   ├── docker/                   # Docker setup docs
│   ├── setup/                    # Setup & guides
│   └── development/              # Development docs
├── scripts/                      # 🔧 Utility scripts
│   ├── resume_processing/        # Resume processing
│   └── utilities/                # General utilities
├── tests/                        # 🧪 Test files
├── manage.py                     # Django management
├── requirements.txt              # Dependencies
└── README.md                     # This file
```

---

## 🎯 Key Features

### For Job Seekers (Candidates)
- ✅ Create and manage profile
- ✅ Upload and parse resumes (PDF, DOCX, TXT)
- ✅ Search and browse job listings
- ✅ Apply for jobs
- ✅ Track application status

### For Employers
- ✅ Post job openings
- ✅ Manage job listings
- ✅ Review candidate applications
- ✅ Download candidate resumes

### Resume Processing
- ✅ Automatic resume parsing
- ✅ Extract candidate information
- ✅ Support for multiple formats

---

## 📚 Documentation

All documentation is organized in the **`docs/`** folder:

### 📖 Start Here
- **[docs/START_HERE.md](docs/START_HERE.md)** - Complete documentation index

### 🐳 Docker Setup
- [Docker Quick Start](docs/docker/) - Fast setup
- [Frontend Guide](docs/docker/) - For UI developers
- [Commands Reference](docs/docker/) - All commands

### 💻 Development
- [Setup Guides](docs/setup/) - Installation guides
- [Development Docs](docs/development/) - Coding guidelines

---

## 🔧 Scripts

All scripts are organized in the **`scripts/`** folder:

### Resume Processing (`scripts/resume_processing/`)
```bash
python scripts/resume_processing/auto_process_resumes.py
python scripts/resume_processing/extract_resume_data.py
```

### Utilities (`scripts/utilities/`)
```bash
python scripts/utilities/check_records.py
python scripts/utilities/check_users.py
```

---

## 🧪 Testing

All tests are in the **`tests/`** folder:

```bash
# Run all tests
python manage.py test

# Run specific test
python -m pytest tests/test_resume_processing.py
```

---

## 🛠️ Development

1. Create feature branch: `git checkout -b feature/name`
2. Make changes following PEP 8
3. Add tests for new features
4. Update documentation
5. Submit pull request

---

## 📞 Support

- **📚 Documentation:** [docs/START_HERE.md](docs/START_HERE.md)
- **🐛 Issues:** Create an issue in the repository
- **💬 Questions:** Check documentation first

---

**Version:** 1.0  
**Last Updated:** December 20, 2025  
**Status:** Active Development

---

## 🗺️ Quick Links

- **Application:** http://localhost:8000
- **Admin:** http://localhost:8000/admin
- **Documentation:** [docs/START_HERE.md](docs/START_HERE.md)
- **Docker Guide:** [docs/docker/](docs/docker/)
