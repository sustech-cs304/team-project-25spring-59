import { defineConfig } from 'vitepress'
import path from 'path'
import fs from 'fs'

// 自动生成侧边栏配置的函数
function getSidebarItems(dir, basePath = '') {
    const items = []
    const fullPath = path.join(__dirname, dir, basePath)

    // 读取目录内容
    const files = fs.readdirSync(fullPath)

    files.forEach(file => {
        const filePath = path.join(fullPath, file)
        const stat = fs.statSync(filePath)
        const relativePath = path.join(basePath, file)

        if (stat.isDirectory()) {
            // 如果是目录，递归处理
            const children = getSidebarItems(dir, relativePath)
            if (children.length > 0) {
                items.push({
                    text: file,
                    collapsed: false, // 默认展开
                    items: children
                })
            }
        } else if (file.endsWith('.md') && !file.startsWith('_')) {
            // 如果是 Markdown 文件且不是以下划线开头
            const link = path.join(dir, relativePath).replace(/\.md$/, '')
            items.push({
                text: file.replace(/\.md$/, ''),
                link: link
            })
        }
    })

    return items
}

// 自动创建 api-reference.md 文件
function createApiReferenceFile() {
    const apiReferencePath = path.join(__dirname, '../api-reference.md')
    const fastapiUrl = 'http://localhost:8000/docs' // 替换为你的 FastAPI 文档地址

    if (!fs.existsSync(apiReferencePath)) {
        const content = `# API 参考文档

## FastAPI 交互式文档

以下是集成的 FastAPI Swagger UI：

<iframe 
    src="${fastapiUrl}" 
    width="100%" 
    height="800px"
    frameborder="0"
></iframe>

## 使用说明
1. 确保 FastAPI 服务正在运行
2. 生产环境请替换上方 iframe 的 src 地址
`
        fs.writeFileSync(apiReferencePath, content)
        console.log('已自动创建 api-reference.md 文件')
    }
}

// 执行文件创建
createApiReferenceFile()

export default defineConfig({
    title: '组件文档',
    description: '',
    themeConfig: {
        sidebar: [
            {
                text: '组件',
                items: getSidebarItems('../components')
            },
            {
                text: 'API 参考',
                link: '/api-reference'
            }
        ]
    },
    vite: {
        resolve: {
            alias: { '@': path.resolve(__dirname, '../../src') }
        }
    }
})