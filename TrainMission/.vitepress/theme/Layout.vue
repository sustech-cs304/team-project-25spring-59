<template>
  <div class="layout-wrapper">
    <div class="background-color-layer" />
    <div class="background-image-layer" />
    <Header />
    <aside />
    <main>
      <ToTop />
      <template v-if="path === ''">
        <Banner />
        <BlogList :posts="posts" />
      </template>
      <Tag v-else-if="path === 'tags/'" />
      <Plans v-else-if="path === 'plans/'" />
      <Article v-else />

      <!-- 只有在路径以 .md 结尾时才显示 DeleteButton 和 AlterButton -->
      <DeleteButton v-if="isMdPage" />
      <AlterButton v-if="isMdPage" />
    </main>
  </div>
</template>

<script setup lang="ts">
import Header from './components/Header.vue'
import Banner from './components/Banner.vue'
import Article from './Article.vue'
import BlogList from './BlogList.vue'
import Tag from './Tag.vue'
import Plans from './Plans.vue'
import ToTop from './ToTop.vue'
import DeleteButton from './components/DeleteButton.vue' // 导入自定义删除按钮组件
import AlterButton from './components/AlterButton.vue' // 导入自定义修改按钮组件
import { computed } from 'vue'
import { useRoute, useData } from 'vitepress'
import { data as posts } from '../posts.data'

// 获取站点的基本路径
const base = useData().site.value.base
const route = useRoute()

// 获取当前路径并去除base和index.html
const path = computed(() => {
  console.log('Current path:', JSON.stringify(route.path));  // 使用 JSON.stringify() 输出 path 字符串形式
  return route.path.replace(base, '').replace('index.html', '');
})

// 计算属性，检查路径是否以 .html 结尾（即一个 md 文件）
const isMdPage = computed(() => path.value.endsWith('.html'))

</script>

<style lang="scss">
html {
  scroll-behavior: smooth;
  --global-font: "Noto Serif SC", "MicroSoft Yahei", serif;
  --color-accent: #fe9600;
  --color-gray: #666;
  --color-text: #02111d;
  --color-background: #eee;
  --color-border: #d0d7de;
  --code-line-height: 24px;
  --code-font-family: monospace;
  --code-font-size: 15px;
}

body {
  margin: 0;
  padding: 0;
  font-family: var(--global-font);
  font-size: 16px;
  overflow-x: hidden;
}

* {
  box-sizing: border-box;
}

a {
  text-decoration: none;
}

img {
  max-width: 100%;
}

hr {
  border: none;
  border-bottom: 1px dashed var(--color-border);
}

::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}

::-webkit-scrollbar-thumb {
  border-radius: 4px;
  background: var(--color-accent);
}

.layout-wrapper {
  position: relative;
  min-height: 100vh;
  overflow-x: hidden;

  .background-color-layer {
    background-color: #eaebed; // RGB: 234, 235, 237
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    z-index: -1000;
  }

  .background-image-layer {
    background: url('/assets/background.svg') no-repeat center bottom;
    background-size: cover;
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    z-index: -999;
    pointer-events: none;
  }
}
</style>
