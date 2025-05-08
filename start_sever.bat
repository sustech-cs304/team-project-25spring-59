@echo off
REM 激活 Conda 虚拟环境
call conda activate fastapi-env

REM 切换到项目目录
cd /d D:\py_code\SE_pro\SE_pro

REM 启动 FastAPI 项目
python -m uvicorn backapp.main:app --reload

pause
