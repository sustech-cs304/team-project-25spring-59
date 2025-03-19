import { defineConfigWithTheme } from 'vitepress'
import fixKatex from './fix-katex'

export interface ThemeConfig {
  name?: string,
  cover?: string,
  hello?: string,
  highText?: string,
  motto?: string,
  social?: { icon: string, url: string }[],
  waline?: string,
}

export default defineConfigWithTheme<ThemeConfig>({
  vite: {
    css: {
      preprocessorOptions: {
        less: {
          javascriptEnabled: true,
          additionalData: `@import './.vitepress/styles/vars.less';`
        }
      }
    }
  },

  lang: 'zh-CN',
  base: '/vitepress-theme-sakura/',
  head: [
    ['link', { rel: 'stylesheet', href: 'https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@6.0.0/css/regular.min.css' }],
    ['link', { rel: 'stylesheet', href: 'https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@6.0.0/css/all.min.css' }],
    ['link', { rel: 'stylesheet', href: 'https://fonts.googleapis.com/css?family=Noto+Serif+SC' }],
    ['script', { src: 'https://cdn.jsdelivr.net/npm/@waline/client@1.5.4/dist/Waline.min.js' }],
    ['script', { src: 'https://cdn.jsdelivr.net/npm/katex@0.15.2/dist/katex.min.js' }],
    ['script', { src: 'https://cdn.jsdelivr.net/npm/katex@0.15.2/dist/contrib/auto-render.min.js' }],
    ['link', { rel: 'stylesheet', href: 'https://cdn.jsdelivr.net/npm/katex@0.15.2/dist/katex.min.css' }],
    ['link', { rel: 'shortcut icon', href: '/favicon.ico' }],
    ['link', { rel: 'stylesheet', href: 'https://unpkg.com/gitalk/dist/gitalk.css' }],
    ['script', { src: 'https://unpkg.com/gitalk/dist/gitalk.min.js' }],
    [
      'link',
      {
        rel: 'stylesheet',
        href: '/font/Blueaka/Blueaka.css',
      },
    ],
    [
      'link',
      {
        rel: 'stylesheet',
        href: '/font/Blueaka_Bold/Blueaka_Bold.css',
      },
    ],
    [
      'link',
      {
        rel: 'stylesheet',
        href: 'https://cdn.jsdelivr.net/npm/@fancyapps/ui/dist/fancybox.css',
      },
    ],
    [
      'script',
      {
        src: 'https://cdn.jsdelivr.net/npm/@fancyapps/ui@4.0/dist/fancybox.umd.js',
      },
    ],
  ],

  markdown: {
    theme: 'github-light',
    lineNumbers: true,
    config: md => {
      md.use(fixKatex)
    }
  },

  themeConfig: {
    name: 'flaribbit',
    cover: '/vitepress-theme-sakura/assets/banner/banner.webp',
    social: [
      { icon: 'fa-github', url: 'https://github.com' },
      { icon: 'fa-twitter', url: 'https://twitter.com' },
      { icon: 'fa-weibo', url: 'https://weibo.com' },
    ],
    waline: 'https://blog-waline-e7jqcxb9s-flaribbit.vercel.app/',
  },

})

