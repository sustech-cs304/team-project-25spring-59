export default {
    components: [
        'src/views/[A-Z]*.vue',
        'src/components/**/[A-Z]*.vue',
        '!src/components/Spine-Player-Dashboard/[A-Z]*.vue',
        '!src/components/Spine-Player-MainMenu/[A-Z]*.vue',
        '!src/components/test/[A-Z]*.vue',
        '!src/components/TrainMission/**/[A-Z]*.vue',
    ],
    outDir: 'docs/components',
    defaultExamples: true,  // 为没有示例的组件生成默认示例
    apiOptions: {
        jsx: false,  // 是否支持 JSX
        scriptSetup: true, // 明确启用script setup支持
    },
    getDocFileName: (componentPath) =>
        componentPath.replace(/\.vue$/, '.md'),   // 输出为 Markdown 文件
    jsDoc: 'full'
}