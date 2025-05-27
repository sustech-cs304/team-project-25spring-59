@echo off
echo Starting Personal Health Assistant project build...

REM Build frontend
echo ========== Building Frontend Application ==========
cd frontier-app
call npm install
call npm run build
cd ..
echo Frontend build completed!

REM Build backend
echo ========== Building Backend Application ==========
pip install -r requirements.txt
echo Backend dependencies installed!

REM Copy built frontend files to backend static directory
echo ========== Integrating Frontend and Backend ==========
if not exist backapp\static mkdir backapp\static
xcopy /E /Y frontier-app\dist\* backapp\static\
echo Frontend static files copied to backend static directory

echo Build completed!
pause