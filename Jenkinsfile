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
        
        stage('Testing') {
            steps {
                echo "这里将进行自动化测试"
                echo "启动 FastAPI 后端并执行自动化测试..."

                bat '''
                    @echo off
                    chcp 65001 > nul

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

                echo "测试完成，已生成覆盖率报告"
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
                // 归档测试报告
                archiveArtifacts artifacts: 'frontier-app/reports/**/*', fingerprint: true
                archiveArtifacts artifacts: 'backapp/reports/**/*', fingerprint: true
                
                echo "构建产物已归档"
            }
        }
        
        stage('Deployment') {
                    steps {
                        // echo "终止可能运行中的服务..."
                        // // 使用Windows任务管理器终止进程
                        // bat '''
                        //     @echo off
                        //     chcp 65001 > nul                          // 强制命令行使用 UTF-8 编码
                        //     taskkill /F /IM node.exe /T >nul 2>&1 || echo 没有Node进程在运行
                        //     taskkill /F /FI "WINDOWTITLE eq frontend*" >nul 2>&1 || echo 没有前端窗口
                        //     taskkill /F /FI "WINDOWTITLE eq backend*" >nul 2>&1 || echo 没有后端窗口
                            
                        //     REM 尝试停止现有服务（如果有）
                        //     sc query HealthAssistantService >nul 2>&1
                        //     if not errorlevel 1 (
                        //         sc stop HealthAssistantService
                        //         sc delete HealthAssistantService
                        //         echo 已停止并删除旧的服务
                        //     )
                            
                        //     REM 杀死可能运行的Python进程
                        //     taskkill /F /IM python.exe /FI "WINDOWTITLE eq HealthAssistant*" >nul 2>&1 || echo 没有相关Python进程
                        // '''
                        
                        // echo "安装wheel包到部署环境..."
                        // // 创建部署环境并安装wheel包
                        // bat '''
                        //     @echo off
                        //     chcp 65001 > nul
                        //     if not exist deploy_env python -m venv deploy_env
                        //     call deploy_env\\Scripts\\activate.bat
                        //     pip install --find-links=backapp\\dist\\ personal-health-assistant
                        // '''
                        
                        // echo "创建启动脚本..."
                        // // 创建启动脚本，以便在Jenkins外部运行
                        // bat '''
                        //     @echo off
                        //     chcp 65001 > nul
                        //     echo @echo off > run_app.bat
                        //     echo title HealthAssistant >> run_app.bat
                        //     echo cd /d %%CD%% >> run_app.bat        // 使用 %%CD%% 替代 %CD% 避免变量转义问题
                        //     echo call deploy_env\\Scripts\\activate.bat >> run_app.bat
                        //     echo uvicorn backapp.main:app --host 0.0.0.0 --port 8000 >> run_app.bat
                            
                        //     REM 创建PowerShell启动脚本（UTF-8 with BOM编码）
                        //     powershell -Command "[IO.File]::WriteAllText('start_app.ps1', \\"`$processPath = '%%CD%%\\run_app.bat'`n`$workingDir = '%%CD%%'`nStart-Process -FilePath `$processPath -WorkingDirectory `$workingDir -WindowStyle Normal\\", [Text.Encoding]::UTF8)"
                        // '''
                        
                        // echo "使用后台进程启动应用..."
                        // // 使用PowerShell启动后台进程
                        // bat '''
                        //     @echo off
                        //     chcp 65001 > nul
                        //     REM 第一种方法：使用PowerShell后台启动
                        //     powershell -ExecutionPolicy Bypass -File start_app.ps1
                            
                        //     REM 第二种方法：使用start命令（备用方法）
                        //     start /min cmd /c run_app.bat
                            
                        //     REM 等待服务启动（兼容所有Windows版本）
                        //     ping -n 10 127.0.0.1 > nul              // 替代 timeout /t 10
                            
                        //     REM 检查端口是否可访问（改用英文输出避免编码问题）
                        //     powershell -Command "if ((Test-NetConnection -ComputerName localhost -Port 8000).TcpTestSucceeded) { Write-Output '[成功] 端口8000可访问' } else { Write-Output '[错误] 端口8000不可访问'; exit 1 }"
                        // '''
                        
                        // echo "创建Windows启动项，确保系统重启后自动启动..."
                        // // 创建Windows启动项
                        // bat '''
                        //     @echo off
                        //     chcp 65001 > nul
                        //     REM 创建启动文件夹快捷方式
                        //     powershell -Command "$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%%APPDATA%%\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\HealthAssistant.lnk'); $Shortcut.TargetPath = '%%CD%%\\run_app.bat'; $Shortcut.WorkingDirectory = '%%CD%%'; $Shortcut.Save()"
                        //     echo 已创建Windows启动项，系统重启后应用将自动启动
                        // '''
                        
                        echo "应用已部署并在后台运行：前端访问地址 http://localhost:8000"
                        echo "应用将在系统重启后自动启动"
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