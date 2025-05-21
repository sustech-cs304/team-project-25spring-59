<template>
  <div class="transition-container">
    <!-- 背景图片 -->
    <div class="background"></div>

    <!-- 轮换图片（添加上下浮动效果） -->
    <img class="center-image floating" :src="currentImage" alt="Loading..." />

    <!-- 进度条 -->
    <div class="progress-wrapper">
      <span class="progress-text">{{ progress }}%</span>
      <div class="progress-bar-container">
        <div class="progress-bar" :style="{ width: progress + '%' }"></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from "vue";
import { useRoute, useRouter } from "vue-router";

const router = useRouter();
const route = useRoute();

const images = ["/transform/1.png", "/transform/2.png", "/transform/3.png", "/transform/4.png"];
const currentIndex = ref(0);
const currentImage = ref(images[currentIndex.value]);
const progress = ref(0);

let intervalId, progressInterval;

// **图片轮播**
onMounted(() => {
  intervalId = setInterval(() => {
    currentIndex.value = (currentIndex.value + 1) % images.length;
    currentImage.value = images[currentIndex.value];
  }, 500);

  // **模拟下载进度**
  progressInterval = setInterval(() => {
    if (progress.value < 100) {
      progress.value += 10;
    }
  }, 250);

  // **2.5 秒后跳转到目标页面**
  setTimeout(() => {
  clearInterval(intervalId);
  clearInterval(progressInterval);

  // 获取跳转路径
  const redirectPath = route.query.redirect || '/';
  router.push(redirectPath);

  // if (redirectPath === '/trainMission') {
  //   // 目标是 /trainMission，跳转到 3000 端口
  //   window.location.href = 'http://10.12.184.92:3000/';
  // } else {
  //   // 其他路径正常跳转
  //   router.push(redirectPath);
  // }
  }, 250); // 在这里transition时间被缩短了10倍，正常是2500，记得改回来

});

// **清除定时器**
onUnmounted(() => {
  clearInterval(intervalId);
  clearInterval(progressInterval);
});
</script>

<style scoped>
/* 📌 过渡界面容器 */
.transition-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  background: url("/transform/background.png") no-repeat center center;
  background-size: cover;
}

/* 📌 轮换图片样式（增加浮动动画） */
.center-image {
  width: 200px;
  height: auto;
  animation: fadeIn 0.5s ease-in-out, floatUpDown 3s ease-in-out infinite;
}

/* 📌 让图片有上下浮动效果 */
@keyframes floatUpDown {
  0% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-50px);
  }
  100% {
    transform: translateY(0px);
  }
}

/* 📌 进度条区域 */
.progress-wrapper {
  margin-top: 20px;
  text-align: center;
}

/* 📌 蓝色文字（百分比） */
.progress-text {
  font-size: 18px;
  font-weight: bold;
  color: #42a5f5;
}

/* 📌 进度条容器 */
.progress-bar-container {
  width: 200px;
  height: 8px;
  background: rgba(255, 255, 255, 0.3);
  border-radius: 5px;
  margin-top: 5px;
  overflow: hidden;
}

/* 📌 进度条 */
.progress-bar {
  height: 100%;
  background: #42a5f5;
  transition: width 0.25s ease-in-out;
}

/* 字体 */
@font-face {
  font-family: TVPS-Vain-Capital-2;
  src: url(https://webcnstatic.yostar.net/ba_cn_web/prod/web/assets/TVPS-Vain-Capital-2.cca90a05.ttf);
}

/* 📌 图片淡入动画 */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: scale(0.9);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}
</style>
