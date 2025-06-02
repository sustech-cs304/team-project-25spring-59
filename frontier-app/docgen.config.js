export default {
    components: 'src/views/**/[A-Z]*.vue', // 匹配组件文件
    outDir: 'docs/components',                         // 输出目录
    defaultExamples: true,                      // 为没有示例的组件生成默认示例
    apiOptions: {
        jsx: false                                // 是否支持 JSX
    },
    getDocFileName: (componentPath) =>
        componentPath.replace(/\.vue$/, '.md'),   // 输出为 Markdown 文件
    templates: {
        // 自定义模板配置（后续会详细介绍）
    }
}