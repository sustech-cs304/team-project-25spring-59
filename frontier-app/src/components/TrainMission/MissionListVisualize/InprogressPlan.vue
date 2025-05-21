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

    <div class="pagination" v-if="inProgressTotalPages > 1">
      <button :disabled="inProgressCurrentPage === 1" @click="inProgressCurrentPage--">上一页</button>
      <span>第 {{ inProgressCurrentPage }} 页 / 共 {{ inProgressTotalPages }} 页</span>
      <button :disabled="inProgressCurrentPage === inProgressTotalPages" @click="inProgressCurrentPage++">下一页</button>
    </div>

    <!-- 分隔线 -->
    <hr style="margin: 2rem 0;" />

    <h2 class="title">⏰ 即将开始的计划</h2>
    <div class="input-section">
      <input type="number" v-model.number="queryMinutes" placeholder="请输入分钟数" />
      <button @click="fetchStartingSoonPlans">确定</button>
    </div>

    <div v-if="startingPlans.length === 0" class="empty">暂无记录</div>
    <table v-else class="plan-table">
      <thead>
        <tr>
          <th>开始时间</th>
          <th>结束时间</th>
          <th>运动类型</th>
          <th>运动时长</th>
          <th>消耗卡路里</th>
          <th>平均心率</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="plan in pagedStartingPlans" :key="'soon-' + plan.id">
          <td>{{ plan.startDate }}</td>
          <td>{{ plan.endDate }}</td>
          <td>{{ plan.type }}</td>
          <td>{{ plan.duration }}</td>
          <td>{{ plan.calories }}</td>
          <td>{{ plan.heartRate }}</td>
        </tr>
      </tbody>
    </table>

    <div class="pagination" v-if="startingTotalPages > 1">
      <button :disabled="startingCurrentPage === 1" @click="startingCurrentPage--">上一页</button>
      <span>第 {{ startingCurrentPage }} 页 / 共 {{ startingTotalPages }} 页</span>
      <button :disabled="startingCurrentPage === startingTotalPages" @click="startingCurrentPage++">下一页</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed } from 'vue'
import axios from 'axios'

interface RecordItem {
  id: number
  type: string
  duration: string
  calories: string
  heartRate: string
  startDate: string
  endDate: string
  completed?: boolean
  progress?: number
}

const userId = ref<string | null>(localStorage.getItem('user_id'))

// ✅ 进行中的计划数据
const inProgressPlans = ref<RecordItem[]>([])
const inProgressCurrentPage = ref(1)
const inProgressPageSize = 10
const pagedInProgressPlans = computed(() => {
  const start = (inProgressCurrentPage.value - 1) * inProgressPageSize
  return inProgressPlans.value.slice(start, start + inProgressPageSize)
})
const inProgressTotalPages = computed(() => Math.ceil(inProgressPlans.value.length / inProgressPageSize))

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
  fetchInProgressPlans()
  refreshInterval = window.setInterval(() => {
    fetchInProgressPlans()
  }, 10000)
})
onUnmounted(() => {
  if (refreshInterval) clearInterval(refreshInterval)
})

const getProgressColor = (progress: number): string => {
  if (progress < 30) return '#f44336'
  if (progress < 70) return '#ff9800'
  return '#4caf50'
}

// ✅ 即将开始的计划数据
const queryMinutes = ref<number>(60)
const startingPlans = ref<RecordItem[]>([])
const startingCurrentPage = ref(1)
const startingPageSize = 10
const pagedStartingPlans = computed(() => {
  const start = (startingCurrentPage.value - 1) * startingPageSize
  return startingPlans.value.slice(start, start + startingPageSize)
})
const startingTotalPages = computed(() => Math.ceil(startingPlans.value.length / startingPageSize))

const fetchStartingSoonPlans = async () => {
  if (!userId.value || !queryMinutes.value || queryMinutes.value <= 0) return
  try {
    const res = await axios.post('http://localhost:8000/generate-user-records/starting-soon', {
      user_id: Number(userId.value),
      minutes: queryMinutes.value
    })
    startingPlans.value = res.data.records.map((record: any) => ({
      id: record.id,
      type: record.activity_type || '未知',
      duration: `${record.duration_minutes}分钟`,
      calories: `${record.calories ?? 0} kcal`,
      heartRate: `${record.average_heart_rate ?? '-'} bpm`,
      startDate: new Date(record.start_time).toLocaleString(),
      endDate: new Date(record.end_time).toLocaleString()
    }))
    startingCurrentPage.value = 1
  } catch (e) {
    console.error('获取即将开始的计划失败', e)
  }
}
</script>

<style scoped>
/* 原样保留你的样式代码，包括表格、进度条、卡片、分页等 */

.in-progress-card {
  backdrop-filter: blur(10px);
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

.empty {
  color: #444;
  padding: 1rem 0;
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

.input-section {
  display: flex;
  justify-content: center;
  gap: 1rem;
  margin-top: 1rem;
  margin-bottom: 1rem;
}

.input-section input {
  padding: 0.6rem;
  border-radius: 6px;
  border: 1px solid #ccc;
  font-size: 1rem;
  width: 160px;
}

.input-section button {
  padding: 0.6rem 1rem;
  background-color: #1976d2;
  color: #fff;
  border: none;
  border-radius: 6px;
  font-weight: bold;
  cursor: pointer;
}

.pagination {
  margin-top: 1.5rem;
  text-align: center;
  user-select: none;
}

.pagination button {
  margin: 0 6px;
  padding: 6px 12px;
  background-color: #1976d2;
  color: #fff;
  border: none;
  border-radius: 4px;
  font-weight: 600;
  cursor: pointer;
}

.pagination button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}
</style>
