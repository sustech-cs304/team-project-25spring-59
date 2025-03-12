<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";

const router = useRouter();
const isLoading = ref(true); // 控制是否显示启动页面
const progress = ref(0); // 加载进度
const statusText = ref("正在初始化应用..."); // 状态文字

onMounted(async () => {
  await initializeApp();
  isLoading.value = false; // 加载完成后进入 Login 界面
  router.push("/login"); // 自动跳转到登录页面
});

// **前置准备任务**
const initializeApp = async () => {
  try {
    await simulateLoadingStep("检查网络连接...", 20);
    await checkServerStatus();

    await simulateLoadingStep("加载关键资源...", 50);
    await preloadAssets();

    await simulateLoadingStep("应用准备完成！", 100);
  } catch (error) {
    console.error("❌ 应用启动失败", error);
  }
};

// **检查后端服务器是否可用**
const checkServerStatus = async () => {
  try {
    await axios.get("http://127.0.0.1:8000/");
    console.log("✅ 服务器正常运行");
  } catch (error) {
    console.warn("⚠ 服务器无法连接");
  }
};

// **预加载资源**
const preloadAssets = async () => {
  return new Promise((resolve) => {
    setTimeout(resolve, 2000); // 模拟2秒的加载时间
  });
};

// **模拟加载步骤**
const simulateLoadingStep = (text, percentage) => {
  return new Promise((resolve) => {
    setTimeout(() => {
      statusText.value = text;
      progress.value = percentage;
      resolve();
    }, 1500); // 模拟每个任务耗时 1.5 秒
  });
};
</script>

<template>
  <div v-if="isLoading" class="splash-container">
    <!-- 背景视频 -->
    <video autoplay loop muted playsinline class="background-video">
      <source src="./assets/login_background.mp4" type="video/mp4" />
      您的浏览器不支持 HTML5 视频
    </video>

<!-- 状态文本 -->
  <div class="status-text">
    <span class="loading-spinner"></span>
    {{ statusText }}
  </div>


    <!-- 加载进度条 -->
    <div class="progress-bar-container">
      <div class="progress-bar" :style="{ width: progress + '%' }"></div>
    </div>
  </div>

  <router-view v-else />
</template>

<style scoped>
/* 📌 背景视频 */
.background-video {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  z-index: -1;
}

/* 📌 启动画面容器 */
.splash-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-end;
  color: white;
  font-size: 18px;
  font-weight: bold;
  padding-bottom: 50px;
  z-index: 1000;
}

/* 📌 状态文本（左下角） */
.status-text {
  position: absolute;
  bottom: 80px;
  left: 50px;
  font-size: 18px;
  font-weight: bold;
  color: white;
  background: rgba(0, 0, 0, 0.5);
  padding: 8px 12px;
  border-radius: 5px;
}

/* 📌 进度条容器 */
.progress-bar-container {
  position: absolute;
  bottom: 60px;
  width: 80%;
  height: 8px;
  background: rgba(255, 255, 255, 0.3);
  border-radius: 5px;
  overflow: hidden;
}

/* 📌 进度条 */
.progress-bar {
  height: 100%;
  background: #42a5f5; /* 蓝色进度条 */
  transition: width 0.5s ease-in-out;
}

/* 📌 自定义蓝色旋转加载动画 */
.loading-spinner {
  display: inline-block;
  width: 20px;
  height: 20px;
  border: 3px solid rgba(66, 165, 245, 0.3); /* 浅蓝色半透明 */
  border-top: 3px solid #42a5f5; /* 亮蓝色 */
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-right: 10px;
  vertical-align: middle;
}

/* 旋转动画 */
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>
