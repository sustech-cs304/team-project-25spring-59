<template>
  <header class="header">
    <nav class="nav">
      <!-- 左侧 Logo -->
      <div class="left-decoration">
        <span class="logo">
          <img src="/assets/icon/navLogo.svg" alt="Logo" @dragstart.prevent />
        </span>
      </div>

      <!-- 中间导航菜单 -->
      <ul class="menu">
        <li v-for="item in menuList" :key="item.url">
          <a :href="base + item.url">{{ item.name }}</a>
        </li>
      </ul>

      <div class="spacer" /> <!-- 用于撑开右侧空间 -->
    </nav>
  </header>
</template>

<script setup lang="ts">
import { defineProps, ref } from 'vue'

// 接收 base 作为 prop，用于拼接链接
defineProps<{
  base: string
}>()

interface MenuItem {
  name: string
  url: string
}

const menuList: MenuItem[] = [
  { name: '首页', url: 'TrainMission' },
  { name: '运动界面', url: 'TrainMission/Specification' },
  { name: '任务列表', url: 'TrainMission/Plans' },
  { name: '训练数据', url: 'TrainMission/Dashboard' },
  { name: '返回大厅', url: 'carousel' }
]
</script>

<style lang="scss">
:root {
  --triangle-background: repeating-linear-gradient(
      60deg,
      rgba(190, 242, 255, 0.3),
      transparent 35px
    ),
    repeating-linear-gradient(180deg, transparent, rgba(108, 230, 255, 0.3) 30px),
    repeating-linear-gradient(120deg, rgba(16, 179, 215, 0.3), transparent 46px);
}

.header {
  position: fixed;
  top: 0;
  width: 50%;
  left: 25%;
  height: 72px;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
  border-radius: 0 0 32px 32px;
  border-bottom: 2px solid white;
  backdrop-filter: blur(15px);
  padding: 0 20px;
  box-shadow: inset 0 0 0 1px rgba(255, 255, 255, 1);
  background: linear-gradient(to right,
         rgba(255, 255, 255, 0) 0%,
         rgba(255, 255, 255, 0.3) 10%,
         rgba(255, 255, 255, 0.6) 20%,
         rgba(255, 255, 255, 0.9) 25%,
         rgba(255, 255, 255, 1) 26%,
         rgba(255, 255, 255, 1) 100%),
         var(--triangle-background);
  background-position: 3px 0;
  background-clip: padding-box;
}

.nav {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  max-width: 1200px;
}

.left-decoration {
  display: flex;
  align-items: center;
  padding: 12px;
  position: relative;
  overflow: hidden;
  width: 160px;
  height: 100%;
  left: -30px;
}

.logo img {
  height: 36px;
  width: auto;
  filter: drop-shadow(0 0 8px #328cfa);
  position: relative;
  z-index: 10;
}

.menu {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 32px;
  list-style: none;
  margin: 0;         // ✅ 去掉原来的负 margin
  padding: 0;
  flex: 1;           // ✅ 让它在中间自动占据剩余空间
  text-align: center;
}

.menu li a {
  font-size: 18px;
  font-weight: 600;
  color: #4c5866;
  text-decoration: none;
  padding: 10px 16px;
  border-radius: 8px;
  transition: all 0.3s ease-in-out;

  &:hover {
    color: #ffe401;
    background-color: #425c8b;
    transform: translateY(-2px);
  }
}

.spacer {
  width: 160px; // 与 .left-decoration 宽度一样，撑出对称布局
}
</style>
