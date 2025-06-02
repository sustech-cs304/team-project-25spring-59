# final-report-59

## 4. Build

### **4.1 构建技术、工具、框架与方法**

*   **前端 (`frontier-app`)**:
    *   **Node.js 和 npm**: Node.js 作为 JavaScript 的运行时环境。npm 用于管理前端项目的依赖库，并执行构建脚本。
    *   **Vite**: 一个高性能的前端构建工具，用于编译 Vue.js 单文件组件、TypeScript/JavaScript 代码、CSS 等，并进行优化、打包，生成静态资源文件。
    *   **Vue.js**: 前端框架，项目的用户界面基于此构建。

*   **后端 (`backapp`)**:
    *   **Python 和 pip (Pip Installs Packages)**: Python 是后端服务的主要编程语言。pip 用于从 Python Package Index (PyPI) 安装项目所需的库。
    *   后端的“构建”主要集中在依赖安装和环境配置上，因为 Python 是解释型语言，不需要像编译型语言那样的显式编译步骤。
    
*   **构建脚本与自动化**:
    *   **批处理脚本 (`build.bat` ) (本地/Windows)**: 一个自定义的批处理脚本，自动化了本地环境下的构建步骤，包括前端编译、后端依赖安装和前后端产物整合。
    *   **Jenkins (`Jenkinsfile`)**: 用于持续集成（CI）。`Jenkinsfile` 中定义了构建阶段，自动化从代码检出到编译打包的流程。

*   **构建方法**:
    *   前端应用首先通过 Vite 独立编译成静态资源。后端则通过 pip 安装依赖。随后，前端的静态产物被整合到后端项目的静态文件目录中。

### **4.2 自动化构建执行的任务**

