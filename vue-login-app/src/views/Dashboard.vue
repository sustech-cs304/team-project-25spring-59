<script setup>
import { useRouter } from 'vue-router';

const router = useRouter();

const logout = () => {
  localStorage.removeItem('token'); // 清除 Token
  router.push('/login'); // 退出登录
};
</script>

<template>
  <div class="dashboard-container">
    <h2>欢迎来到健康管理系统</h2>
    <el-button type="danger" @click="logout">退出登录</el-button>
  </div>
</template>

<style scoped>
.dashboard-container {
  text-align: center;
  margin-top: 100px;
}
</style>
