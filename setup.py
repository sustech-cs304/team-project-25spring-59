from setuptools import setup, find_packages
import os
from pathlib import Path

# 从 requirements.txt 文件中读取依赖项
with open('backapp/requirements.txt') as f:
    required = f.read().splitlines()

# 项目信息
setup(
    name="personal_health_assistant",
    version="0.1.0",
    description="个人健康助手后端服务",
    author="Team-25Spring-59",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'backapp': ['static/**/*'],
    },
    python_requires=">=3.8",
    install_requires=required,
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.11",
    ],
) 