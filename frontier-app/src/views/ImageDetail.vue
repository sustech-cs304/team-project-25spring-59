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


defineExpose({
  /**
   * 当前图片ID（来自路由参数）
   * @member {import('vue').ComputedRef<string>}
   * @description 从路由参数中获取的当前图片ID（响应式计算属性）
   */
  id,

  /**
   * 根据ID生成的图片URL
   * @member {import('vue').ComputedRef<string>}
   * @description 基于ID自动生成的图片资源路径（格式：/0{id}.jpg）
   */
  imageUrl,

  /**
   * 返回轮播图页面
   * @function
   * @description 导航回轮播图列表页面
   */
  goBack,

  /**
   * 当前路由对象（只读）
   * @member {import('vue-router').RouteLocationNormalizedLoaded}
   * @description Vue Router的当前路由对象
   * @warning 不建议直接修改
   */
  route,

  /**
   * 路由实例（只读）
   * @member {import('vue-router').Router}
   * @description Vue Router实例
   * @warning 谨慎操作路由跳转
   */
  router
});
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
