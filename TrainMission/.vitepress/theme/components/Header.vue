<template>
  <header class="header">
    <nav class="nav">
      <!-- 左侧装饰 + Logo -->
      <div class="left-decoration">
        <span class="logo">
          <img src="/vitepress-theme-sakura/assets/icon/navLogo.svg" alt="Logo" @dragstart.prevent />
        </span>
      </div>

      <!-- 中间导航菜单 -->
      <ul class="menu">
        <li v-for="item in menuList" :key="item.url">
          <a :href="base + item.url">{{ item.name }}</a>
        </li>
      </ul>

       <!-- 右侧控件（搜索 & 汉堡菜单 & 下拉菜单按钮） -->
      <div class="right-controls">
        <!-- ✅ 右上角透明按钮 -->
        <button class="dropdown-button" @click="toggleDropdown">☰</button>

        <!-- ✅ DropdownMenu 组件 -->
        <DropdownMenu :showMenu="showDropdownMenu" class="dropdown-container" />
      </div>
    </nav>

    <!-- 移动端菜单 -->
    <DropdownMenu :showMenu="showDropdown" />
  </header>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useData } from 'vitepress'
import DropdownMenu from './Navbar/Dropdown-Menu.vue'

const base = useData().site.value.base
const showDropdown = ref(false)

interface MenuItem {
  name: string
  url: string
}

const menuList: MenuItem[] = [
  { name: '首页', url: '' },
  { name: '运动标签', url: 'tags/' },
  { name: '任务列表', url: 'plans/' },
  { name: '训练数据', url: 'dashboard/' }
]

// 切换移动端菜单
const toggleDropdown = () => {
  showDropdown.value = !showDropdown.value
}
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
/* 头部整体 */
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
  //box-shadow: 0px 6px 12px rgba(40, 135, 200, 0.3);
  backdrop-filter: blur(15px);
  padding: 0 20px;
  box-shadow: inset 0 0 0 1px rgba(255, 255, 255, 1); /* ✅ 内部创建 1px 白色边框 */

  background: linear-gradient(to right,
         rgba(255, 255, 255, 0) 0%, /* 透明 */
         rgba(255, 255, 255, 0.3) 10%, /* 开始渐变 */
         rgba(255, 255, 255, 0.6) 20%, /* 逐渐变白 */
         rgba(255, 255, 255, 0.9) 25%, /* 25% 位置接近白色 */
         rgba(255, 255, 255, 1) 26%, /* 26% 位置完全变为白色 */
         rgba(255, 255, 255, 1) 100%), /* 之后一直白色 */
         var(--triangle-background);
  background-position: 3px 0; /* 让背景向右偏移 20px */
  background-clip: padding-box; /* ✅ 限制背景在圆角内 */

}

/* 导航栏布局 */
.nav {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  max-width: 1200px;

}

/* 左侧装饰 + Logo */
.left-decoration {
  display: flex;
  align-items: center;
  padding: 12px;
  position: relative;
  overflow: hidden;
  width: 160px; /* 扩展宽度 */
  height: 100%;
  left: -30px;
}

//.left-decoration::before {
//  content: "";
//  position: absolute;
//  top: 0;
//  left: 0; /* 让装饰从 header 左侧开始 */
//  width: 100%; /* 让它填满整个 header */
//  height: 100%;
//  background: var(--triangle-background);
//  border-radius: 0 0 32px 32px; /* 与 header 一致 */
//  clip-path: inset(0 0 0 0 round 0 0 32px 32px); /* 确保背景跟随圆角 */
//  opacity: 0.8;
//  z-index: -1; /* 确保它不会覆盖内容 */
//}


/* ✅ 让 Logo 也保持在装饰区域内 */
.logo img {
  height: 36px;
  width: auto;
  filter: drop-shadow(0 0 8px #328cfa);
  position: relative;
  z-index: 10;
}

.test-background {
  background: var(--triangle-background);
  width: 300px;
  height: 300px;
}


/* 菜单导航 */
.menu {
  display: flex;
  align-items: center;
  gap: 32px;
  list-style: none;
  margin-left: -200px;
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

/* 右侧控件（搜索 & 汉堡菜单） */
.right-controls {
  display: flex;
  align-items: center;
  gap: 16px;
}



/* 汉堡菜单（移动端） */
.hamburger {
  display: none;
  flex-direction: column;
  width: 32px;
  cursor: pointer;
}

.hamburger .line {
  display: block;
  width: 80%;
  height: 4px;
  border-radius: 4px;
  background-color: #4c5866;
  margin-bottom: 4px;
  transition: all 0.3s ease-in-out;
}

.hamburger.active .line:nth-child(1) {
  transform: translateY(8px) rotate(45deg);
}
.hamburger.active .line:nth-child(2) {
  opacity: 0;
}
.hamburger.active .line:nth-child(3) {
  transform: translateY(-8px) rotate(-45deg);
}



/* 适配移动端 */
@media (max-width: 768px) {
  .menu {
    display: none;
  }

  .hamburger {
    display: flex;
  }
}
</style>
