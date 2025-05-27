@echo off
echo ========== 个人健康助手项目部署脚本（SQLite版）==========
echo 此脚本将帮助您部署完整的应用程序，包括前端和后端（使用SQLite数据库）

REM 检查Docker是否已安装
where docker >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo 错误: 未安装Docker
    echo 请先安装Docker和Docker Compose，然后再运行此脚本
    exit /b 1
)

echo ========== 开始构建和启动容器 ==========
REM 停止并删除现有容器
docker-compose down

REM 构建并启动新容器
docker-compose up -d

REM 等待容器启动
echo 正在等待服务启动...
timeout /t 10 /nobreak >nul

echo ========== 部署完成 ==========
echo 前端: http://localhost:80
echo 后端API: http://localhost:8000
echo 后端API文档: http://localhost:8000/docs
echo SQLite数据库文件位置: /app/backapp/sqlite_health_assistant.db (容器内路径)

echo.
echo 要查看应用日志，请运行: docker-compose logs
echo 要停止应用，请运行: docker-compose down

pause 