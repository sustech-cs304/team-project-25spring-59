from setuptools import setup, find_packages
import os

# 读取requirements.txt中的依赖
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="personal-health-assistant",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
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
            "health-assistant=backapp.main:start",
        ],
    },
) 