pipeline {
    agent any
    
    tools {
        nodejs 'NodeJS' // 确保Jenkins已配置NodeJS工具
    }
    
    environment {
        // 环境变量
        DOCKER_COMPOSE_VERSION = '1.29.2'
        PROJECT_NAME = 'personal-health-assistant'
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
        
        stage('Compilation and Packaging') {
            parallel {
                stage('Frontend Build') {
                    steps {
                        dir('frontier-app') {
                            // 安装前端依赖
                            sh 'npm install'
                            
                            // 构建前端项目
                            sh 'npm run build'
                            
                            echo "前端构建完成"
                        }
                    }
                }
                
                stage('Backend Build') {
                    steps {
                        dir('backapp') {
                            // 创建虚拟环境
                            sh 'python3 -m venv venv || true'
                            
                            // 激活虚拟环境并安装依赖
                            sh '''
                                . venv/bin/activate
                                pip install --upgrade pip
                                pip install -r requirements.txt
                            '''
                            
                            echo "后端依赖安装完成"
                        }
                    }
                }
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
                    .\\.venv\\Scripts\\python.exe -m pip install radon
                    radon cc . -s -a > reports\\python-complexity.txt
                    cd ..

                    REM 3. 使用 pipdeptree 导出依赖结构
                    cd backapp
                    .\\.venv\\Scripts\\python.exe -m pip install pipdeptree
                    .\\.venv\\Scripts\\pipdeptree > reports\\python-dependencies.txt
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
                
                // 如果后端有构建产物，也可以归档
                // archiveArtifacts artifacts: 'backapp/dist/**/*', fingerprint: true
                
                echo "构建产物已归档"
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