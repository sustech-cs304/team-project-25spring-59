# 多阶段构建

# 前端构建阶段
FROM node:18-alpine AS frontend-build

WORKDIR /app/frontend
COPY frontier-app/package*.json ./
RUN npm install
COPY frontier-app/ ./
RUN npm run build

# 后端构建阶段
FROM python:3.11-slim

WORKDIR /app

# 复制依赖文件并安装
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制后端文件
COPY backapp/ ./backapp/

# 复制前端构建结果到后端静态目录
COPY --from=frontend-build /app/frontend/dist ./backapp/static/

# 复制SQL文件
COPY test.sql ./

# 暴露端口
EXPOSE 8000

# 启动应用
CMD ["uvicorn", "backapp.main:app", "--host", "0.0.0.0", "--port", "8000"] 