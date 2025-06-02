import { defineConfig } from 'vitepress'

export default defineConfig({
    title: '组件文档',
    description: '',
    themeConfig: {
        sidebar: [
            {
                text: '组件',
                items: [
                    { text: 'BeforeLogin', link: '/components/src/views/BeforeLogin' },
                    { text: 'Carousel', link: '/components/src/views/Carousel' },
                ]
            }
        ]
    }
})