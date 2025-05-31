@echo off
echo ===============================================
echo   Personal Health Assistant - Production Build and Deploy
echo ===============================================

REM Enable error display
echo on

echo ========== Phase 1: Building Application ==========
echo ========== Building Frontend (Production Mode) ==========
cd frontier-app 
call npm ci 
call npm run build
cd ..
echo Frontend build completed!

echo ========== Building Backend ==========
pip install -r requirements.txt --no-cache-dir 
echo Backend dependencies installation completed!


echo ========== Integrating Frontend and Backend ==========
if not exist backapp\static mkdir backapp\static
xcopy /E /Y frontier-app\dist\* backapp\static\ 
echo Frontend static files copied to backend static directory

echo ========== Building Python Wheel Package ==========
pip install wheel
cd backapp

REM 确保包含了必要的__init__.py文件
if not exist databases\__init__.py echo # databases package initialization > databases\__init__.py
if not exist __init__.py echo # backapp package initialization > __init__.py
if not exist static\__init__.py echo # static package initialization > static\__init__.py

REM 清理之前的build产物
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist personal_health_assistant.egg-info rmdir /s /q personal_health_assistant.egg-info

REM 使用sdist确保包含所有文件，然后构建wheel
python setup.py sdist bdist_wheel
cd ..

echo ========== Phase 2: Deploying Application ==========

REM Terminate potentially running processes
echo Terminating potentially running services...
taskkill /F /IM node.exe /T >nul 2>&1
taskkill /F /FI "WINDOWTITLE eq FRONTEND-PREVIEW*" >nul 2>&1
taskkill /F /FI "WINDOWTITLE eq BACKEND-PREVIEW*" >nul 2>&1
timeout /t 1 >nul

echo ========== Starting Backend in Preview Mode ==========
start "BACKEND-PREVIEW" cmd /k "uvicorn backapp.main:app --host 0.0.0.0 --port 8000 --reload"
echo ========== Starting Frontend in Preview Mode ==========
echo Vue application in preview mode
cd frontier-app
start "FRONTEND-PREVIEW" cmd /k "npm run preview"
cd ..

pause