@echo off
echo Starting Personal Health Assistant project build...

REM Build frontend
echo ========== Building Frontend Application ==========
cd frontier-app
call npm install
call npm run build
cd ..
echo Frontend build completed!

REM 确保目标目录存在
if not exist backapp\static mkdir backapp\static

REM 复制前端构建结果到后端静态目录
echo ========== Integrating Frontend and Backend ==========
xcopy /E /Y frontier-app\dist\* backapp\static\
echo Frontend static files copied to backend static directory

REM Build backend
echo ========== Building Backend Application ==========
pip install -r requirements.txt wheel setuptools
echo Backend dependencies installed!

REM Build wheel package
echo ========== Building Backend Wheel Package ==========
python setup.py bdist_wheel
echo Backend wheel package built successfully! Available in dist/ directory

echo ========== Build completed! ==========
echo.
echo To run the application locally:
echo   1. pip install .\dist\*.whl
echo   2. uvicorn backapp.main:app --reload
echo.
echo To build Docker images:
echo   docker compose build
echo.
echo To run Docker containers:
echo   docker compose up
echo.

pause