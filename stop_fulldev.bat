@echo off
REM ======================================================
REM Full Development Environment - Stop Script
REM ======================================================

echo.
echo ========================================
echo  Stopping Jobstock Development Server
echo ========================================
echo.

docker-compose -f docker-compose.fulldev.yml down

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Failed to stop application!
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo  Application Stopped Successfully!
echo ========================================
echo.
echo All containers have been stopped and removed.
echo Your data (templates, static, database) is preserved.
echo.
pause
