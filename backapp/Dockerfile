# 多阶段构建 - 构建wheel包
FROM python:3.11-slim AS build-stage

# 设置工作目录
WORKDIR /app

# 安装构建工具和依赖
COPY requirements.txt .
RUN pip install wheel setuptools -r requirements.txt

# 复制项目文件
COPY setup.py MANIFEST.in ./
COPY backapp/ ./backapp/

# 创建静态目录（用于存放前端构建结果）
RUN mkdir -p ./backapp/static

# 复制前端已构建的文件（这些文件应该由build.bat已经构建好）
COPY frontier-app/dist/ ./backapp/static/

# 构建wheel包
RUN python setup.py bdist_wheel

# 最终运行阶段
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 安装构建工具
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

# 创建包结构
RUN mkdir -p /app/backapp

# 复制wheel包
COPY --from=build-stage /app/dist/*.whl /app/

# 安装wheel包（将会安装所有依赖）
RUN pip install --no-cache-dir /app/*.whl

# 复制源码（确保模块可以被正确导入）
COPY backapp/ /app/backapp/

# 复制数据库文件
COPY test.sql /app/

# 暴露端口
EXPOSE 8000

# 启动应用
CMD ["uvicorn", "backapp.main:app", "--host", "0.0.0.0", "--port", "8000"] 