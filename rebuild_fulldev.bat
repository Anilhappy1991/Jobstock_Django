@echo off
REM ======================================================
REM Full Development Environment - Rebuild Image
REM ======================================================

echo.
echo ========================================
echo  Rebuilding Jobstock Docker Image
echo ========================================
echo.
echo This will rebuild the Docker image with latest code.
echo Frontend files (templates, static, database) are not affected.
echo.
echo This may take 2-3 minutes...
echo.

docker-compose -f docker-compose.fulldev.yml down
docker-compose -f docker-compose.fulldev.yml build --no-cache
docker-compose -f docker-compose.fulldev.yml up -d

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Rebuild failed!
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo  Rebuild Complete!
echo ========================================
echo.
echo Application is now running at http://localhost:8000
echo.
timeout /t 2 /nobreak >nul
start http://localhost:8000
echo.
pause
