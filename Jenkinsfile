pipeline {
    agent any
    
    tools {
        nodejs 'NodeJS' // 确保Jenkins已配置NodeJS工具
    }
    
    environment {
        // 环境变量
        DOCKER_COMPOSE_VERSION = '1.29.2'
        PROJECT_NAME = 'personal-health-assistant'
        VENV_NAME = 'venv'  // 虚拟环境名称
    }
    
    stages {
        stage('Checkout') {
            steps {
                // 检出代码
                checkout scm
                echo "代码检出完成"
            }
        }
        
        stage('Linting') {
            steps {
                echo "这里将进行代码检查"
                // TODO: 实现代码检查（暂时留空）
            }
        }
        
        stage('Build Application') {
            parallel {
                stage('Frontend Build') {
                    steps {
                        dir('frontier-app') {
                            // 安装前端依赖
                            bat 'npm ci'
                            
                            // 构建前端项目
                            bat 'npm run build'
                            
                            echo "前端构建完成"
                        }
                    }
                }
                
                stage('Backend Build') {
                    steps {
                        // 创建并激活Python虚拟环境
                        bat '''
                            python -m venv %VENV_NAME%
                            call %VENV_NAME%\\Scripts\\activate.bat
                            python -m pip install --upgrade pip
                        '''
                        
                        // 安装后端依赖
                        bat '''
                            call %VENV_NAME%\\Scripts\\activate.bat
                            pip install -r requirements.txt --no-cache-dir
                        '''
                        
                        // 生成wheel包
                        bat '''
                            call %VENV_NAME%\\Scripts\\activate.bat
                            pip install wheel
                            cd backapp
                            python setup.py bdist_wheel
                            cd ..
                        '''
                        
                        echo "后端构建完成，wheel包已生成"
                    }
                }
            }
        }
        
        stage('Integration') {
            steps {
                // 创建静态文件目录（如果不存在）
                bat 'if not exist backapp\\static mkdir backapp\\static'
                
                // 复制前端构建文件到后端静态目录 - 使用Windows xcopy命令
                bat 'xcopy /E /Y frontier-app\\dist\\* backapp\\static\\'
                
                echo "前后端集成完成：前端静态文件已复制到后端静态目录"
            }
        }
        
        stage('Testing') {
            steps {
                echo "这里将进行自动化测试"
                // TODO: 实现自动化测试（暂时留空）
            }
        }
        
        stage('Test Report Generation') {
            steps {
                echo "开始生成前端和后端的测试报告..."

                // ---------- 前端报告 ----------
                echo "生成前端报告..."
                bat '''
                    if not exist frontier-app\\reports mkdir frontier-app\\reports

                    REM 1. 使用 cloc 统计前端代码行数
                    cloc.exe frontier-app --exclude-dir=node_modules,dist,.venv,__pycache__ --out=frontier-app\\reports\\cloc_report.txt

                    REM 2. 使用 Plato 分析圈复杂度
                    cd frontier-app
                    npx plato -r -d reports ./src
                    cd ..

                    REM 3. 使用 jq 统计依赖数量
                    cd frontier-app
                    echo 直接依赖数量: > reports\\dependency_summary.txt
                    npm ls --depth=0 --json | ..\\jq.exe ".dependencies | keys | length" >> reports\\dependency_summary.txt
                    echo 所有依赖数量（含 dev）: >> reports\\dependency_summary.txt
                    npm ls --depth=0 --json | ..\\jq.exe "[.dependencies, .devDependencies] | map(keys | length) | add" >> reports\\dependency_summary.txt
                    cd ..
                '''

                // ---------- 后端报告 ----------
                echo "生成后端报告..."
                bat '''
                    if not exist backapp\\reports mkdir backapp\\reports

                    REM 1. 使用 cloc 统计后端代码行数
                    cloc.exe backapp --exclude-dir=__pycache__,.venv --out=backapp\\reports\\cloc_report.txt

                    REM 2. 使用 radon 分析圈复杂度
                    cd backapp
                    ..\\%VENV_NAME%\\Scripts\\python.exe -m pip install radon
                    ..\\%VENV_NAME%\\Scripts\\radon cc . -s -a > reports\\python-complexity.txt
                    cd ..

                    REM 3. 使用 pipdeptree 导出依赖结构
                    cd backapp
                    ..\\%VENV_NAME%\\Scripts\\python.exe -m pip install pipdeptree
                    ..\\%VENV_NAME%\\Scripts\\pipdeptree > reports\\python-dependencies.txt
                    cd ..
                '''

                echo "✅ 所有测试报告已生成：frontier-app/reports 和 backapp/reports"
            }
        }
        
        stage('Documentation Generation') {
            steps {
                echo "这里将生成文档"
                // TODO: 实现文档生成（暂时留空）
            }
        }
        
        stage('Artifact Archiving') {
            steps {
                // 归档构建产物
                archiveArtifacts artifacts: 'frontier-app/dist/**/*', fingerprint: true
                archiveArtifacts artifacts: 'backapp/static/**/*', fingerprint: true
                // 归档wheel包
                archiveArtifacts artifacts: 'backapp/dist/*.whl', fingerprint: true
                
                echo "构建产物已归档"
            }
        }
        
        stage('Deployment') {
            steps {
                echo "终止可能运行中的服务..."
                // 使用Windows任务管理器终止进程
                bat '''
                    taskkill /F /IM node.exe /T >nul 2>&1 || echo 没有Node进程在运行
                    taskkill /F /FI "WINDOWTITLE eq frontend*" >nul 2>&1 || echo 没有前端窗口
                    taskkill /F /FI "WINDOWTITLE eq backend*" >nul 2>&1 || echo 没有后端窗口
                '''
                
                echo "安装wheel包到部署环境..."
                // 创建部署环境并安装wheel包
                bat '''
                    if not exist deploy_env python -m venv deploy_env
                    call deploy_env\\Scripts\\activate.bat
                    pip install --find-links=backapp\\dist\\ personal-health-assistant --no-index
                '''
                
                echo "启动生产服务器..."
                // 使用Windows start命令启动后端服务器
                bat '''
                    call deploy_env\\Scripts\\activate.bat
                    start "server" cmd /c "uvicorn backapp.main:app --host 0.0.0.0 --port 8000"
                '''
                
                echo "应用已部署：前端访问地址 http://localhost:8000"
            }
        }
    }
    
    post {
        always {
            // 清理工作区
            cleanWs()
        }
        success {
            echo "构建成功！"
        }
        failure {
            echo "构建失败，请检查日志"
        }
    }
} 