<template>
  <div class="detail-container">
    <h2>图片详情</h2>
    <img :src="imageUrl" alt="详情图片" />
    <p>这是一张编号为 {{ id }} 的图片。</p>
    <el-button type="primary" @click="goBack">返回</el-button>
  </div>
</template>

<script setup>
import { useRoute, useRouter } from 'vue-router';
import { computed } from 'vue';

const route = useRoute();
const router = useRouter();
const id = computed(() => route.params.id); // 获取动态路由参数
const imageUrl = computed(() => `/0${id.value}.jpg`); // 根据 ID 显示不同图片

const goBack = () => {
  router.push('/carousel'); // 返回轮播图页面
};
</script>

<style scoped>
.detail-container {
  text-align: center;
  margin-top: 50px;
}

img {
  width: 300px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  margin-bottom: 20px;
}
</style>
