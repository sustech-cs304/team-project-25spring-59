// vite.config.ts
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

export default defineConfig({
  plugins: [vue()],
  base: '/',  // 使用绝对路径，而不是相对路径
  server: {
    port: 5173,
    strictPort: true,
    historyApiFallback: true,
  },
  preview: {
    port: 4173,
    strictPort: true,
    historyApiFallback: true,
  },
  build: {
    // 确保资源路径正确
    assetsDir: 'assets',
    rollupOptions: {
      output: {
        manualChunks: undefined
      }
    }
  },
  // test配置
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
