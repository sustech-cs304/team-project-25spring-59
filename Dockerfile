# 多阶段构建

# 前端构建阶段
FROM node:18-alpine AS frontend-build

WORKDIR /app/frontend
COPY frontier-app/package*.json ./
RUN npm install
COPY frontier-app/ ./
RUN npm run build

# 后端构建阶段 - 使用Python和Node.js构建wheel包
FROM python:3.11-slim AS backend-build

WORKDIR /app

# 安装wheel和setuptools
COPY requirements.txt .
RUN pip install wheel setuptools -r requirements.txt

# 复制项目文件
COPY setup.py MANIFEST.in ./
COPY backapp/ ./backapp/

# 复制前端构建结果到后端静态目录
COPY --from=frontend-build /app/frontend/dist ./backapp/static/

# 构建wheel包
RUN python setup.py bdist_wheel

# 最终运行阶段
FROM python:3.11-slim

WORKDIR /app

# 从构建阶段复制wheel包
COPY --from=backend-build /app/dist/*.whl /app/

# 安装wheel包（将会安装所有依赖）
RUN pip install --no-cache-dir /app/*.whl

# 复制完整的backapp目录（确保模块可以被正确导入）
COPY backapp/ /app/backapp/

# 复制SQL文件
COPY test.sql ./

# 暴露端口
EXPOSE 8000

# 启动应用
CMD ["uvicorn", "backapp.main:app", "--host", "0.0.0.0", "--port", "8000"] 