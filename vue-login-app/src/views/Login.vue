<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import { ElMessage } from 'element-plus';

const router = useRouter();
const username = ref('');
const password = ref('');
const loading = ref(false);
const showPassword = ref(false); // 控制密码显示

const login = async () => {
  if (!username.value || !password.value) {
    ElMessage.error('请输入用户名和密码');
    return;
  }

  loading.value = true;

  try {
    // 这里是本地验证（模拟后端验证）
    if (username.value === '1' && password.value === '1') {
      ElMessage.success('登录成功！');
      localStorage.setItem('token', 'mock-token'); // 存储 Token
      router.push('/carousel'); // ✅ 登录成功后跳转到 Carousel 页面
    } else {
      ElMessage.error('用户名或密码错误');
    }
  } catch (error) {
    ElMessage.error(error.response?.data?.message || '登录失败');
  } finally {
    loading.value = false;
  }
};

</script>

<template>
  <div class="login-container">
    <el-card class="login-card">
      <div class="title">
        <img src="/vite.svg" alt="logo" class="logo" />
        <h2>健康管理系统</h2>
      </div>

      <el-form label-width="80px">
        <!-- 用户名输入框 -->
        <el-form-item>
          <el-input
            v-model="username"
            placeholder="请输入用户名"
            prefix-icon="el-icon-user"
            clearable
          />
        </el-form-item>

        <!-- 密码输入框 -->
        <el-form-item>
          <el-input
            v-model="password"
            :type="showPassword ? 'text' : 'password'"
            placeholder="请输入密码"
            prefix-icon="el-icon-lock"
            show-password
          />
        </el-form-item>

        <!-- 登录按钮 -->
        <el-form-item>
          <el-button type="primary" @click="login" :loading="loading" class="login-btn">
            登录
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<style scoped>
/* 背景渐变 */
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: linear-gradient(to right, #42a5f5, #478ed1, #42b983);
}

/* 登录卡片 */
.login-card {
  width: 400px;
  padding: 30px;
  border-radius: 12px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
  background: white;
}

/* 标题 */
.title {
  text-align: center;
  margin-bottom: 20px;
}

/* Logo */
.logo {
  width: 50px;
  height: 50px;
}

/* 输入框美化 */
.el-input {
  height: 40px;
}

/* 登录按钮美化 */
.login-btn {
  width: 100%;
  height: 45px;
  font-size: 16px;
  font-weight: bold;
  background: linear-gradient(to right, #42a5f5, #42b983);
  border: none;
  transition: 0.3s;
}

.login-btn:hover {
  background: linear-gradient(to right, #42b983, #42a5f5);
}
</style>
