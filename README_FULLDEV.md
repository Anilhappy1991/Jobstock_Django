# Jobstock Django - Full Development Environment

## 🚀 Quick Start for Frontend Developers

### First Time Setup:

1. **Make sure Docker Desktop is running**
   - Look for Docker icon in system tray
   - Should show "Docker Desktop is running"

2. **Double-click `start_fulldev.bat`**
   - First time will take 2-3 minutes to build
   - Wait for "Application Started Successfully!"
   - Browser will open automatically at http://localhost:8000

3. **Start working!**
   - Edit files in `templates/` or `static/` folders
   - Modify `db.sqlite3` database (using DB Browser or Django Admin)
   - Save and refresh browser to see changes

### Daily Usage:

| Action | Command |
|--------|---------|
| **Start Server** | Double-click `start_fulldev.bat` |
| **Stop Server** | Double-click `stop_fulldev.bat` |
| **Restart Server** | Double-click `restart_fulldev.bat` |
| **View Logs** | Double-click `logs_fulldev.bat` |
| **Rebuild Image** | Double-click `rebuild_fulldev.bat` |

---

## 📁 What You Can Edit

### ✅ Frontend Files (Changes Reflect Immediately):
```
templates/          - All HTML template files
  ├── Base/         - Base layouts, header, footer
  ├── Components/   - Reusable components
  └── pages/        - Individual page templates

static/             - All static assets
  ├── css/          - Stylesheets
  ├── js/           - JavaScript files
  ├── img/          - Images
  ├── vendor/       - Third-party libraries
  └── webfonts/     - Font files
```

### ✅ Database (Changes Reflect Immediately):
```
db.sqlite3         - SQLite database file
```

