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
import {API_BASE_URL} from "../configs/network_config.js"

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
    const response = await axios.post(`${API_BASE_URL}/register`, {
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

defineExpose({
  /**
   * 用户名输入框的值
   * @member {import('vue').Ref<string>}
   */
  username,

  /**
   * 邮箱输入框的值
   * @member {import('vue').Ref<string>}
   */
  email,

  /**
   * 密码输入框的值
   * @member {import('vue').Ref<string>}
   */
  password,

  /**
   * 确认密码输入框的值
   * @member {import('vue').Ref<string>}
   */
  confirmPassword,

  /**
   * 注册请求的加载状态
   * @member {import('vue').Ref<boolean>}
   */
  loading,

  /**
   * 提交注册请求的方法
   * @function
   * @async
   * @description 验证表单后提交注册请求，成功则跳转登录页
   * @throws {Error} 注册失败时抛出错误
   */
  register,

  /**
   * 跳转到登录页面的方法
   * @function
   * @description 导航到/login路由
   */
  goToLogin
});
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
