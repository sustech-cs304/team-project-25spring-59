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
                echo "这里将生成测试报告"
                // TODO: 实现测试报告生成（暂时留空）
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