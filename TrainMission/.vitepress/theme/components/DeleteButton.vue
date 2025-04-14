<template>
  <button @click="handleDelete" class="delete-button">删除记录</button>
</template>

<script setup lang="ts">
import { useRoute } from 'vitepress';

const route = useRoute();  // 获取当前路由信息

const handleDelete = async () => {
  try {
    // 获取当前页面的路径并提取文件名
    const path = route.path;
    const filename = path.substring(path.lastIndexOf("/") + 1, path.lastIndexOf(".html")) + ".md";

    // 向后端发送删除请求
    const response = await fetch('http://localhost:8000/delete-record', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ filename })
    });

    const result = await response.json();

    if (response.ok) {
      alert('文件删除成功！');
    } else {
      alert('删除失败: ' + result.detail);
    }
  } catch (error) {
    alert('请求失败，请检查网络连接。');
  }
};
</script>

<style scoped>
.delete-button {
  background-color: #dc3545;
  color: white;
  border: none;
  padding: 10px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 14px;
}

.delete-button:hover {
  background: #c82333;
}
</style>