**How to Edit Database:**
1. Download [DB Browser for SQLite](https://sqlitebrowser.org/)
2. Open `db.sqlite3` file
3. Make changes (add/edit/delete data)
4. Save changes
5. Refresh your browser - changes appear immediately!

**Or use Django Admin:**
1. Go to http://localhost:8000/admin
2. Login with admin credentials
3. Edit data through web interface

### ✅ Python Dependencies (Changes Require Rebuild):
```
requirements.txt   - Python package dependencies
```

**How to Edit Dependencies:**
1. Open `requirements.txt` in any text editor
2. Add, remove, or update package versions
3. Save the file
4. Run `rebuild_fulldev.bat` to rebuild with new packages
5. Container will restart with updated dependencies

### ❌ Backend Files (Inside Docker - Cannot Edit):
```
App/                - Python application code
Jobstock/           - Django configuration
manage.py           - Django management script
```

---

## 🌐 Access the Application

After running `start_fulldev.bat`:
- **Main Application:** http://localhost:8000
- **Admin Panel:** http://localhost:8000/admin
- **Static Files:** http://localhost:8000/static/

---

## 🔧 How It Works

### Volume Mounting:
All editable files are **mounted** from your computer into Docker:

```
Your Computer                Docker Container
─────────────                ────────────────
templates/            ←→     /app/templates/
static/               ←→     /app/static/
db.sqlite3            ←→     /app/db.sqlite3
data/                 ←→     /app/data/
```

This means:
- ✅ Edit files on your computer using any editor
- ✅ Changes appear in Docker immediately
- ✅ No rebuild required for frontend changes
- ✅ Database changes sync both ways

### What's Inside Docker:
- Python 3.12
- Django framework
- All backend code (App/, Jobstock/)
- Python dependencies
- Web server

### What's Outside Docker:
- HTML templates
- CSS, JavaScript
- Images and static files
- SQLite database
- Uploaded files

---

## 💡 Workflow Examples

### Edit HTML Template:
1. Open `templates/pages/home.html` in VS Code
2. Make changes
3. Save file
4. Refresh browser (Ctrl+F5)
5. See changes immediately!

### Edit CSS:
1. Open `static/css/style.css`
2. Make changes
3. Save file
4. Hard refresh browser (Ctrl+Shift+R)
5. See changes immediately!

### Edit Database:
1. Open `db.sqlite3` in DB Browser
2. Go to "Browse Data" tab
3. Select a table (e.g., `App_job`)
4. Edit data
5. Click "Write Changes"
6. Refresh website - see changes!

### Add New Image:
1. Copy image to `static/img/`
2. Use in template: `<img src="{% static 'img/your-image.jpg' %}">`
3. Refresh browser - image appears!

---

## 🆘 Troubleshooting

### Changes Not Appearing?
1. **Hard refresh browser:** Ctrl+F5 (Windows) or Cmd+Shift+R (Mac)
2. **Clear browser cache**
3. **Check you saved the file**
4. **Restart server:** Run `restart_fulldev.bat`

### Port 8000 Already in Use?
1. Run `stop_fulldev.bat`
2. Run: `docker ps -a`
3. Run: `docker rm -f jobstock_fulldev`
4. Run `start_fulldev.bat` again

### Database Locked Error?
1. Close DB Browser for SQLite
2. Make sure no other programs are accessing `db.sqlite3`
3. Restart server with `restart_fulldev.bat`

### Container Won't Start?
1. Run `logs_fulldev.bat` to see errors
2. Check Docker Desktop is running
3. Try `rebuild_fulldev.bat` to rebuild from scratch

### Static Files Not Loading?
1. Run `rebuild_fulldev.bat`
2. This will run `collectstatic` command
3. Check `staticfiles/` folder is created

---

## 📊 File Structure

```
Jobstock_Django/
├── start_fulldev.bat          # ← Start server
├── stop_fulldev.bat           # ← Stop server
├── restart_fulldev.bat        # ← Restart server
├── logs_fulldev.bat           # ← View logs
├── rebuild_fulldev.bat        # ← Rebuild image
├── Dockerfile.fulldev         # Docker image definition
├── docker-compose.fulldev.yml # Docker configuration
├── db.sqlite3                 # ← Database (editable)
├── templates/                 # ← HTML files (editable)
├── static/                    # ← CSS/JS/Images (editable)
├── data/                      # ← Uploads (editable)
├── App/                       # Python code (in Docker)
├── Jobstock/                  # Django config (in Docker)
└── manage.py                  # Django CLI (in Docker)
```

---

## 🔐 Security Notes

### What You Should NOT Do:
- ❌ Don't commit `db.sqlite3` to Git (use .gitignore)
- ❌ Don't share database with sensitive data
- ❌ Don't modify files in `App/` or `Jobstock/` folders
- ❌ Don't change Docker configuration files

### What's Safe:
- ✅ Edit all files in `templates/` folder
- ✅ Edit all files in `static/` folder
- ✅ Edit `db.sqlite3` for testing
- ✅ Add new images, CSS, JavaScript files

---

## 🎯 Tips for Success

### Use Good Editor:
- **VS Code** (Recommended): Free, powerful, many extensions
- **Sublime Text**: Fast and lightweight
- **PyCharm**: Full-featured IDE

### Browser DevTools:
- Press F12 to open Developer Tools
- Debug CSS changes in real-time
- Test JavaScript in console
- Check network requests

### Database Management:
- **DB Browser for SQLite**: Visual database editor
- **Django Admin**: Web-based data management
- **SQLite CLI**: Command-line access

### Version Control:
- Use Git to track your changes
- Commit template and static file changes
- Create branches for new features
- Don't commit `db.sqlite3`

---

## 📝 Common Tasks

### Add New Page Template:
1. Create new HTML file in `templates/pages/`
2. Copy structure from existing template
3. Edit content
4. Add URL route (ask backend developer)
5. Refresh browser

### Modify Existing Page:
1. Find template in `templates/pages/`
2. Edit HTML
3. Save file
4. Hard refresh browser (Ctrl+F5)

### Change Styling:
1. Edit CSS in `static/css/`
2. Or add inline styles in template
3. Save changes
4. Hard refresh browser

### Add JavaScript Functionality:
1. Edit or create JS file in `static/js/`
2. Include in template: `<script src="{% static 'js/your-script.js' %}"></script>`
3. Save and refresh

### Update Database Content:
1. Open `db.sqlite3` in DB Browser
2. Navigate to table
3. Edit data
4. Write changes
5. Refresh website

---

## 🚀 Advanced Usage

### Access Django Shell:
```batch
docker exec -it jobstock_fulldev python manage.py shell
```

### Run Django Commands:
```batch
docker exec -it jobstock_fulldev python manage.py <command>
```

### Access Container Bash:
```batch
docker exec -it jobstock_fulldev bash
```

### View Container Status:
```batch
docker ps
```

### View All Logs:
```batch
docker-compose -f docker-compose.fulldev.yml logs
```

---

## 📞 Need Help?

### Check Logs:
Run `logs_fulldev.bat` to see detailed error messages

### Common Solutions:
1. Restart: `restart_fulldev.bat`
2. Rebuild: `rebuild_fulldev.bat`
3. Check Docker Desktop is running
4. Clear browser cache

### Still Stuck?
Contact your backend developer with:
- Description of the issue
- Error messages from logs
- What you were trying to do
- Screenshot if applicable

---

## ✨ Summary

**You have full access to:**
- ✅ All HTML templates
- ✅ All CSS, JavaScript, images
- ✅ SQLite database
- ✅ Uploaded files and media

**Changes reflect immediately:**
- No rebuild required
- Just save and refresh
- Fast development workflow

**Simple commands:**
- `start_fulldev.bat` - Start everything
- Edit files - Make changes
- Refresh browser - See results
- `stop_fulldev.bat` - Stop when done

**Happy Coding!** 🎨
