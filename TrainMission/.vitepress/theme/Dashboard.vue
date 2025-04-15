<template>
  <section class="dashboard">
    <h1>📈 数据总览</h1>

    <!-- 显示训练总结数据 -->
    <div v-if="summaryData" class="summary-data">
      <p>总训练时长: {{ summaryData.total_minutes }} 分钟</p>
      <p>估算卡路里消耗: {{ summaryData.estimated_calories }} 千卡</p>
      <p>实际卡路里消耗: {{ summaryData.actual_calories }} 千卡</p>
      <p>平均心率: {{ summaryData.average_heart_rate }} bpm</p>
      <p>最大心率: {{ summaryData.max_heart_rate }} bpm</p>
    </div>

    <!-- 卡路里图表组件 -->
    <div class="chart-wrapper">
      <CalorieChart />
    </div>

    <!-- 时间柱状图组件 -->
    <div class="chart-wrapper">
      <TimeBar />
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'
import CalorieChart from './components/Charts/CalorieChart.vue' // 导入卡路里图表组件
import TimeBar from './components/Charts/TimeBar.vue'  // 导入时间柱状图组件

const userId = localStorage.getItem('user_id') // 假设用户ID存储在localStorage中

// 创建一个响应式变量来存储接口返回的训练总结数据
const summaryData = ref<any>(null)

// 请求训练总结数据
const fetchSummaryData = async () => {
  if (!userId) {
    console.error("User ID not found")
    return
  }

  try {
    const response = await axios.post('http://localhost:8000/stats/summary', {
      user_id: parseInt(userId)
    })
    summaryData.value = response.data
  } catch (error) {
    console.error("Failed to fetch summary data:", error)
  }
}

// 在组件挂载后获取训练总结数据
onMounted(() => {
  fetchSummaryData()
})
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

.summary-data {
  margin-bottom: 20px;
  padding: 10px;
  background-color: #f0f0f0;
  border-radius: 5px;
}

.summary-data p {
  font-size: 16px;
  margin: 5px 0;
}
</style>
