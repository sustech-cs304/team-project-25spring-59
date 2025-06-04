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
                        
                        echo "后端依赖安装完成"

                        // 创建静态文件目录（如果不存在）
                        bat 'if not exist backapp\\static mkdir backapp\\static'
                
                        // 复制前端构建文件到后端静态目录 - 使用Windows xcopy命令
                        bat 'xcopy /E /Y frontier-app\\dist\\* backapp\\static\\'
                
                        echo "前后端集成完成：前端静态文件已复制到后端静态目录"
                    }
                }
            }
        }
        
        stage('Wheel Package Build') {
            steps {
                // 确保static目录有__init__.py文件
                bat '''
                    if not exist backapp\\static\\__init__.py echo # static package initialization > backapp\\static\\__init__.py
                    if not exist backapp\\static\\uploads mkdir backapp\\static\\uploads
                '''
                
                // 生成wheel包
                bat '''
                    call %VENV_NAME%\\Scripts\\activate.bat
                    pip install wheel
                    cd backapp
                    
                    REM 确保包含了必要的__init__.py文件
                    if not exist databases\\__init__.py echo # databases package initialization > databases\\__init__.py
                    if not exist __init__.py echo # backapp package initialization > __init__.py
                    
                    python setup.py sdist bdist_wheel
                    cd ..
                '''
                
                echo "wheel包构建完成，包含所有静态文件"
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

                    REM 4. 使用 vitest 运行测试并生成覆盖率报告
                    npx vitest run --coverage > output.txt 2>&1
                    cd ..

                    REM 启动后端服务到后台
                    start "FastAPI Backend" cmd /c "call venv\\Scripts\\activate.bat && uvicorn backapp.main:app --host 0.0.0.0 --port 8000"

                    REM 等待后端启动
                    ping -n 8 127.0.0.1 > nul

                    REM 安装测试工具（如果尚未安装）
                    call venv\\Scripts\\activate.bat
                    pip install pytest pytest-cov

                    REM 执行测试并生成覆盖率报告
                    pytest test/ --cov=backapp --cov-report=term-missing --cov-report=html > backapp\\reports\\pytest_output.txt
                    
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

        stage('Generate Docs') {
            steps {
                bat '''                
                    call %VENV_NAME%\\Scripts\\activate.bat
                    cd frontier-app
                    
                    :: 安全安装（可选）
                    npm install --save-dev vue-docgen-cli || exit /B 0
                    
                    :: 使用npx确保找到本地命令
                    npx vue-docgen -c docgen.config.js || (
                        echo [WARNING] Doc generation failed, but continuing build...
                        exit /B 0
                    )
                    
                    npm run docs:build
                    npm run docs:preview
                    cd ..
                '''
            }
        }

        
        stage('Artifact Archiving') {
            steps {
                // 归档构建产物
                archiveArtifacts artifacts: 'frontier-app/dist/**/*', fingerprint: true
                archiveArtifacts artifacts: 'backapp/static/**/*', fingerprint: true
                // 归档wheel包
                archiveArtifacts artifacts: 'backapp/dist/*.whl', fingerprint: true
                // 归档前端和后端测试报告
                archiveArtifacts artifacts: 'frontier-app/reports/**/*', fingerprint: true
                archiveArtifacts artifacts: 'backapp/reports/**/*', fingerprint: true

                archiveArtifacts artifacts: 'backend_test_report/**/*', fingerprint: true
                archiveArtifacts artifacts: 'frontier-app/output.txt', fingerprint: true

                // 归档文档
                archiveArtifacts artifacts: 'frontier-app/docs/.vitepress/dist/**/*', fingerprint: true
                
                echo "构建产物已归档"
            }
        }
        
        stage('Deployment') {
                    steps {             
                        echo "应用已部署并在后台运行"
                    }
        }
    }
    
    post {
        always {
            // 不要清理工作区，因为部署依赖于这些文件
            // cleanWs()
            echo "保留工作区以维持服务运行"
        }
        success {
            echo "构建成功！"
        }
        failure {
            echo "构建失败，请检查日志"
        }
    }
} 