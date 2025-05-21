<template>
  <div class="register-container">
    <MouseTrail />

    <el-card class="register-card">
      <div class="title">
        <img src="/vite.svg" alt="logo" class="logo" />
        <h2>用户注册</h2>
      </div>

      <el-form label-width="80px">
        <el-form-item>
          <el-input v-model="username" placeholder="请输入用户名" clearable />
        </el-form-item>

        <el-form-item>
          <el-input v-model="email" placeholder="请输入邮箱" clearable />
        </el-form-item>

        <el-form-item>
          <el-input v-model="password" type="password" placeholder="请输入密码" clearable />
        </el-form-item>

        <el-form-item>
          <el-input v-model="confirmPassword" type="password" placeholder="请确认密码" clearable />
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="register" :loading="loading" class="register-btn">
            注册
          </el-button>
          <el-button @click="goToLogin" class="register-btn">
            返回登录
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
import MouseTrail from "../components/MouseTrail.vue"; // 引入 axios 用于发送 HTTP 请求

const router = useRouter();
const username = ref("");
const email = ref("");
const password = ref("");
const confirmPassword = ref("");
const loading = ref(false);

const register = async () => {
  if (!username.value || !email.value || !password.value || !confirmPassword.value) {
    ElMessage.error("请填写所有字段");
    return;
  }
  if (password.value !== confirmPassword.value) {
    ElMessage.error("两次输入的密码不匹配");
    return;
  }

  loading.value = true;

  try {
    console.log("发送注册请求", username.value, email.value, password.value);
    const response = await axios.post("http://10.12.184.92:8000/register", {
      username: username.value,
      email: email.value,
      password: password.value,
    });

    ElMessage.success(response.data.message);
    router.push("/login"); // 注册成功后跳转到登录页面
  } catch (error) {
    console.error("注册失败", error.response?.data);
    ElMessage.error(error.response?.data?.detail || "注册失败");
  } finally {
    loading.value = false;
  }
};

const goToLogin = () => {
  router.push("/login");
};
</script>

<style scoped>
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: linear-gradient(to right, #42a5f5, #478ed1, #42b983);
  position: relative;
}

.register-card {
  width: 400px;
  padding: 30px;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
  transition: transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out;
}

.register-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.4);
}
</style>
