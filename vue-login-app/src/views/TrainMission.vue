<template>
  <div class="train-mission">
    <!-- 头部 Banner -->
    <Banner />
    <!-- Name Banner -->
    <NameBanner />

    <div class="container">
      <!-- 其他内容 -->
    </div>
  </div>
</template>

<script setup>
import Banner from '../../src/components/TrainMissionComponents/Banner.vue'
import NameBanner from "../components/TrainMissionComponents/NameBanner.vue";
</script>

<style scoped>
/* 让整个背景处于最底层 */
.train-mission {
  width: 100vw;
  height: 100vh;
  display: flex;
  flex-direction: column; /* 使 Banner 在顶部，内容部分在下方 */
  align-items: center;
  overflow-y: auto;
  position: relative; /* 确保 NameBanner 相对于此容器定位 */
}

/* 使用伪元素让背景在最底层，限定背景样式只在当前组件中生效 */
.train-mission::before {
  content: "";
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-image: url("/assets/background.svg");
  background-size: cover; /* 确保背景填充整个视口 */
  background-position: right center;
  background-repeat: no-repeat;
  z-index: -2; /* 让背景永远在最底层 */
}

/* 让 Banner 在 NameBanner 之下 */
.train-mission .banner {
  width: 100%;
  height: 75vh;
  z-index: 1; /* 确保 Banner 在 NameBanner 下 */
}

/* 让 NameBanner 放在 Banner 上面，并调整位置 */
.train-mission .name-banner {
  width: 100%;
  position: absolute;
  z-index: 2; /* 保证 NameBanner 在 Banner 上面 */
}

/* 容器区域 */
.train-mission .container {
  position: relative;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  z-index: 3; /* 确保内容层级高于 NameBanner */
}

/* 内容区域 */
.train-mission .content {
  width: 100%;
  max-width: 800px;
  padding: 20px;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  position: relative;
  z-index: 4; /* 确保内容不会被其他层级覆盖 */
}

/* 其他样式保持不变... */
</style>
