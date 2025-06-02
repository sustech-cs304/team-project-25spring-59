# 使用 Sphinx 整合 Vue + FastAPI 项目文档教程

Sphinx 是一个强大的文档生成工具，特别适合整合多技术栈项目的文档。下面是如何使用 Sphinx 整合 Vue.js 前端和 FastAPI 后端文档的完整指南。

## 1. 安装 Sphinx

首先确保你已安装 Python，然后安装 Sphinx：

```bash
pip install sphinx sphinx-autobuild sphinx-rtd-theme
```

## 2. 初始化 Sphinx 项目

在项目根目录下创建文档目录并初始化：

```bash
mkdir docs
cd docs
sphinx-quickstart
```

回答初始化问题（大部分可默认）：
- 分离源文件和构建目录：y
- 项目名称：输入你的项目名
- 作者：你的名字/团队
- 版本：0.1.0
- 语言：en 或 zh_CN

## 3. 配置 Sphinx

编辑 `docs/source/conf.py`：

```python
# 添加扩展
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'sphinx.ext.autosummary',
    'sphinx_rtd_theme',
]

# 使用 readthedocs 主题
html_theme = 'sphinx_rtd_theme'

# 添加 Markdown 支持
extensions.append('myst_parser')

# 添加 Vue 和 FastAPI 文档路径
import os
import sys
sys.path.insert(0, os.path.abspath('../../backend'))  # 指向 FastAPI 代码目录
```

安装 Markdown 支持：
```bash
pip install myst-parser
```

## 4. 组织文档结构

编辑 `docs/source/index.rst`：

```rst
.. My Project documentation master file

Welcome to My Project's Documentation!
======================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:
   
   frontend/index
   backend/index
```

创建前端和后端子目录：
```bash
mkdir -p docs/source/frontend docs/source/backend
```

## 5. 集成前端文档

### 5.1 生成 Vue 组件文档

使用 Vue Styleguidist 生成文档：
```bash
npm run docs:build  # 假设已在 package.json 配置
```

### 5.2 将前端文档链接到 Sphinx

创建 `docs/source/frontend/index.rst`：

```rst
Frontend Documentation
======================

.. raw:: html
   :file: ../../../frontend-dist/index.html  # 指向 Vue 生成的文档
```

或使用 iframe 嵌入：

```rst
Frontend Documentation
======================

.. raw:: html

   <iframe src="../_static/frontend/index.html" width="100%" height="800px" style="border:none;"></iframe>
```

确保构建时复制前端文档：
```python
# 在 conf.py 中添加
html_static_path = ['_static']
```

## 6. 集成后端文档

### 6.1 生成 FastAPI OpenAPI 文档

创建 `docs/source/backend/index.rst`：

```rst
Backend API Documentation
=========================

.. openapi:: ../../backend/openapi.json
   :format: redoc
```

安装必要的扩展：
```bash
pip install sphinxcontrib-openapi
```

在 `conf.py` 中添加扩展：
```python
extensions.append('sphinxcontrib.openapi')
```

### 6.2 自动生成 Python 模块文档

创建 `docs/source/backend/modules.rst`：

```rst
Python Modules
==============

.. automodule:: main
   :members:
   :undoc-members:
   :show-inheritance:
```

## 7. 构建文档

### 本地构建和预览

```bash
cd docs
make html
sphinx-autobuild source build/html
```

访问 `http://localhost:8000` 查看文档

### 生产构建

```bash
cd docs
make html
```

生成的文档在 `docs/build/html` 目录

## 8. 高级配置

### 自定义主题

编辑 `conf.py`：

```python
html_theme_options = {
    'navigation_depth': 4,
    'collapse_navigation': False,
    'sticky_navigation': True,
    'includehidden': True,
    'titles_only': False
}
```

### 多语言支持

安装翻译工具：
```bash
pip install sphinx-intl
```

配置 `conf.py`：
```python
locale_dirs = ['locale/']
gettext_compact = False
```

生成翻译模板：
```bash
sphinx-build -b gettext source locale
sphinx-intl update -p locale -l zh_CN
```

## 9. CI/CD 集成 (GitHub Actions 示例)

创建 `.github/workflows/docs.yml`：

```yaml
name: Build and Deploy Documentation

on:
  push:
    branches: [ main ]

jobs:
  build-docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.8'
          
      - name: Install dependencies
        run: |
          pip install -r docs/requirements.txt
          npm install
          
      - name: Build frontend docs
        run: npm run docs:build
        
      - name: Build Sphinx docs
        run: |
          cd docs
          make html
          
      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./docs/build/html
```

## 10. 目录结构示例

最终项目结构应类似：

```
my-project/
├── backend/            # FastAPI 代码
├── frontend/           # Vue.js 代码
├── docs/               # Sphinx 文档
│   ├── source/
│   │   ├── frontend/   # 前端文档
│   │   ├── backend/    # 后端文档
│   │   ├── conf.py
│   │   └── index.rst
│   └── build/
├── .github/workflows/  # CI/CD 配置
└── README.md
```

通过以上步骤，你将拥有一个自动化构建的统一文档系统，整合了 Vue.js 前端组件文档和 FastAPI 后端 API 文档。