#!/bin/bash

echo "========== 个人健康助手项目部署脚本 =========="
echo "此脚本将帮助您部署完整的应用程序，包括前端、后端和MySQL数据库"

# 检查Docker是否已安装
if ! command -v docker &> /dev/null || ! command -v docker-compose &> /dev/null; then
    echo "错误: 未安装Docker或Docker Compose"
    echo "请先安装Docker和Docker Compose，然后再运行此脚本"
    exit 1
fi

# 确保数据库初始化脚本存在
if [ ! -f "test.sql" ]; then
    echo "警告: 未找到test.sql数据库初始化文件"
    echo "数据库将创建但可能没有初始数据"
fi

echo "========== 开始构建和启动容器 =========="
# 停止并删除现有容器
docker-compose down

# 构建并启动新容器
docker-compose up -d

# 等待容器启动
echo "正在等待服务启动..."
sleep 10

# 验证服务是否正常运行
backend_status=$(docker-compose ps | grep backend | grep -i "up" | wc -l)
frontend_status=$(docker-compose ps | grep frontend | grep -i "up" | wc -l)
mysql_status=$(docker-compose ps | grep mysql | grep -i "up" | wc -l)

if [ $backend_status -eq 1 ] && [ $frontend_status -eq 1 ] && [ $mysql_status -eq 1 ]; then
    echo "========== 部署成功 =========="
    echo "前端: http://localhost:80"
    echo "后端API: http://localhost:8000"
    echo "后端API文档: http://localhost:8000/docs"
    echo "MySQL数据库: localhost:3306"
    echo "   - 用户名: root"
    echo "   - 密码: 123456"
    echo "   - 数据库名: health_assistant"
else
    echo "========== 部署警告 =========="
    echo "一些服务可能未成功启动，请检查日志:"
    echo "docker-compose logs"
fi

echo ""
echo "要查看应用日志，请运行: docker-compose logs -f"
echo "要停止应用，请运行: docker-compose down" 