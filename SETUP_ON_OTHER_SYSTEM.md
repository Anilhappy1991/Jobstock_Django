# Setup on Other System - Quick Guide

## 📋 What You Need to Install

### Required Software:
1. **Docker Desktop** ⬅️ MUST HAVE!
   - Windows: https://www.docker.com/products/docker-desktop
   - Mac: https://www.docker.com/products/docker-desktop
   - Linux: https://docs.docker.com/engine/install/

2. **Git** (Optional - for team collaboration)
   - Windows: https://git-scm.com/download/win
   - Mac: Already installed or via Homebrew: `brew install git`
   - Linux: `sudo apt-get install git`

3. **Code Editor** (Optional but recommended)
   - VS Code: https://code.visualstudio.com/
   - Or any text editor you prefer

---

## 🚀 Transfer Project to New Computer

### Method 1: Using ZIP File (Easiest)
```
1. Locate ZIP file: Jobstock_FullDev_Package_20251220_103029.zip
2. Copy to USB drive or upload to cloud (Google Drive, OneDrive, Dropbox)
3. Download/copy to new computer
4. Extract to any location (e.g., D:\Projects\ or ~/Projects/)
```

### Method 2: Using Git (Best for Teams)
```bash
# On original computer (one time setup):
cd c:\RandR\Jobstock_Django_v1.0.0\Jobstock_Django
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/yourusername/jobstock.git
git push -u origin main

# On new computer:
git clone https://github.com/yourusername/jobstock.git
cd jobstock
```

### Method 3: Network Share
```
1. Share folder on network
2. Copy entire folder to new computer
3. Done!
```

---

## 🖥️ Setup Instructions by Operating System

### Windows 10/11

1. **Install Docker Desktop**
   - Download from https://www.docker.com/products/docker-desktop
   - Run installer
   - Restart computer if prompted
   - Start Docker Desktop (wait for green icon in system tray)

2. **Open Project Folder**
   ```
   Navigate to: D:\Projects\Jobstock_Django (or wherever you extracted)
   ```

3. **Start Server**
   ```batch
   Double-click: start_fulldev.bat
   ```

4. **Wait for Build** (first time: 2-3 minutes)

5. **Browser Opens Automatically** at http://localhost:8000

6. **Start Editing!**
   - Edit files in `templates/` and `static/`
   - Save → Refresh browser → See changes!

---

### macOS (Intel or Apple Silicon)

1. **Install Docker Desktop**
   ```
   Download from https://www.docker.com/products/docker-desktop
   Install and start Docker Desktop
   ```

2. **Open Terminal**
   ```bash
   # Navigate to project
   cd ~/Desktop/Jobstock_Django
   ```

3. **Make Scripts Executable (First Time Only)**
   ```bash
   chmod +x start_fulldev.sh stop_fulldev.sh restart_fulldev.sh logs_fulldev.sh rebuild_fulldev.sh
   ```

4. **Start Server**
   ```bash
   ./start_fulldev.sh
   ```

5. **Open Browser**
   ```
   Automatically opens at http://localhost:8000
   Or manually open: http://localhost:8000
   ```

**Alternative (Manual Docker Commands):**
```bash
docker-compose -f docker-compose.fulldev.yml up --build -d
open http://localhost:8000
```

---

### Linux (Ubuntu/Debian)

1. **Install Docker**
   ```bash
   # Update package list
   sudo apt-get update
   
   # Install Docker
   sudo apt-get install docker.io docker-compose
   
   # Add your user to docker group (avoid sudo)
   sudo usermod -aG docker $USER
   
   # Log out and log back in for group change to take effect
   ```

2. **Start Docker Service**
   ```bash
   sudo systemctl start docker
   sudo systemctl enable docker
   ```

3. **Navigate to Project**
   ```bash
   cd ~/Projects/Jobstock_Django
   ```

4. **Make Scripts Executable (First Time Only)**
   ```bash
   chmod +x *.sh
   ```

5. **Start Server**
   ```bash
   ./start_fulldev.sh
   ```

6. **Open Browser**
   ```bash
   # Automatically opens or manually:
   xdg-open http://localhost:8000
   ```

**Alternative (Manual Docker Commands):**
```bash
docker-compose -f docker-compose.fulldev.yml up --build -d
```

---

## 📁 Files Included (What to Transfer)

