<template>
  <div class="login-container">
    <MouseTrail />

    <el-card class="login-card">
      <div class="title">
        <img src="/vite.svg" alt="logo" class="logo" />
        <h2>健康管理系统</h2>
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
            登录
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
import MouseTrail from "../components/MouseTrail.vue";

const router = useRouter();
const username = ref("");
const password = ref("");
const loading = ref(false);

const login = () => {
  loading.value = true;
  setTimeout(() => {
    loading.value = false;
    ElMessage.success("登录成功！");
    router.push("/carousel");
  }, 1000);
};
</script>

<style scoped>
/* 📌 背景渐变 */
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: linear-gradient(to right, #42a5f5, #478ed1, #42b983);
  position: relative; /* 确保粒子背景不会遮挡内容 */
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
}

.login-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.4);
}
</style>
