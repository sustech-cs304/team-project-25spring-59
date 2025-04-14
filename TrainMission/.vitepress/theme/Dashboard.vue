<template>
  <section class="dashboard">
    <h1>📈 数据总览</h1>

    <div class="chart-wrapper">
      <CalorieChart />
    </div>

    <!-- 添加时间柱状图组件 -->
    <div class="chart-wrapper">
      <TimeBar />
    </div>
  </section>
</template>

<script setup lang="ts">
import CalorieChart from './components/Charts/CalorieChart.vue' // 导入卡路里图表组件
import TimeBar from './components/Charts/TimeBar.vue'  // 导入时间柱状图组件
</script>

<style scoped>
.dashboard {
  max-width: 900px;
  margin: 100px auto 0;
  padding: 20px;
  font-size: 18px;
  text-align: center;
}

.chart-wrapper {
  margin-top: 40px;
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
