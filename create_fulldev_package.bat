@echo off
REM ======================================================
REM Create Package for Frontend Developer
REM Full Development Environment with Database Access
REM ======================================================

echo.
echo ========================================
echo  Creating Frontend Developer Package
echo  (Full Development Environment)
echo ========================================
echo.

set PACKAGE_NAME=Jobstock_FullDev_Package
set TIMESTAMP=%date:~-4%%date:~3,2%%date:~0,2%_%time:~0,2%%time:~3,2%%time:~6,2%
set TIMESTAMP=%TIMESTAMP: =0%
set PACKAGE_DIR=%PACKAGE_NAME%_%TIMESTAMP%

REM Create package directory
echo [1/10] Creating package directory...
if exist %PACKAGE_DIR% (
    echo Removing old package...
    rmdir /s /q %PACKAGE_DIR%
)
mkdir %PACKAGE_DIR%

REM Copy Docker files
echo [2/10] Copying Docker configuration...
copy Dockerfile.fulldev %PACKAGE_DIR%\Dockerfile.fulldev >nul
copy docker-compose.fulldev.yml %PACKAGE_DIR%\docker-compose.fulldev.yml >nul
copy requirements.txt %PACKAGE_DIR%\requirements.txt >nul
if exist .dockerignore copy .dockerignore %PACKAGE_DIR%\ >nul

REM Copy batch files
echo [3/10] Copying batch scripts...
copy start_fulldev.bat %PACKAGE_DIR%\ >nul
copy stop_fulldev.bat %PACKAGE_DIR%\ >nul
copy restart_fulldev.bat %PACKAGE_DIR%\ >nul
copy logs_fulldev.bat %PACKAGE_DIR%\ >nul
copy rebuild_fulldev.bat %PACKAGE_DIR%\ >nul

REM Copy documentation
echo [4/10] Copying documentation...
copy README_FULLDEV.md %PACKAGE_DIR%\README.md >nul
copy QUICK_START_FULLDEV.txt %PACKAGE_DIR%\ >nul
copy FULLDEV_SETUP_COMPLETE.md %PACKAGE_DIR%\ >nul

REM Copy frontend files (editable)
echo [5/10] Copying templates...
xcopy templates %PACKAGE_DIR%\templates\ /E /I /Q >nul

echo [6/10] Copying static files...
xcopy static %PACKAGE_DIR%\static\ /E /I /Q >nul

REM Copy backend files (required but not editable)
echo [7/10] Copying backend code...
xcopy App %PACKAGE_DIR%\App\ /E /I /Q >nul
xcopy Jobstock %PACKAGE_DIR%\Jobstock\ /E /I /Q >nul
xcopy core %PACKAGE_DIR%\core\ /E /I /Q >nul
if exist scripts xcopy scripts %PACKAGE_DIR%\scripts\ /E /I /Q >nul
copy manage.py %PACKAGE_DIR%\ >nul

REM Copy database
echo [8/10] Copying database...
if exist db.sqlite3 (
    copy db.sqlite3 %PACKAGE_DIR%\ >nul
    echo Database copied successfully
) else (
    echo Database not found, skipping...
)

REM Copy data directories
echo [9/10] Copying data directories...
if exist data xcopy data %PACKAGE_DIR%\data\ /E /I /Q >nul
mkdir %PACKAGE_DIR%\staticfiles >nul 2>&1
mkdir %PACKAGE_DIR%\temp_processing >nul 2>&1

