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

REM wheel
echo ========== Building Python Wheel Package ==========
pip install wheel
cd backapp

REM 确保包含了必要的__init__.py文件
if not exist auth\__init__.py echo # auth package initialization > auth\__init__.py
if not exist databases\__init__.py echo # databases package initialization > databases\__init__.py
if not exist __init__.py echo # backapp package initialization > __init__.py

REM 确保static目录被包含并有__init__.py文件
if not exist static mkdir static
if not exist static\__init__.py echo # static package initialization > static\__init__.py

REM 确保frontend静态文件已复制到static目录
if exist "..\frontier-app\dist" (
    echo 复制前端构建文件到static目录...
    xcopy /E /Y "..\frontier-app\dist\*" "static\"
)

REM 确保uploads目录存在于static中
if not exist static\uploads mkdir static\uploads

REM 确保main.py中有start函数
echo def start():>tmpstart.py
echo     """Entry point for the package when installed via pip.""">>tmpstart.py
echo     import uvicorn>>tmpstart.py
echo     uvicorn.run("main:app", host="0.0.0.0", port=8000)>>tmpstart.py

REM 检查main.py是否已包含start函数
findstr /C:"def start():" main.py >nul
if errorlevel 1 (
    echo Adding start function to main.py
    type tmpstart.py >> main.py
)
del tmpstart.py

REM 清理之前的build产物
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist personal_health_assistant.egg-info rmdir /s /q personal_health_assistant.egg-info

REM 使用sdist确保包含所有文件，然后构建wheel
python setup.py sdist bdist_wheel

REM 检查wheel包中是否包含静态文件
echo ========== 检查wheel包内容 ==========
pip install wheel
python -m wheel unpack dist/*.whl -d tmp_wheel_check
if exist tmp_wheel_check (
    dir tmp_wheel_check\personal_health_assistant-0.1.0\static /s
    echo 如果上面列出了static目录下的文件，则wheel包包含了静态文件
    rmdir /s /q tmp_wheel_check
)

cd ..
echo Wheel package created in backapp/dist directory

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