**Essential Files:**
```
Jobstock_Django/
├── start_fulldev.bat          # Windows start script
├── stop_fulldev.bat           # Windows stop script
├── restart_fulldev.bat        # Windows restart script
├── logs_fulldev.bat           # Windows logs script
├── rebuild_fulldev.bat        # Windows rebuild script
├── start_fulldev.sh           # Mac/Linux start script
├── stop_fulldev.sh            # Mac/Linux stop script
├── restart_fulldev.sh         # Mac/Linux restart script
├── logs_fulldev.sh            # Mac/Linux logs script
├── rebuild_fulldev.sh         # Mac/Linux rebuild script
├── Dockerfile.fulldev         # Docker configuration
├── docker-compose.fulldev.yml # Docker compose config
├── requirements.txt           # Python packages
├── README_FULLDEV.md          # Documentation
├── templates/                 # HTML templates (EDITABLE)
├── static/                    # CSS/JS/Images (EDITABLE)
├── db.sqlite3                 # Database (EDITABLE)
├── App/                       # Backend code
├── Jobstock/                  # Django config
└── manage.py                  # Django CLI
```

---

## 🎯 Quick Start Checklist

- [ ] Docker Desktop installed and running (green icon)
- [ ] Project folder copied/extracted to new computer
- [ ] Navigate to project folder
- [ ] Windows: Run `start_fulldev.bat`
- [ ] Mac/Linux: Run `./start_fulldev.sh` (after `chmod +x start_fulldev.sh`)
- [ ] Wait 2-3 minutes (first time only)
- [ ] Browser opens at http://localhost:8000
- [ ] Edit files in `templates/` or `static/`
- [ ] Save → Refresh browser (Ctrl+F5)
- [ ] See changes immediately!

---

## 🔧 Troubleshooting

### Docker not running?
```
Windows: Check system tray for Docker icon (should be green)
Mac: Check menu bar for Docker whale icon
Linux: sudo systemctl status docker
```

### Port 8000 already in use?
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Mac/Linux
lsof -ti:8000 | xargs kill -9
```

### Permission errors (Linux)?
```bash
# Add user to docker group
sudo usermod -aG docker $USER
# Log out and log back in
```

### Can't execute .sh files (Mac/Linux)?
```bash
chmod +x *.sh
```

### Docker build fails?
```
1. Check internet connection (needs to download images)
2. Check Docker has enough disk space (Settings → Resources)
3. Try: docker system prune -af
4. Run rebuild script again
```

---

## 📞 Support

### Common Questions:

**Q: Do I need Python installed?**
A: No! Everything runs inside Docker.

**Q: Which port does it use?**
A: Port 8000. Make sure it's not in use.

**Q: Can I change the port?**
A: Yes, edit `docker-compose.fulldev.yml`:
```yaml
ports:
  - "9000:8000"  # Change 9000 to your preferred port
```

**Q: How do I stop the server?**
```
Windows: stop_fulldev.bat
Mac/Linux: ./stop_fulldev.sh
```

**Q: How do I update Python packages?**
```
1. Edit requirements.txt
2. Windows: rebuild_fulldev.bat
3. Mac/Linux: ./rebuild_fulldev.sh
```

---

## ✅ Verification Steps

After setup, verify everything works:

1. **Check Docker is running:**
   ```bash
   docker ps
   # Should show jobstock_fulldev container
   ```

2. **Check web server:**
   ```bash
   # Open: http://localhost:8000
   # Should see website
   ```

3. **Test live editing:**
   ```
   1. Open: templates/pages/index.html
   2. Change some text
   3. Save (Ctrl+S)
   4. Refresh browser (Ctrl+F5)
   5. Should see changes!
   ```

---

## 🎓 Daily Workflow

**Morning:**
```
Windows: start_fulldev.bat
Mac/Linux: ./start_fulldev.sh
```

**Work:**
```
Edit files → Save → Refresh browser
```

**Evening:**
```
Windows: stop_fulldev.bat
Mac/Linux: ./stop_fulldev.sh
```

---

## 📧 Share With Team Members

**Email Template:**
```
Subject: Jobstock Development Environment Setup

Hi,

Here's how to set up the Jobstock development environment on your computer:

1. Install Docker Desktop: https://www.docker.com/products/docker-desktop
2. Extract the attached ZIP file
3. Windows: Double-click start_fulldev.bat
   Mac/Linux: Run ./start_fulldev.sh (after chmod +x start_fulldev.sh)
4. Wait 2-3 minutes (first time)
5. Browser opens at http://localhost:8000

Edit files in templates/ and static/ folders.
See changes instantly by refreshing browser!

Full guide: See README_FULLDEV.md in the folder

Questions? Let me know!
```

---

**Summary:**
1. ✅ Install Docker Desktop on new computer
2. ✅ Copy/transfer project folder
3. ✅ Run start script (Windows: .bat, Mac/Linux: .sh)
4. ✅ Edit files and see changes instantly!

No Python, no complex setup - just Docker and go! 🚀