REM Create instructions file
echo [10/10] Creating setup instructions...
echo. > %PACKAGE_DIR%\START_HERE.txt
echo ====================================================================== >> %PACKAGE_DIR%\START_HERE.txt
echo   JOBSTOCK DJANGO - FULL DEVELOPMENT ENVIRONMENT >> %PACKAGE_DIR%\START_HERE.txt
echo   Quick Start for Frontend Developers >> %PACKAGE_DIR%\START_HERE.txt
echo ====================================================================== >> %PACKAGE_DIR%\START_HERE.txt
echo. >> %PACKAGE_DIR%\START_HERE.txt
echo STEP 1: Install Docker Desktop >> %PACKAGE_DIR%\START_HERE.txt
echo    Download from: https://www.docker.com/products/docker-desktop >> %PACKAGE_DIR%\START_HERE.txt
echo. >> %PACKAGE_DIR%\START_HERE.txt
echo STEP 2: Make sure Docker Desktop is running >> %PACKAGE_DIR%\START_HERE.txt
echo    Look for Docker icon in system tray >> %PACKAGE_DIR%\START_HERE.txt
echo. >> %PACKAGE_DIR%\START_HERE.txt
echo STEP 3: Double-click: start_fulldev.bat >> %PACKAGE_DIR%\START_HERE.txt
echo    - First time takes 2-3 minutes >> %PACKAGE_DIR%\START_HERE.txt
echo    - Browser opens automatically >> %PACKAGE_DIR%\START_HERE.txt
echo. >> %PACKAGE_DIR%\START_HERE.txt
echo STEP 4: Start editing! >> %PACKAGE_DIR%\START_HERE.txt
echo    - Edit files in templates/ or static/ folders >> %PACKAGE_DIR%\START_HERE.txt
echo    - Save and refresh browser (Ctrl+F5) >> %PACKAGE_DIR%\START_HERE.txt
echo    - Changes appear immediately! >> %PACKAGE_DIR%\START_HERE.txt
echo. >> %PACKAGE_DIR%\START_HERE.txt
echo ====================================================================== >> %PACKAGE_DIR%\START_HERE.txt
echo   YOU CAN EDIT: >> %PACKAGE_DIR%\START_HERE.txt
echo ====================================================================== >> %PACKAGE_DIR%\START_HERE.txt
echo    ✓ templates/     - All HTML files >> %PACKAGE_DIR%\START_HERE.txt
echo    ✓ static/css/    - All CSS files >> %PACKAGE_DIR%\START_HERE.txt
echo    ✓ static/js/     - All JavaScript files >> %PACKAGE_DIR%\START_HERE.txt
echo    ✓ static/img/    - All images >> %PACKAGE_DIR%\START_HERE.txt
echo    ✓ db.sqlite3     - Database file >> %PACKAGE_DIR%\START_HERE.txt
echo. >> %PACKAGE_DIR%\START_HERE.txt
echo ====================================================================== >> %PACKAGE_DIR%\START_HERE.txt
echo   DAILY WORKFLOW: >> %PACKAGE_DIR%\START_HERE.txt
echo ====================================================================== >> %PACKAGE_DIR%\START_HERE.txt
echo    Morning:  start_fulldev.bat >> %PACKAGE_DIR%\START_HERE.txt
echo    Work:     Edit files - Save - Refresh browser >> %PACKAGE_DIR%\START_HERE.txt
echo    Evening:  stop_fulldev.bat >> %PACKAGE_DIR%\START_HERE.txt
echo. >> %PACKAGE_DIR%\START_HERE.txt
echo ====================================================================== >> %PACKAGE_DIR%\START_HERE.txt
echo   For complete documentation, see: README.md >> %PACKAGE_DIR%\START_HERE.txt
echo ====================================================================== >> %PACKAGE_DIR%\START_HERE.txt

REM Create .gitignore
echo. > %PACKAGE_DIR%\.gitignore
echo # Database >> %PACKAGE_DIR%\.gitignore
echo db.sqlite3 >> %PACKAGE_DIR%\.gitignore
echo. >> %PACKAGE_DIR%\.gitignore
echo # Static files >> %PACKAGE_DIR%\.gitignore
echo staticfiles/ >> %PACKAGE_DIR%\.gitignore
echo. >> %PACKAGE_DIR%\.gitignore
echo # Data and uploads >> %PACKAGE_DIR%\.gitignore
echo data/ >> %PACKAGE_DIR%\.gitignore
echo temp_processing/ >> %PACKAGE_DIR%\.gitignore
echo. >> %PACKAGE_DIR%\.gitignore
echo # Python cache >> %PACKAGE_DIR%\.gitignore
echo __pycache__/ >> %PACKAGE_DIR%\.gitignore
echo *.pyc >> %PACKAGE_DIR%\.gitignore
echo. >> %PACKAGE_DIR%\.gitignore
echo # Logs >> %PACKAGE_DIR%\.gitignore
echo *.log >> %PACKAGE_DIR%\.gitignore

REM Create ZIP archive
echo.
echo Creating ZIP archive...
powershell -command "Compress-Archive -Path '%PACKAGE_DIR%\*' -DestinationPath '%PACKAGE_DIR%.zip' -Force"

echo.
echo ========================================
echo  Package Created Successfully!
echo ========================================
echo.
echo Package folder: %CD%\%PACKAGE_DIR%
echo ZIP file:       %PACKAGE_DIR%.zip
echo.
echo ========================================
echo  Package Contents:
echo ========================================
echo.
echo  ✓ Batch files (start, stop, restart, logs, rebuild)
echo  ✓ Docker configuration (Dockerfile, docker-compose.yml)
echo  ✓ Documentation (README.md, guides)
echo  ✓ Frontend files (templates, static)
echo  ✓ Backend code (App, Jobstock, core)
echo  ✓ Database (db.sqlite3)
echo  ✓ Data directories
echo.
echo ========================================
echo  How Frontend Developer Uses It:
echo ========================================
echo.
echo  1. Extract ZIP file
echo  2. Make sure Docker Desktop is running
echo  3. Double-click: start_fulldev.bat
echo  4. Wait for browser to open
echo  5. Start editing templates/ and static/
echo  6. Refresh browser to see changes
echo.
echo ========================================
echo  Share This File:
echo ========================================
echo.
echo  Send: %PACKAGE_DIR%.zip
echo.
echo  Via: Email, Google Drive, Dropbox, WeTransfer, etc.
echo.
echo ========================================
pause
