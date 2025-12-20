@echo off
REM ======================================================
REM Full Development Environment - Start Script
REM For Frontend Developers with Database Access
REM ======================================================

echo.
echo ========================================
echo  Jobstock Full Development Environment
echo ========================================
echo.

REM Check if Docker is running


docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Docker is not running!
    echo.
    echo Please start Docker Desktop and try again.
    echo.
    pause
    exit /b 1
)

echo [INFO] Docker is running...
echo.

REM Check if this is first run (no image exists)
docker images | findstr "jobstock_fulldev" >nul 2>&1
if %errorlevel% neq 0 (
    echo [INFO] First time setup - Building Docker image...
    echo [INFO] This will take 2-3 minutes. Please wait...
    echo.
    docker-compose -f docker-compose.fulldev.yml build
    if %errorlevel% neq 0 (
        echo.
        echo [ERROR] Docker build failed!
        echo Please check the error messages above.
        echo.
        pause
        exit /b 1
    )
) else (
    echo [INFO] Using existing Docker image...
    echo.
)

REM Start the application
echo [INFO] Starting application...
docker-compose -f docker-compose.fulldev.yml up -d

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Failed to start application!
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo  Application Started Successfully!
echo ========================================
echo.
echo Application URL: http://localhost:8000
echo Admin Panel:     http://localhost:8000/admin
echo.
echo ========================================
echo  What You Can Edit:
echo ========================================
echo.
echo  [32m✓[0m templates/       - All HTML files
echo  [32m✓[0m static/css/      - All CSS files
echo  [32m✓[0m static/js/       - All JavaScript files
echo  [32m✓[0m static/img/      - All images
echo  [32m✓[0m db.sqlite3       - Database file
echo.
echo ========================================
echo  How to Work:
echo ========================================
echo.
echo  1. Edit files in templates/ or static/
echo  2. Save your changes
echo  3. Refresh browser (Ctrl+F5) to see changes
echo  4. Database changes reflect immediately
echo.
echo ========================================
echo  Useful Commands:
echo ========================================
echo.
echo  - View logs:     docker-compose -f docker-compose.fulldev.yml logs -f
echo  - Stop server:   docker-compose -f docker-compose.fulldev.yml down
echo  - Restart:       docker-compose -f docker-compose.fulldev.yml restart
echo  - Rebuild:       docker-compose -f docker-compose.fulldev.yml up -d --build
echo.
echo Opening browser in 3 seconds...
timeout /t 3 /nobreak >nul
start http://localhost:8000

echo.
echo Press any key to exit...
pause >nul
