<template>
  <div class="login-container">
    <!-- 背景视频 -->
    <video autoplay loop muted playsinline class="background-video">
      <source src="../assets/login_background.mp4" type="video/mp4" />
      您的浏览器不支持 HTML5 视频
    </video>

    <!-- 鼠标特效 -->
    <MouseTrail />

    <!-- 登录卡片 -->
    <el-card class="login-card">
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
import { ref } from "vue";
import { useRouter } from "vue-router";
import { ElMessage } from "element-plus";
import axios from "axios";
import MouseTrail from "../components/MouseTrail.vue";

const router = useRouter();
const username = ref("");
const password = ref("");
const loading = ref(false);

const login = async () => {
  if (!username.value || !password.value) {
    ElMessage.error("请输入用户名和密码");
    return;
  }

  loading.value = true;
  try {
    const response = await axios.post("http://127.0.0.1:8000/login", {
      username: username.value,
      password: password.value,
    });

    ElMessage.success(response.data.message);
    sessionStorage.setItem("token", response.data.token);
    router.push("/carousel"); // 登录成功后跳转到 Carousel 页面
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || "登录失败");
  } finally {
    loading.value = false;
  }
};

// 点击按钮跳转到 注册用户的界面/register
const goToRegister = () => {
  router.push("/register");
};
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

/* 📌 登录界面布局 */
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  position: relative;
}

/* 📌 登录卡片美化 */
.login-card {
  width: 400px;
  padding: 30px;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.2); /* 透明度增强 */
  backdrop-filter: blur(10px); /* 毛玻璃效果 */
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
  transition: transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out;
  z-index: 10;
}

.login-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.4);
}
</style>
