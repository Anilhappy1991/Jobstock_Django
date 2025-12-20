@echo off
REM ======================================================
REM Full Development Environment - Restart Script
REM ======================================================

echo.
echo ========================================
echo  Restarting Jobstock Development Server
echo ========================================
echo.

docker-compose -f docker-compose.fulldev.yml restart

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Failed to restart application!
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo  Application Restarted Successfully!
echo ========================================
echo.
echo Application is now running at http://localhost:8000
echo.
timeout /t 2 /nobreak >nul
start http://localhost:8000
echo.
pause
