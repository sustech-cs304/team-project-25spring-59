# Jenkins 配置指南

## 前提条件

1. WSL Ubuntu已安装
2. Jenkins已在WSL Ubuntu中安装并运行
3. Docker和Docker Compose已在WSL Ubuntu中安装
4. Node.js已在WSL Ubuntu中安装

## 安装必要的Jenkins插件

在Jenkins管理界面中安装以下插件：

1. **Pipeline** - 支持Pipeline作为代码
2. **Git** - Git集成
3. **Docker Pipeline** - Docker集成
4. **NodeJS Plugin** - Node.js集成
5. **Workspace Cleanup Plugin** - 工作区清理

## 配置Jenkins工具

1. 进入 **Dashboard > Manage Jenkins > Tools**
2. 配置NodeJS：
   - 点击"NodeJS installations..."
   - 点击"Add NodeJS"
   - 填写名称为"NodeJS"
   - 选择适当的版本（例如NodeJS 18.x）
   - 保存

3. 配置Python（如果需要）：
   - 点击"Python installations..."
   - 点击"Add Python"
   - 填写名称为"Python3"
   - 选择适当的版本
   - 保存

## 创建Jenkins Pipeline项目

1. 进入Jenkins Dashboard
2. 点击"New Item"
3. 输入项目名称（例如"personal-health-assistant"）
4. 选择"Pipeline"
5. 点击"OK"

## 配置Pipeline

1. 在"Pipeline"部分，选择"Pipeline script from SCM"
2. SCM选择"Git"
3. 在"Repository URL"中输入您的Git仓库URL
4. 在"Branch Specifier"中输入分支名（例如*/main或*/master）
5. 在"Script Path"中输入"Jenkinsfile"
6. 点击"Save"

## 运行Pipeline

配置完成后，您可以通过以下方式触发构建：

1. 手动触发：点击"Build Now"
2. 配置Webhook实现自动触发：
   - 在Github/GitLab中设置Webhook
   - 触发URL为：`http://your-jenkins-url/generic-webhook-trigger/invoke?token=YOUR_TOKEN`

## 故障排除

如果遇到权限问题，可能需要在WSL中执行以下命令：

```bash
# 确保Jenkins用户可以运行Docker
sudo usermod -aG docker jenkins

# 重启Jenkins服务
sudo systemctl restart jenkins
```

如果遇到Node.js或Python路径问题，检查Jenkins的全局工具配置是否正确指定了路径。 