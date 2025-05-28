@echo off
echo ===============================================
echo   Personal Health Assistant - Production Build and Deploy
echo ===============================================

REM Enable error display
echo on

echo ========== Phase 1: Building Application ==========
REM Build frontend (production mode)
echo ========== Building Frontend (Production Mode) ==========
cd frontier-app 
call npm ci 
call npm run build
cd ..
echo Frontend build completed!

REM Build backend
echo ========== Building Backend ==========
pip install -r requirements.txt --no-cache-dir 
echo Backend dependencies installation completed!

REM Copy frontend build to backend static directory
echo ========== Integrating Frontend and Backend ==========
if not exist backapp\static mkdir backapp\static
xcopy /E /Y frontier-app\dist\* backapp\static\ 
echo Frontend static files copied to backend static directory

echo ========== Phase 2: Deploying Application ==========

REM Terminate potentially running processes
echo Terminating potentially running services...
taskkill /F /IM node.exe /T >nul 2>&1
taskkill /F /FI "WINDOWTITLE eq frontend*" >nul 2>&1
taskkill /F /FI "WINDOWTITLE eq backend*" >nul 2>&1

REM Start backend production server only - it will serve the frontend files
echo Starting production server...
start "server" cmd /c "uvicorn backapp.main:app --host 0.0.0.0 --port 8000"

echo ========== Deployment Complete! ==========
echo.
echo Service is running in the background. Check the console window named "server" for logs.
echo Frontend is accessible at: http://localhost:8000
echo API endpoints are available at: http://localhost:8000/docs
echo.
echo To stop the service, close the console window or terminate the process using Task Manager.
echo.
pause