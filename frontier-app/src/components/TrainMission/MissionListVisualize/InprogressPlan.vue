<template>
  <div class="in-progress-card animate__animated animate__fadeInUp animate__slow animate__delay-0.5s">
    <h2 class="title">🟡 正在进行的计划</h2>

    <div v-if="inProgressPlans.length === 0" class="empty">暂无记录</div>
    <table v-else class="plan-table">
      <thead>
        <tr>
          <th>开始时间</th>
          <th>结束时间</th>
          <th>运动类型</th>
          <th>运动时长</th>
          <th>消耗卡路里</th>
          <th>平均心率</th>
          <th>完成进度</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="plan in pagedInProgressPlans" :key="'progress-' + plan.id">
          <td>{{ plan.startDate }}</td>
          <td>{{ plan.endDate }}</td>
          <td>{{ plan.type }}</td>
          <td>{{ plan.duration }}</td>
          <td>{{ plan.calories }}</td>
          <td>{{ plan.heartRate }}</td>
          <td>
            <div class="progress-wrapper">
              <div class="progress-container">
                <div
                  class="progress-bar"
                  :style="{ width: plan.progress + '%', backgroundColor: getProgressColor(plan.progress) }"
                />
              </div>
              <span class="progress-text">{{ plan.progress }}%</span>
            </div>
          </td>
        </tr>
      </tbody>
    </table>

    <div class="pagination">
      <button :disabled="inProgressCurrentPage === 1" @click="inProgressCurrentPage--">上一页</button>
      <span>第 {{ inProgressCurrentPage }} 页 / 共 {{ inProgressTotalPages }} 页</span>
      <button :disabled="inProgressCurrentPage === inProgressTotalPages" @click="inProgressCurrentPage++">下一页</button>
    </div>
  </div>
</template>







<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed } from 'vue'
import axios from 'axios'

// 类型定义
interface RecordItem {
  id: number
  type: string
  duration: string
  calories: string
  heartRate: string
  startDate: string
  endDate: string
  completed: boolean
  progress: number
}

// 用户 ID
const userId = ref<string | null>(null)

// 正在进行中的计划
const inProgressPlans = ref<RecordItem[]>([])

const inProgressCurrentPage = ref(1)
const inProgressPageSize = 10
const pagedInProgressPlans = computed(() => {
  const start = (inProgressCurrentPage.value - 1) * inProgressPageSize
  return inProgressPlans.value.slice(start, start + inProgressPageSize)
})
const inProgressTotalPages = computed(() => Math.ceil(inProgressPlans.value.length / inProgressPageSize))

// 获取计划数据
const fetchInProgressPlans = async () => {
  if (!userId.value) return
  try {
    const res = await axios.post('http://localhost:8000/generate-user-records/in-progress', {
      user_id: Number(userId.value)
    })
    inProgressPlans.value = res.data.records.map(formatRecordWithProgress)
  } catch (e) {
    console.error('获取进行中计划失败', e)
  }
}

// 格式化数据并计算进度
const formatRecordWithProgress = (record: any): RecordItem => {
  const now = Date.now()
  const start = new Date(record.start_time).getTime()
  const end = new Date(record.end_time).getTime()
  const durationInMinutes = record.duration_minutes ?? 0
  const progress = now < start
    ? 0
    : now > end
    ? 100
    : Math.floor(((now - start) / (end - start)) * 100)

  return {
    id: record.id,
    type: record.activity_type || '未知',
    duration: `${durationInMinutes}分钟`,
    calories: `${record.calories ?? 0} kcal`,
    heartRate: `${record.average_heart_rate ?? '-'} bpm`,
    startDate: new Date(record.start_time).toLocaleString(),
    endDate: new Date(record.end_time).toLocaleString(),
    completed: record.is_completed,
    progress
  }
}

let refreshInterval: number | undefined

onMounted(() => {
  userId.value = localStorage.getItem('user_id')
  fetchInProgressPlans()

  //每分钟刷新一次
  refreshInterval = window.setInterval(() => {
    fetchInProgressPlans()
  }, 1000)
})

onUnmounted(() => {
  if (refreshInterval) clearInterval(refreshInterval)
})


//设置颜色
const getProgressColor = (progress: number): string => {
  if (progress < 30) return '#f44336' // 红色
  if (progress < 70) return '#ff9800' // 橙色
  return '#4caf50' // 绿色
}

</script>




<style scoped>
.progress-container {
  position: relative;
  background-color: #e0e0e0;
  border-radius: 8px;
  height: 16px;
  width: 100px;
  margin: 0 auto;
}

.progress-bar {
  background-color: #ff9800;
  height: 100%;
  border-radius: 8px;
  transition: width 0.3s ease-in-out;
}

.progress-label {
  position: absolute;
  top: -22px;
  left: 50%;
  transform: translateX(-50%);
  font-size: 0.8rem;
  color: #333;
}



.in-progress-card {
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  background-color: rgba(255, 255, 255, 0.15);
  border-radius: 12px;
  padding: 1.5rem;
  margin: 1rem auto;
  max-width: 900px;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.1);
  color: #000;
  text-align: center;
  overflow-x: auto;
}

.title {
  font-size: 1.6rem;
  font-weight: bold;
  margin-bottom: 1rem;
}


.in-progress-card {
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  background-color: rgba(255, 255, 255, 0.15);
  border-radius: 12px;
  padding: 1.5rem;
  margin: 1rem auto;
  max-width: 900px;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.1);
  color: #000;
  text-align: center;
  overflow-x: auto;
}

.title {
  font-size: 1.6rem;
  font-weight: bold;
  margin-bottom: 1.5rem;
}

.plan-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.95rem;
  margin-top: 1rem;
}

.plan-table th,
.plan-table td {
  border: 1px solid rgba(0, 0, 0, 0.1);
  padding: 0.75rem;
  text-align: center;
  background-color: rgba(255, 255, 255, 0.85);
}

.plan-table th {
  background-color: rgba(0, 0, 0, 0.05);
  font-weight: 600;
}

.plan-table tr:hover {
  background-color: rgba(0, 0, 0, 0.05);
}

.progress-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.3rem;
}

.progress-container {
  width: 100px;
  height: 12px;
  background-color: #e0e0e0;
  border-radius: 6px;
  overflow: hidden;
}

.progress-bar {
  height: 100%;
  transition: width 0.3s ease;
}

.progress-text {
  font-size: 0.8rem;
  font-weight: 500;
  color: #333;
}

.empty {
  color: #444;
  text-align: center;
  padding: 1rem 0;
}

.pagination {
  display: block;
  width: 100%;
  margin-top: 1.5rem;
  text-align: center;
  user-select: none;
}

.pagination button {
  display: inline-block;
  margin: 0 6px;
  padding: 6px 12px;
  border: none;
  border-radius: 4px;
  background-color: #1976d2;
  color: #fff;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.pagination button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.pagination span {
  display: inline-block;
  margin: 0 10px;
  font-weight: 600;
  vertical-align: middle;
}

</style>