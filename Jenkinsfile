pipeline {
    agent any
    environment {
        // 使用 Jenkins 凭据管理 Docker Hub 认证
        DOCKER_HUB_CREDENTIALS = credentials('2')
        
        // Docker Hub 用户名（从凭据中提取）
        DOCKER_USER = "${env.DOCKER_HUB_CREDENTIALS_USR}"
        
        // 镜像名称
        BACKEND_IMAGE = "team-project-backend"
        FRONTEND_IMAGE = "team-project-frontend"
        
        // 构建标签（使用构建号）
        BUILD_TAG = "${env.BUILD_NUMBER}"
    }
    
    stages {
        stage('检出代码') {
            steps {
                // 检出代码库
                checkout([
                    $class: 'GitSCM',
                    branches: [[name: '*/Deployment']],  // 根据你的分支名修改
                    extensions: [],
                    userRemoteConfigs: [[
                        url: 'https://github.com/sustech-cs304/team-project-25spring-59.git'  // 替换为实际 URL
                    ]]
                ])
            }
        }
        
        stage('构建前端镜像') {
            steps {
                script {
                    // 构建前端镜像
                    docker.build("${env.BACKEND_IMAGE}:${env.BUILD_TAG}", './frontend')  
                }
            }
        }
        
        stage('构建后端镜像') {
            steps {
                script {
                    // 构建后端镜像
                    docker.build("${env.FRONTEND_IMAGE}:${env.BUILD_TAG}", './backend') 
                }
            }
        }
        
        stage('登录 Docker Hub') {
            steps {
                script {
                    // 使用凭据登录 Docker Hub
                    withCredentials([usernamePassword(
                        credentialsId: '2',
                        usernameVariable: 'viayu',
                        passwordVariable: 'shiyansong123'
                    )]) {
                        sh "echo ${env.DOCKER_PASSWORD} | docker login -u ${env.DOCKER_USERNAME} --password-stdin"
                    }
                }
            }
        }
        
        stage('推送镜像') {
            steps {
                script {
                    // 标记并推送前端镜像
                    docker.withRegistry('https://registry.hub.docker.com', '2') {
                        // 标记后端镜像
                        def backendImage = docker.image("${env.BACKEND_IMAGE}:${env.BUILD_TAG}")
                        backendImage.push()
                        backendImage.push('latest')  // 额外推送 latest 标签
                        
                        // 标记并推送后端镜像
                        def frontendImage = docker.image("${env.FRONTEND_IMAGE}:${env.BUILD_TAG}")
                        frontendImage.push()
                        frontendImage.push('latest')  // 额外推送 latest 标签
                    }
                }
            }
        }
        
        stage('清理') {
            steps {
                script {
                    // 清理旧容器
                    sh(script: '''
                        docker stop backend-container || true
                        docker rm backend-container || true
                        
                        docker stop frontend-container || true
                        docker rm frontend-container || true
                    ''', returnStatus: true)
                    
                    // 运行新容器
                    sh "docker run -d -p 8080:8080 --name backend-container ${env.DOCKER_USER}/${env.BACKEND_IMAGE}:${env.BUILD_TAG}"
                    sh "docker run -d -p 3000:3000 --name frontend-container ${env.DOCKER_USER}/${env.FRONTEND_IMAGE}:${env.BUILD_TAG}"
                }
            }
        }
    }
    
    post {
        always {
            // 清理 Docker 系统
            sh 'docker system prune -af'
        }
    }
}