自动化构建（[`Jenkinsfile`](https://github.com/sustech-cs304/team-project-25spring-59/blob/main/Jenkinsfile)）流程主要执行以下任务：

*   **激活虚拟环境**
*   **Checkout** 
    *   从版本控制系统（如 Git）获取最新的源代码。
*   **Frontend Build**:
    1.  **依赖安装**: 执行 `npm install` (或 `npm ci` 在 CI 环境中)命令，根据[`package.json`](https://github.com/sustech-cs304/team-project-25spring-59/blob/main/frontier-app/package.json)下载并安装所有前端依赖。
    2.  **代码编译**: 执行 `npm run build` 命令，将 Vue.js 组件、JavaScript/TypeScript 代码和 CSS 等静态资源进行编译、代码分割、Tree Shaking、压缩和混淆。
*   **Backend Build**:
    *   执行 `pip install -r requirements.txt` 命令，安装所有在 [`requirements.txt`](https://github.com/sustech-cs304/team-project-25spring-59/blob/main/requirements.txt) 中声明的 Python 依赖包。
    *   将前端构建产物 (`frontier-app/dist/` 目录下的所有内容) 复制到后端项目指定的静态文件目录 (`backapp/static/`)。

*   **Generate Frontend Docs**
    *   生成用户文档和开发者文档

*   **Metrics**:
    *   使用 cloc 统计前端代码行数
    *   使用 Plato 分析圈复杂度
    *   使用 jq 统计依赖数量
    *   使用 pipdeptree 导出依赖结构
*   **Wheel Package Build**
    *   将整合后的前端后端、requirement等生成wheel包

*   **Testing**
    *   进行前端和后端的测试，并生成报告

*   **Artifact Archiving**
    *   将所有的产物（test report、docs、wheel包）进行归档


### 4.3 成功构建的最终产物

*   **前端静态资源**:
    *   **位置**: [`frontier-app/dist/`](https://github.com/sustech-cs304/team-project-25spring-59/tree/frontier-app/dist)
    *   **内容**: 包含 HTML, CSS, JavaScript 文件以及图片等其他静态资源。这些文件经过了编译、压缩和优化，可以直接部署到任何静态 Web 服务器，或由后端应用提供服务。
*   **配置好的后端应用代码及依赖**:
    *   **位置**: `backapp/`
    *   **内容**: 包含所有后端 Python 源代码，并且其运行所需的依赖已通过 `pip install -r requirements.txt` 在虚拟环境中准备好
*   **整合后的应用结构**:
    *   **位置**: [`backapp/static/`](https://github.com/sustech-cs304/team-project-25spring-59/tree//main/backapp/static)
    *   包含前端的`dist/`目录的内容

### **4.4 构建文件/脚本**

以下是项目中用于定义和执行构建过程的关键文件和脚本：

* [`package.json`](https://github.com/sustech-cs304/team-project-25spring-59/blob/main/frontier-app/package.json):

  *   **用途**: 定义前端项目的构建命令。<img src=".\iamges\image-20250601195230937.png" alt="image-20250601195230937" style="zoom:33%;" />

*  [`requirements.txt`](https://github.com/sustech-cs304/team-project-25spring-59/blob/main/requirements.txt) 
  * **用途**: 列出后端 Python 项目运行所需的所有依赖包。<img src=".\iamges\image-20250601195256035.png" alt="image-20250601195256035" style="zoom:33%;" />

    

* [`Jenkinsfile`](https://github.com/sustech-cs304/team-project-25spring-59/blob/main/Jenkinsfile)

  *   **用途**: 定义 Jenkins CI 流水线中的构建步骤。<img src=".\iamges\image-20250601195337242.png" alt="image-20250601195337242" style="zoom:33%;" />

### 4.5 Jenkins成功运行的截图

<img src=".\iamges\image-20250601200857252.png" alt="image-20250601200857252" style="zoom:33%;" />

---

## **5. Deployment - Containerization**

### **5.1 容器化技术、工具、框架与方法**

*   **Docker**:
    *   **核心技术**: Docker 是一个开源的应用容器引擎，允许开发者将应用及其依赖打包到一个轻量级、可移植的容器中
    *   **`Dockerfile`**: 每个需要容器化的服务（前端、后端，或整合后的应用）都有一个 `Dockerfile`。这是一个文本文件，包含了一系列指令，用于告诉 Docker 如何构建该服务的镜像。指令包括指定基础镜像、复制文件、运行命令（如安装依赖、设置环境变量）和定义容器启动命令。
*   **Docker Compose**:
    *   **工具**: Docker Compose 是一个用于定义和运行多容器 Docker 应用程序的工具。
    *   **`docker-compose.yml`**: 通过一个 YAML 文件 (`docker-compose.yml`) 来配置应用的服务、网络和卷。这使得开发者可以用一条命令 (`docker-compose up`) 启动、停止和管理整个应用栈（例如，前端容器、后端容器、数据库容器）。
*   **容器化方法**:
    *   前端和后端被构建为独立的 Docker 镜像，并通过 Docker Compose 进行编排。前端镜像包含一个 Web 服务器（Nginx）来服务静态文件，后端镜像包含应用服务器（Uvicorn）来运行 FastAPI 应用。

### **5.2 容器化脚本**

*   **前端的[`frontier-app/Dockerfile`](https://github.com/sustech-cs304/team-project-25spring-59/blob/main/frontier-app/Dockerfile)**:
    
    * **用途**: 部署前端
    
      <img src=".\iamges\image-20250601195927071.png" alt="image-20250601195927071" style="zoom:33%;" />
    
*   **后端的[`backapp/Dockerfile`](https://github.com/sustech-cs304/team-project-25spring-59/blob/main/backapp/Dockerfile)**:
    
    *   **用途**: 构建后端<img src=".\iamges\image-20250601200059848.png" alt="image-20250601200059848" style="zoom:33%;" />
    
*   **[nginx.conf](https://github.com/sustech-cs304/team-project-25spring-59/blob/main/frontier-app/nginx.conf) (Nginx 配置文件)**:
    
    *   **用途**: 配置 Nginx 服务前端SPA，确保路由正确。<img src=".\iamges\image-20250601200219167.png" alt="image-20250601200219167" style="zoom:33%;" />
    
*   **[docker-compose.yml](https://github.com/sustech-cs304/team-project-25spring-59/blob/main/docker-compose.yml)**:
    
    *   **用途**: 定义和编排多容器应用（前端、后端、数据库）。<img src=".\iamges\image-20250601200352831.png" alt="image-20250601200352831" style="zoom:33%;" />
    
    
    
    

### **5.3 成功容器化**

1.  **`docker images` 命令显示新构建的镜像**:
    执行 `docker ps` 命令,查看正在运行中的容器，前端和后端正常运行。<img src=".\iamges\image-20250601200522340.png">
2.  **应用可访问和功能正常**:
    *   **前端**: 在浏览器中访问为前端服务映射的主机端口（ `http://localhost:80`），能看到应用界面并能与之交互。
    *   **后端**: 后端 API 端点能通过映射的端口（例如 `http://localhost:8000`）被访问，并且前端发起的 API 请求能得到正确响应。