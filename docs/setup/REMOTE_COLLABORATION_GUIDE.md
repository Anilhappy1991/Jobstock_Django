# Remote Frontend Developer Setup Guide

## Overview
The HTML/CSS developer is in a **remote location** (different city/country), so they need internet-based access instead of local network sharing.

---

## 🌍 Best Solutions for Remote Collaboration

### ✅ **Option 1: Git Repository (RECOMMENDED)**
**Best for:** Most common, professional workflow  
**Cost:** Free  
**Setup time:** 15 minutes

### ✅ **Option 2: Cloud Django Hosting**
**Best for:** Live preview, easy access  
**Cost:** Free tier available  
**Setup time:** 30 minutes

### ✅ **Option 3: VS Code Live Share**
**Best for:** Real-time collaboration  
**Cost:** Free  
**Setup time:** 5 minutes

### ✅ **Option 4: ngrok Tunnel**
**Best for:** Quick demos, temporary access  
**Cost:** Free tier available  
**Setup time:** 5 minutes

---

## 🎯 SOLUTION 1: Git Repository (RECOMMENDED)

### Why This is Best:
- ✅ Professional workflow
- ✅ Version control built-in
- ✅ Multiple developers can work
- ✅ Free forever
- ✅ Industry standard
- ✅ No server maintenance

### How It Works:
```
┌─────────────────────┐
│  You (Backend)      │
│  • Python code      │
│  • Push to Git      │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  GitHub/GitLab      │
│  • templates/       │
│  • static/          │
│  • (no sensitive)   │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  Frontend Dev       │
│  • Clone repo       │
│  • Edit HTML/CSS    │
│  • Push changes     │
└─────────────────────┘
```

### Setup Steps:

#### A. Create Repository Structure

**1. Create a `.gitignore` file:**
```bash
# Create .gitignore if not exists
New-Item -Path .gitignore -ItemType File -Force
```

Add this content to `.gitignore`:
```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv*/
env/
ENV/

# Django
*.log
db.sqlite3
db.sqlite3-journal
/media
/staticfiles

# Sensitive files
*.env
.env
user-password.txt
*.pem
*.key

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Keep templates and static
!templates/
!static/
```

**2. Initialize Git (if not already):**
```bash
git init
git add .
git commit -m "Initial commit - Django project setup"
```

**3. Create GitHub Repository:**
- Go to https://github.com
- Click "New Repository"
- Name: `jobstock-django-frontend`
- Make it **Private** (recommended)
- Don't initialize with README (already have one)

**4. Push to GitHub:**
```bash
# Replace with your GitHub username
git remote add origin https://github.com/YOUR-USERNAME/jobstock-django-frontend.git
git branch -M main
git push -u origin main
```

#### B. Grant Frontend Developer Access

**Option 1: Add as Collaborator**
1. Go to repository → Settings → Collaborators
2. Click "Add people"
3. Enter developer's GitHub username
4. They get email invitation
5. They can clone repository

**Option 2: Use Deploy Keys (Read-Only)**
1. Repository → Settings → Deploy keys
2. Add their public SSH key
3. Uncheck "Allow write access" (read-only)

#### C. Frontend Developer Workflow

**Frontend developer does this:**

**1. Clone repository:**
```bash
git clone https://github.com/YOUR-USERNAME/jobstock-django-frontend.git
cd jobstock-django-frontend
```

**2. Work on files:**
```bash
# Edit files in templates/ and static/
# Use any editor: VS Code, Sublime, Notepad++
```

**3. See their work locally (Optional):**
```bash
# They can install Python and run Django locally
pip install -r requirements.txt
python manage.py runserver

# Or just edit and let you test
```

**4. Push changes:**
```bash
git add templates/ static/
git commit -m "Updated homepage design"
git push origin main
```

**5. You pull changes:**
```bash
git pull origin main
python manage.py runserver
# Test their changes
```

### Protect Python Code (Create Frontend-Only Branch)

**Better approach - Create separate branch:**

```bash
# Create frontend-only branch
git checkout -b frontend-only

# Remove Python files from this branch
git rm -r App/
git rm -r Jobstock/
git rm manage.py
git rm *.py
git commit -m "Frontend-only branch - no Python code"
git push origin frontend-only
```

**Frontend developer clones this branch:**
```bash
git clone -b frontend-only https://github.com/YOUR-USERNAME/jobstock-django-frontend.git
```

**Now they only see templates and static!**

---

## 🚀 SOLUTION 2: Cloud Django Hosting

### Deploy Django so Frontend Dev Can Access

#### Option A: PythonAnywhere (Easiest)

**1. Create account:**
- Go to https://www.pythonanywhere.com
- Sign up (Free tier available)

**2. Upload your code:**
```bash
# Use Git or upload files
# Follow PythonAnywhere Django tutorial
```

**3. Configure:**
- Set up web app
- Configure static files path
- Set ALLOWED_HOSTS

**4. Access:**
```
https://yourusername.pythonanywhere.com
```

