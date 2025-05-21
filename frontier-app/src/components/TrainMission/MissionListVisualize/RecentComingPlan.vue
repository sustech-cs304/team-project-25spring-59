<template>
  <div class="in-progress-card animate__animated animate__fadeInUp animate__slow animate__delay-0.5s">
    <h2 class="title">⏰ 即将开始的计划</h2>

    <!-- 🔸输入框和按钮 -->
    <div class="input-section">
      <input type="number" v-model.number="queryMinutes" placeholder="请输入分钟数" />
      <button @click="fetchStartingSoonPlans">确定</button>
    </div>

    <!-- 🔹表格展示 -->
    <div v-if="plans.length === 0" class="empty">暂无记录</div>
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
        <tr v-for="plan in pagedPlans" :key="plan.id">
          <td>{{ plan.startDate }}</td>
          <td>{{ plan.endDate }}</td>
          <td>{{ plan.type }}</td>
          <td>{{ plan.duration }}</td>
          <td>{{ plan.calories }}</td>
          <td>{{ plan.heartRate }}</td>
        </tr>
      </tbody>
    </table>

    <div class="pagination" v-if="totalPages > 1">
      <button :disabled="currentPage === 1" @click="currentPage--">上一页</button>
      <span>第 {{ currentPage }} 页 / 共 {{ totalPages }} 页</span>
      <button :disabled="currentPage === totalPages" @click="currentPage++">下一页</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import axios from 'axios'

interface RecordItem {
  id: number
  type: string
  duration: string
  calories: string
  heartRate: string
  startDate: string
  endDate: string
}

const userId = ref<string | null>(localStorage.getItem('user_id'))
const queryMinutes = ref<number>(60) // 默认查询60分钟内的

const plans = ref<RecordItem[]>([])
const currentPage = ref(1)
const pageSize = 10

const pagedPlans = computed(() => {
  const start = (currentPage.value - 1) * pageSize
  return plans.value.slice(start, start + pageSize)
})

const totalPages = computed(() =>
  Math.ceil(plans.value.length / pageSize)
)

const fetchStartingSoonPlans = async () => {
  if (!userId.value || !queryMinutes.value || queryMinutes.value <= 0) return

  try {
    const res = await axios.post('http://localhost:8000/generate-user-records/starting-soon', {
      user_id: Number(userId.value),
      minutes: queryMinutes.value,
    })

    plans.value = res.data.records.map((record: any) => ({
      id: record.id,
      type: record.activity_type || '未知',
      duration: `${record.duration_minutes}分钟`,
      calories: `${record.calories ?? 0} kcal`,
      heartRate: `${record.average_heart_rate ?? '-'} bpm`,
      startDate: new Date(record.start_time).toLocaleString(),
      endDate: new Date(record.end_time).toLocaleString(),
    }))

    currentPage.value = 1
  } catch (e) {
    console.error('获取即将开始的计划失败', e)
  }
}
</script>

<style scoped>
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

.input-section {
  display: flex;
  justify-content: center;
  gap: 1rem;
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

.empty {
  color: #444;
  padding: 1rem 0;
}

.pagination {
  margin-top: 1.5rem;
  text-align: center;
}

.pagination button {
  margin: 0 8px;
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
