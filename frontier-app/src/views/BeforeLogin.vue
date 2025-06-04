<template>
  <div class="login-container" @click="showLoginForm = true">
    <!-- 📌 1. 加载动画 -->
    <div v-if="isLoading" class="splash-container">
      <video autoplay loop muted playsinline class="background-video">
        <source src="../assets/title_4nd_2.mp4" type="video/mp4" />
        您的浏览器不支持 HTML5 视频
      </video>

      <div class="status-text">
        <span class="loading-spinner"></span>
        {{ statusText }}
      </div>

      <div class="progress-bar-container">
        <div class="progress-bar" :style="{ width: progress + '%' }"></div>
      </div>
    </div>

    <!-- 📌 2. 加载完成后，显示 "点击进入登录界面" -->
    <div v-if="showLoginPrompt && !showLoginForm" class="login-button-container">
      <div class="line top-line"></div>
      <span class="login-text">点击进入登录界面</span>
      <div class="line bottom-line"></div>
    </div>

    <!-- 📌 3. 登录窗口 -->
    <el-card v-if="showLoginForm" class="login-card">
      <div class="title">
        <img src="/vite.svg" alt="logo" class="logo" />
        <h2>个人健康信息管理系统</h2>
      </div>

      <el-form label-width="80px">
        <el-form-item>
          <el-input v-model="username" placeholder="请输入用户名" clearable />
        </el-form-item>

        <el-form-item>
          <el-input v-model="password" type="password" placeholder="请输入密码" clearable />
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="login" :loading="loading" class="login-btn">
            用户登录
          </el-button>
          <el-button type="primary" @click="goToRegister" class="login-btn">
            用户注册
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>





<script setup>
/**
 * 应用启动和登录前页面组件
 * @name BeforeLogin
 * @description 处理应用启动动画、初始化检查和登录界面展示
 */
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";
import {API_BASE_URL} from "../configs/network_config.js";

const router = useRouter();

const isLoading = ref(true); // 控制是否显示启动页面
const progress = ref(0); // 加载进度
const statusText = ref("正在初始化应用..."); // 状态文字
const showLoginButton = ref(false); // 控制是否显示“点击进入登录界面”

/* 初始化加载动画 */
onMounted(async () => {
  await initializeApp();
  isLoading.value = false; // 加载完成，隐藏动画
  router.push("/login");
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
    await axios.get(API_BASE_URL);
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

// **跳转到登录界面**
const goToLogin = () => {
  router.push("/login");
};

// 暴露给文档生成器
defineExpose({
  /**
   * 是否显示加载动画
   * @member {boolean}
   */
  isLoading,

  /**
   * 加载进度百分比
   * @member {number}
   */
  progress,

  /**
   * 状态显示文本
   * @member {string}
   */
  statusText,

  /**
   * 是否显示登录按钮提示
   * @member {boolean}
   */
  showLoginButton,

  /**
   * 初始化应用
   * @method
   * @async
   */
  initializeApp,

  /**
   * 检查服务器是否可用
   * @method
   * @async
   */
  checkServerStatus,

  /**
   * 预加载资源
   * @method
   * @async
   * @returns {Promise<void>}
   */
  preloadAssets,

  /**
   * 模拟加载步骤
   * @method
   * @async
   * @param {string} text - 要显示的状态文本
   * @param {number} percentage - 进度百分比
   * @returns {Promise<void>}
   */
  simulateLoadingStep,

  /**
   * 跳转到登录界面
   * @method
   */
  goToLogin,
});
</script>









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

/* 📌 “点击进入登录界面” */
.login-button-container {
  position: fixed;
  bottom: 100px; /* 距离底部100px */
  left: 50%;
  transform: translateX(-50%);
  text-align: center;
  color: white;
  font-size: 20px;
  font-weight: bold;
  cursor: pointer;
}

/* 📌 上下横线 */
.line {
  width: 60%;
  height: 1px;
  background-color: white;
  margin: 10px auto;
}

.top-line {
  margin-bottom: 10px;
}

.bottom-line {
  margin-top: 10px;
}

/* 📌 闪烁动画 */
.login-button-text {
  animation: blink 1.5s infinite alternate;
}

@keyframes blink {
  0% { opacity: 0.5; }
  100% { opacity: 1; }
}
</style>
