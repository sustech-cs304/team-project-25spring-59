// vite.config.ts
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  base: './',
  // test: {
  //   globals: true,
  //   environment: 'jsdom',
  // },
   test: {
    globals: true,            // 允许使用 describe/test/vi 等全局变量
    environment: 'jsdom',     // 模拟 DOM 环境，Vue 组件必须
    coverage: {
      provider: 'v8',
      reporter: ['text', 'html'],
      reportsDirectory: './coverage',
      all: true,
      include: ['src/**/*.{js,ts,vue}'],
    },
  },
  setupFiles: ['./vitest.setup.ts']
})