**5. Frontend developer:**
- Gets the URL
- Edits files via PythonAnywhere's file editor
- Or uses Git to push changes

#### Option B: Heroku

**1. Install Heroku CLI:**
```bash
# Download from https://devcenter.heroku.com/articles/heroku-cli
```

**2. Create app:**
```bash
heroku login
heroku create jobstock-django-app
```

**3. Deploy:**
```bash
git push heroku main
```

**4. Frontend dev accesses:**
```
https://jobstock-django-app.herokuapp.com
```

#### Option C: Railway.app

**Easiest deployment:**
1. Go to https://railway.app
2. Click "New Project" → "Deploy from GitHub"
3. Select your repository
4. Auto-deploys on every push!

**Frontend dev:**
- Pushes to Git
- Railway auto-deploys
- See changes live instantly

---

## 💻 SOLUTION 3: VS Code Live Share

### Real-Time Collaboration

**1. Install VS Code Live Share:**
- Both install VS Code
- Install "Live Share" extension

**2. You start session:**
```
Ctrl+Shift+P → "Live Share: Start Collaboration Session"
```

**3. Share link with frontend dev:**
```
https://prod.liveshare.vssps.visualstudio.com/join?...
```

**4. They join and edit in real-time!**

**Features:**
- ✅ Real-time editing
- ✅ Shared terminal (optional)
- ✅ Voice/text chat
- ✅ See each other's cursors
- ✅ Restrict access to specific folders

**Restrict folder access:**
- Settings → Live Share
- Set "Share Path" to only `templates/` and `static/`

---

## 🌐 SOLUTION 4: ngrok Tunnel (Quick Demo)

### Temporarily expose your local server

**1. Download ngrok:**
```bash
# Go to https://ngrok.com
# Download and install
```

**2. Start Django:**
```bash
python manage.py runserver 0.0.0.0:8000
```

**3. Start ngrok:**
```bash
ngrok http 8000
```

**4. Share URL:**
```
Forwarding: https://abc123.ngrok.io -> localhost:8000
```

**5. Frontend dev accesses:**
```
https://abc123.ngrok.io
```

**⚠️ Limitations:**
- Free tier: URL changes each restart
- Session timeout after 2 hours
- Best for demos, not daily work

**For persistent URL (ngrok paid):**
```bash
ngrok http 8000 --subdomain=jobstock-dev
# URL: https://jobstock-dev.ngrok.io
```

---

## 🎯 RECOMMENDED WORKFLOW (Professional)

### Best Setup for Remote Team:

```
Day 1: Setup
├── You: Create Git repository
├── You: Push code to GitHub
├── You: Add frontend dev as collaborator
└── Frontend Dev: Clone repository

Daily Work:
├── Frontend Dev:
│   ├── Edit templates/static
│   ├── git commit -m "message"
│   ├── git push
│   └── Notify you
│
└── You:
    ├── git pull
    ├── Test changes locally
    ├── Deploy if good
    └── Provide feedback

Communication:
├── Slack/Discord for chat
├── GitHub Issues for bugs
├── GitHub Pull Requests for reviews
└── Screen share for complex issues
```

---

## 📋 Step-by-Step: Git Method (Detailed)

### Your Setup (Backend Developer):

**1. Install Git (if needed):**
```bash
# Download from https://git-scm.com
```

**2. Configure Git:**
```bash
git config --global user.name "Your Name"
git config --global user.email "your@email.com"
```

**3. Create .gitignore:**
```bash
@"
# Python
__pycache__/
*.pyc
venv*/
db.sqlite3

# Keep these
!templates/
!static/
"@ | Out-File -FilePath .gitignore -Encoding utf8
```

**4. Initialize and push:**
```bash
git init
git add .
git commit -m "Initial commit"

# Create repo on GitHub first, then:
git remote add origin https://github.com/YOUR-USERNAME/jobstock.git
git push -u origin main
```

**5. Invite collaborator:**
- GitHub.com → Your Repository
- Settings → Collaborators → Add people
- Enter frontend dev's GitHub username

### Frontend Developer Setup:

**1. Install Git:**
```bash
# Download from https://git-scm.com
```

**2. Accept invitation:**
- Check email from GitHub
- Click "Accept invitation"

**3. Clone repository:**
```bash
git clone https://github.com/YOUR-USERNAME/jobstock.git
cd jobstock
```

**4. Edit files:**
```
Use any editor:
- VS Code
- Sublime Text
- Notepad++
- WebStorm
```

**5. Save and push:**
```bash
# After editing templates/static files
git add templates/ static/
git commit -m "Updated homepage design"
git push origin main
```

**6. You pull and test:**
```bash
git pull origin main
python manage.py runserver
# Test at http://localhost:8000
```

---

## 🔐 Security for Remote Access

### Protect Sensitive Data:

**1. Environment variables:**
```python
# settings.py
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG', 'False') == 'True'
```

