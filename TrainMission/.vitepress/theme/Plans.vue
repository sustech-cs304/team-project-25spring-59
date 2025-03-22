<template>
  <section class="plans">
    <h1>每周任务计划</h1>

    <!-- ✅ 引入你的 WeeklyPlan 子组件 -->
    <WeeklyPlan />
  </section>
</template>

<script setup lang="ts">
import WeeklyPlan from './components/Plans/Weekly_Plan.vue'
</script>

<style scoped>
.plans {
  max-width: 900px;
  margin: 100px auto 0;
  padding: 20px;
  font-size: 18px;
}
</style>
