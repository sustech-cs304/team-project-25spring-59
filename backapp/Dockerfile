# 使用Python官方镜像作为基础镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 不再需要MySQL客户端库
# 只安装基本的构建工具
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

# 创建包结构
RUN mkdir -p /app/backapp

# 首先只复制依赖文件，提高缓存利用率
COPY requirements.txt .

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 仅复制必要的代码文件，排除测试和缓存
COPY backapp/*.py /app/backapp/
COPY backapp/databases /app/backapp/databases/
COPY backapp/static /app/backapp/static/

# 暴露端口
EXPOSE 8000

# 启动应用 - 使用正确的模块路径
CMD ["uvicorn", "backapp.main:app", "--host", "0.0.0.0", "--port", "8000"] 