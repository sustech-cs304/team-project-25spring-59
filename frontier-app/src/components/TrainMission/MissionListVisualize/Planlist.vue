<template>
  <div class="plan-list animate__animated animate__fadeInUp animate__slow animate__delay-0.5s">
    <h2 class="title">运动计划列表</h2>
    <p class="userid-global">用户ID：{{ userId || '未知' }}</p>

    <div v-if="plans.length === 0" class="empty">暂无计划</div>
    <table v-else class="plan-table">
      <thead>
        <tr>
          <th>开始时间</th>
          <th>结束时间</th>
          <th>运动类型</th>
          <th>运动时长</th>
          <th>消耗卡路里</th>
          <th>平均心率</th>
          <th>是否完成</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="plan in plans" :key="plan.id">
          <td>{{ plan.startDate }}</td>
          <td>{{ plan.endDate }}</td>
          <td>{{ plan.type }}</td>
          <td>{{ plan.duration }}</td>
          <td>{{ plan.calories }}</td>
          <td>{{ plan.heartRate }}</td>
          <td>{{ plan.completed }}</td>
        </tr>
      </tbody>
    </table>


    <!-- ✅ 加载按钮 -->
    <div class="btn-group">
      <button class="btn-add" @click="handleAdd">Add Record</button>
      <button class="btn-delete" @click="handleDelete">Delete Record</button>
    </div>

    <!-- ✅ 加载动画 -->
    <Loading v-model:active="isLoading" :can-cancel="false" :is-full-page="false" />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import Loading from 'vue3-loading-overlay'
import 'vue3-loading-overlay/dist/vue3-loading-overlay.css'

const plans = ref([
  {
    id: 1,
    type: '有氧训练',
    duration: '45分钟',
    calories: '350 kcal',
    heartRate: '125 bpm',
    startDate: '2025-04-01',
    endDate: '2025-04-07',
    completed : true,
  },
  {
    id: 2,
    type: '力量训练',
    duration: '60分钟',
    calories: '500 kcal',
    heartRate: '140 bpm',
    startDate: '2025-04-08',
    endDate: '2025-04-14',
    completed : false,
  }
])

const userId = ref<string | null>(null)
const isLoading = ref(false)

onMounted(() => {
  userId.value = localStorage.getItem('user_id')
})

const handleAdd = () => {
  isLoading.value = true
  setTimeout(() => {
    isLoading.value = false
    // alert('添加成功')
  }, 1500)
}

const handleDelete = () => {
  isLoading.value = true
  setTimeout(() => {
    isLoading.value = false
    // alert('删除成功')
  }, 1500)
}
</script>

<style scoped>
.plan-list {
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
  font-size: 1.8rem;
  font-weight: bold;
  margin-bottom: 0.3rem;
}

.userid-global {
  font-size: 0.95rem;
  color: #333;
  margin-bottom: 1.5rem;
}

.plan-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.95rem;
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
  text-align: center;
  padding: 1rem 0;
}

.btn-group {
  display: flex;
  justify-content: center;
  gap: 1.5rem;
  margin-top: 2rem;
}

.btn-add,
.btn-delete {
  padding: 0.6rem 1.2rem;
  font-size: 1rem;
  font-weight: bold;
  border: none;
  border-radius: 8px;
  color: #fff;
  cursor: pointer;
  transition: 0.3s ease;
}

.btn-add {
  background-color: #4caf50;
}

.btn-delete {
  background-color: #e53935;
}
</style>
