@echo off
REM ======================================================
REM Full Development Environment - View Logs
REM ======================================================

echo.
echo ========================================
echo  Jobstock Development Server Logs
echo ========================================
echo.
echo Press Ctrl+C to exit logs view
echo.

docker-compose -f docker-compose.fulldev.yml logs -f
