from setuptools import setup, find_packages
import os
import glob

# 读取requirements.txt中的依赖
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

# 创建static包的__init__.py文件（如果不存在）
if not os.path.exists('static/__init__.py'):
    os.makedirs('static', exist_ok=True)
    with open('static/__init__.py', 'w') as f:
        f.write('# static package initialization')

# 递归获取static目录下的所有文件
static_files = []
for root, dirs, files in os.walk('static'):
    for file in files:
        if file != '__init__.py':  # 排除__init__.py文件
            path = os.path.join(root, file)
            # 将路径转换为相对于static的路径
            relative_path = os.path.relpath(path, 'static')
            static_files.append(relative_path)

setup(
    name="personal-health-assistant",
    version="0.1.0",
    packages=[ 'databases', 'static'],  # 添加static作为包目录
    py_modules=["main"],  # 包含主模块文件
    include_package_data=True,
    package_data={
        '': ['*.txt', '*.md', '*.jpg', '*.png', '*.svg', '*.ico', '*.webm', '*.jpeg'],
        'static': static_files,  # 使用动态生成的文件列表
        'databases': ['migrations/*', 'schemas/*'],
        'tests': ['*'],
    },
    # 使用zip_safe=False确保包不会被压缩，这样静态文件可以被正确访问
    zip_safe=False,
    install_requires=requirements,
    python_requires=">=3.7",
    description="个人健康助手应用",
    author="Team Project",
    author_email="team@example.com",
    url="https://github.com/yourusername/personal-health-assistant",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "health-assistant=main:start",
        ],
    },
) 