**2. Create .env file (don't commit):**
```
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
```

**3. Add to .gitignore:**
```
.env
*.env
db.sqlite3
user-password.txt
```

**4. Share secrets securely:**
- Use 1Password
- Or encrypted file
- Never in Git!

---

## 📱 Communication Tools

### Recommended for Remote Team:

**Chat:**
- Slack (free tier)
- Discord (free)
- Microsoft Teams

**Video:**
- Zoom
- Google Meet  
- Microsoft Teams

**Screen Share:**
- TeamViewer
- AnyDesk
- Chrome Remote Desktop

**Project Management:**
- GitHub Projects (built-in)
- Trello (free)
- Asana (free tier)

---

## 🛠️ Frontend Dev Tools (Remote)

### Recommended Setup:

**Code Editor:**
- VS Code (free, recommended)
- Sublime Text
- Atom

**Browser DevTools:**
- Chrome DevTools
- Firefox Developer Tools

**Version Control:**
- GitHub Desktop (GUI for Git)
- GitKraken (visual Git client)

**Design Tools:**
- Figma (free, browser-based)
- Adobe XD (free tier)

---

## 📊 Comparison Table

| Solution | Cost | Setup | Best For | Live Preview |
|----------|------|-------|----------|--------------|
| **Git + GitHub** | Free | 15 min | Professional | No (local test) |
| **PythonAnywhere** | Free tier | 30 min | Small projects | Yes |
| **Railway.app** | Free tier | 10 min | Auto-deploy | Yes |
| **VS Code Live Share** | Free | 5 min | Pair programming | Yes |
| **ngrok** | Free tier | 5 min | Quick demos | Yes |
| **Heroku** | Free tier ending | 20 min | Production-like | Yes |

**Recommendation:** Use **Git + GitHub** for daily work, plus **Railway.app** for live preview.

---

## ✅ Complete Setup Guide (Git Method)

### Phase 1: Initial Setup (You)

```powershell
# 1. Create GitHub account (if needed)
# Go to github.com

# 2. Create new repository
# Name: jobstock-frontend
# Private repository

# 3. In your project folder
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR-USERNAME/jobstock-frontend.git
git push -u origin main

# 4. Invite frontend developer
# GitHub → Settings → Collaborators → Add
```

### Phase 2: Frontend Developer Setup (Them)

```bash
# 1. Install Git
# Download from git-scm.com

# 2. Configure Git
git config --global user.name "Frontend Dev Name"
git config --global user.email "dev@email.com"

# 3. Clone repository
git clone https://github.com/YOUR-USERNAME/jobstock-frontend.git
cd jobstock-frontend

# 4. Install editor (VS Code recommended)
# Download from code.visualstudio.com
```

### Phase 3: Daily Workflow

**Frontend Developer:**
```bash
# Morning: Get latest
git pull origin main

# Work: Edit files
# Edit templates/ and static/ folders

# Evening: Push changes
git add templates/ static/
git commit -m "Updated contact page styling"
git push origin main
```

**You (Backend):**
```bash
# When notified of changes
git pull origin main

# Test locally
python manage.py runserver

# If good, deploy to production
```

---

## 🎓 Git Basics for Frontend Developer

### Essential Commands:

```bash
# Get latest code
git pull

# Check what changed
git status

# Add files to commit
git add templates/
git add static/

# Save changes locally
git commit -m "Description of changes"

# Send to GitHub
git push

# Undo local changes
git checkout -- filename.html

# See history
git log

# Create branch for experiments
git checkout -b new-feature

# Switch branches
git checkout main
```

### Git Workflow Diagram:

```
Edit Files → git add → git commit → git push → GitHub
                                               ↓
You ← git pull ← GitHub ← Review changes
```

---

## 📞 Support & Troubleshooting

### Common Issues:

**"Permission denied" on push:**
```bash
# Check collaborator access on GitHub
# Or use personal access token
```

**"Merge conflict":**
```bash
# Don't panic!
# Open conflicted file
# Keep the correct version
git add filename
git commit
```

**"Cannot find repository":**
```bash
# Check URL is correct
git remote -v

# Update if needed
git remote set-url origin https://github.com/USER/REPO.git
```

---

## 🎉 Quick Start Summary

### For Git Method (RECOMMENDED):

**You do:**
1. Create GitHub repository
2. Push code: `git push origin main`
3. Invite frontend dev (Settings → Collaborators)
4. Share repository URL

**Frontend dev does:**
1. Install Git
2. Clone: `git clone [URL]`
3. Edit files in `templates/` and `static/`
4. Push: `git add . && git commit -m "msg" && git push`

**You review:**
1. Pull: `git pull origin main`
2. Test: `python manage.py runserver`
3. Deploy if good!

**Done! Professional remote workflow! 🚀**

---

Need more help? Check these resources:
- Git Guide: https://guides.github.com
- GitHub Docs: https://docs.github.com
- VS Code: https://code.visualstudio.com/docs
- Django Deployment: https://docs.djangoproject.com/en/stable/howto/deployment/
