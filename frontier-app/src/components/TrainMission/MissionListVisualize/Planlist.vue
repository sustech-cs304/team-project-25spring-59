<template>
  <div class="plan-list animate__animated animate__fadeInUp animate__slow animate__delay-0.5s">
    <h2 class="title">运动计划列表</h2>
    <p class="userid-global">用户ID：{{ userId || '未知' }}</p>

    <!-- ✅ 已完成记录 -->
    <div class="table-section">
      <h3 class="section-title">✅ 已完成记录</h3>
      <div v-if="completedPlans.length === 0" class="empty">暂无记录</div>
      <table v-else class="plan-table">
        <thead>
          <tr>
            <th><input type="checkbox" @change="toggleAll(completedPlans)" :checked="isAllChecked(completedPlans)" /></th>
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
          <tr v-for="plan in pagedCompletedPlans" :key="'completed-' + plan.id">
            <td><input type="checkbox" v-model="selectedIds" :value="plan.id" /></td>
            <td>{{ plan.startDate }}</td>
            <td>{{ plan.endDate }}</td>
            <td>{{ plan.type }}</td>
            <td>{{ plan.duration }}</td>
            <td>{{ plan.calories }}</td>
            <td>{{ plan.heartRate }}</td>
            <td>{{ plan.completed ? '是' : '否' }}</td>
          </tr>
        </tbody>
        <div class="pagination">
          <button :disabled="completedCurrentPage === 1" @click="completedCurrentPage--">上一页</button>
          <span>第 {{ completedCurrentPage }} 页 / 共 {{ completedTotalPages }} 页</span>
          <button :disabled="completedCurrentPage === completedTotalPages" @click="completedCurrentPage++">下一页</button>
        </div>

      </table>
    </div>

    <!-- ⚠️ 错过的计划 -->
    <div class="table-section">
      <h3 class="section-title">⚠️ 错过的计划</h3>
      <div v-if="missedPlans.length === 0" class="empty">暂无记录</div>
      <table v-else class="plan-table">
        <thead>
          <tr>
            <th><input type="checkbox" @change="toggleAll(missedPlans)" :checked="isAllChecked(missedPlans)" /></th>
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
          <tr v-for="plan in pagedMissedPlans" :key="'missed-' + plan.id">
            <td><input type="checkbox" v-model="selectedIds" :value="plan.id" /></td>
            <td>{{ plan.startDate }}</td>
            <td>{{ plan.endDate }}</td>
            <td>{{ plan.type }}</td>
            <td>{{ plan.duration }}</td>
            <td>{{ plan.calories }}</td>
            <td>{{ plan.heartRate }}</td>
            <td>{{ plan.completed ? '是' : '否' }}</td>
          </tr>
        </tbody>
        <div class="pagination">
          <button :disabled="missedCurrentPage === 1" @click="missedCurrentPage--">上一页</button>
          <span>第 {{ missedCurrentPage }} 页 / 共 {{ missedTotalPages }} 页</span>
          <button :disabled="missedCurrentPage === missedTotalPages" @click="missedCurrentPage++">下一页</button>
        </div>
      </table>
    </div>

    <!-- ⏳ 未来的计划 -->
    <div class="table-section">
      <h3 class="section-title">⏳ 未来的计划</h3>
      <div v-if="upcomingPlans.length === 0" class="empty">暂无记录</div>
      <table v-else class="plan-table">
        <thead>
          <tr>
            <th><input type="checkbox" @change="toggleAll(upcomingPlans)" :checked="isAllChecked(upcomingPlans)" /></th>
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
          <tr v-for="plan in pagedUpcomingPlans" :key="'upcoming-' + plan.id">
            <td><input type="checkbox" v-model="selectedIds" :value="plan.id" /></td>
            <td>{{ plan.startDate }}</td>
            <td>{{ plan.endDate }}</td>
            <td>{{ plan.type }}</td>
            <td>{{ plan.duration }}</td>
            <td>{{ plan.calories }}</td>
            <td>{{ plan.heartRate }}</td>
            <td>{{ plan.completed ? '是' : '否' }}</td>
          </tr>
        </tbody>
        <div class="pagination">
          <button :disabled="upcomingCurrentPage === 1" @click="upcomingCurrentPage--">上一页</button>
          <span>第 {{ upcomingCurrentPage }} 页 / 共 {{ upcomingTotalPages }} 页</span>
          <button :disabled="upcomingCurrentPage === upcomingTotalPages" @click="upcomingCurrentPage++">下一页</button>
        </div>
      </table>
    </div>



    <!-- ✅ 加载按钮 -->
    <div class="btn-group">
      <button class="btn-add" @click="handleAdd">Add Record</button>
      <button class="btn-delete" @click="handleDelete">Delete Record</button>
      <button class="btn-toggle" @click="handleToggleType">Change Record</button>

    </div>

    <!-- ✅ 加载动画 -->
    <Loading v-model:active="isLoading" :can-cancel="false" :is-full-page="false" />
  </div>


    <!-- 弹窗组件：添加训练记录 -->
  <div v-if="showAddModal" class="modal-overlay">
    <div class="modal-content">
      <h3>新建训练记录</h3>
      <form @submit.prevent="submitNewPlan">
        <label>
          开始时间：
          <input type="datetime-local" v-model="newPlan.start_time" required />
        </label>

        <label>
          结束时间：
          <input type="datetime-local" v-model="newPlan.end_time" required />
        </label>

        <!-- 🕒 显示运动时间提示 -->
        <p v-if="computedDuration" style="margin-top: -8px; font-size: 0.95rem; color: #555;">
          🕒 预计运动时长：{{ computedDuration }}
        </p>

        <label>
          运动类型：
          <input type="text" v-model="newPlan.activity_type" placeholder="如 跑步、游泳等" required />
        </label>

<!--        <label>-->
<!--          运动时长（分钟）：-->
<!--          <input type="number" v-model="newPlan.duration_minutes" required />-->
<!--        </label>-->

        <label>
          消耗卡路里（kcal）：
          <input type="number" v-model="newPlan.calories" />
        </label>

        <label>
          平均心率（bpm）：
          <input type="number" v-model="newPlan.average_heart_rate" />
        </label>

        <label>
          是否完成：
          <select v-model="newPlan.is_completed">
            <option :value="true">完成</option>
            <option :value="false">未完成</option>
          </select>
        </label>

        <div class="modal-buttons">
          <button type="submit" class="btn-add">提交</button>
          <button type="button" class="btn-delete" @click="showAddModal = false">取消</button>
        </div>
      </form>
    </div>
  </div>

</template>

<script setup lang="ts">
import { ref, onMounted} from 'vue'
import axios from 'axios'
import Loading from 'vue3-loading-overlay'
import 'vue3-loading-overlay/dist/vue3-loading-overlay.css'
import {computed} from "vue";

// 定义响应数据结构
interface RecordItem {
  id: number
  type: string
  duration: string
  calories: string
  heartRate: string
  startDate: string
  endDate: string
  completed: boolean
}

const plans = ref<RecordItem[]>([]) // 最终要渲染的训练计划数据
const userId = ref<string | null>(null)
const isLoading = ref(false)
const showAddModal = ref(false)

const completedPlans = ref<RecordItem[]>([]) //已经完成的记录
const missedPlans = ref<RecordItem[]>([]) // 错过并且未完成的记录
const upcomingPlans = ref<RecordItem[]>([]) // 还没有到时间完成的任务

//分页相关数据
//已完成的计划的分页数据
const completedCurrentPage = ref(1)
const completedPageSize = 10
const pagedCompletedPlans = computed(() => {
  const start = (completedCurrentPage.value - 1) * completedPageSize
  return completedPlans.value.slice(start, start + completedPageSize)
})
const completedTotalPages = computed(() => {
  return Math.ceil(completedPlans.value.length / completedPageSize)
})

//错过计划
const missedCurrentPage = ref(1)
const missedPageSize = 10
const pagedMissedPlans = computed(() => {
  const start = (missedCurrentPage.value - 1) * missedPageSize
  return missedPlans.value.slice(start, start + missedPageSize)
})
const missedTotalPages = computed(() => Math.ceil(missedPlans.value.length / missedPageSize))

//即将到来的计划
const upcomingCurrentPage = ref(1)
const upcomingPageSize = 10
const pagedUpcomingPlans = computed(() => {
  const start = (upcomingCurrentPage.value - 1) * upcomingPageSize
  return upcomingPlans.value.slice(start, start + upcomingPageSize)
})
const upcomingTotalPages = computed(() => Math.ceil(upcomingPlans.value.length / upcomingPageSize))



// 定义注册新记录的结构
const newPlan = ref({
  start_time: '',
  end_time: '',
  activity_type: '',
  duration_minutes: 0,
  calories: 0,
  average_heart_rate: 0,
  is_completed: true
})

const selectedIds = ref<number[]>([]) // 存放勾选的 ID
// 是否全选
const isAllChecked = (list: RecordItem[]) => {
  return list.length > 0 && list.every(p => selectedIds.value.includes(p.id))
}

// 切换全选
const toggleAll = (list: RecordItem[]) => {
  if (isAllChecked(list)) {
    selectedIds.value = selectedIds.value.filter(id => !list.some(p => p.id === id))
  } else {
    selectedIds.value = Array.from(new Set([...selectedIds.value, ...list.map(p => p.id)]))
  }
}


// onMounted(() => {
//   userId.value = localStorage.getItem('user_id')
//   fetchPlans()
// })

onMounted(() => {
  userId.value = localStorage.getItem('user_id')
  fetchCompletedPlans()
  fetchMissedPlans()
  fetchUpcomingPlans()
})




const handleAdd = () => {
  showAddModal.value = true
}

const handleDelete = async () => {
  if (selectedIds.value.length === 0) {
    alert('请先选择要删除的训练记录')
    return
  }

  isLoading.value = true
  try {
    for (const id of selectedIds.value) {
      await axios.post('http://127.0.0.1:8000/delete-record', {
        record_id: id
      })
    }
    alert('删除成功')
    selectedIds.value = [] // 清空已选
      await fetchCompletedPlans()
      await fetchMissedPlans()
      await fetchUpcomingPlans()
  } catch (err) {
    console.error('删除失败:', err)
    alert('删除失败，请稍后重试')
  } finally {
    isLoading.value = false
  }
}


const handleToggleType = async () => {
  if (selectedIds.value.length === 0) {
    alert('请先选择要修改的训练记录')
    return
  }

  isLoading.value = true
  try {
    for (const id of selectedIds.value) {
      await axios.post('http://127.0.0.1:8000/toggle-record-status', {
        record_id: id
      })
    }
    alert('类型切换成功')
    selectedIds.value = [] // 清空已选
    await fetchCompletedPlans()
    await fetchMissedPlans()
    await fetchUpcomingPlans()
  } catch (err) {
    console.error('切换失败:', err)
    alert('类型切换失败，请稍后重试')
  } finally {
    isLoading.value = false
  }
}




//注册一个新的用户训练记录
const submitNewPlan = async () => {
  if (!userId.value) return

  // 自动计算运动时长（分钟）
  const plan = newPlan.value
  const start = new Date(plan.start_time).getTime()
  const end = new Date(plan.end_time).getTime()
  const durationInMinutes = Math.floor((end - start) / 60000) // 毫秒转分钟
  plan.duration_minutes = durationInMinutes

  // 基本校验

  if (!plan.start_time || !plan.end_time) {
    alert('开始时间和结束时间不能为空')
    return
  }

  if (new Date(plan.start_time) >= new Date(plan.end_time)) {
    alert('开始时间不能晚于或等于结束时间')
    return
  }

  if (!plan.activity_type.trim()) {
    alert('运动类型不能为空')
    return
  }

  if (!plan.duration_minutes || plan.duration_minutes <= 0) {
    alert('运动时长必须为正数')
    return
  }

  if (plan.calories < 0) {
    alert('卡路里不能为负数')
    return
  }

  if (plan.average_heart_rate < 0 || plan.average_heart_rate > 220) {
    alert('心率应在 0–220 之间')
    return
  }

  isLoading.value = true
  try {
    await axios.post('http://127.0.0.1:8000/saveMission', {
      user_id: Number(userId.value),
      ...newPlan.value
    })

    // 关闭弹窗并清空表单
    showAddModal.value = false
    Object.assign(newPlan.value, {
      start_time: '',
      end_time: '',
      activity_type: '',
      duration_minutes: 0,
      calories: 0,
      average_heart_rate: 0,
      is_completed: true
    })

    // 刷新数据
    await fetchCompletedPlans()
    await fetchMissedPlans()
    await fetchUpcomingPlans()
  } catch (err) {
    console.error('添加失败:', err)
  } finally {
    isLoading.value = false
  }
}

// const fetchPlans = async () => {
//   if (!userId.value) return
//
//   isLoading.value = true
//   try {
//     const response = await axios.post('http://127.0.0.1:8000/generate-user-records', {
//       user_id: Number(userId.value)
//     })
//
//     const records = response.data.records || []
//
//     plans.value = records.map((record: any) => ({
//       id: record.id,
//       type: record.activity_type || '未知',
//       duration: `${record.duration_minutes}分钟`,
//       calories: `${record.calories ?? 0} kcal`,
//       heartRate: `${record.average_heart_rate ?? '-'} bpm`,
//       startDate: new Date(record.start_time).toLocaleString(),
//       endDate: new Date(record.end_time).toLocaleString(),
//       completed: record.is_completed ? '是' : '否',
//     }))
//   } catch (error) {
//     console.error('获取用户训练记录失败:', error)
//   } finally {
//     isLoading.value = false
//   }
// }

const fetchCompletedPlans = async () => {
  if (!userId.value) return
  try {
    const res = await axios.post('http://127.0.0.1:8000/generate-user-records/completed', {
      user_id: Number(userId.value)
    })
    completedPlans.value = res.data.records.map(formatRecord)
  } catch (e) {
    console.error('获取已完成记录失败', e)
  }
}

const fetchMissedPlans = async () => {
  if (!userId.value) return
  try {
    const res = await axios.post('http://127.0.0.1:8000/generate-user-records/missed-plans', {
      user_id: Number(userId.value)
    })
    missedPlans.value = res.data.records.map(formatRecord)
  } catch (e) {
    console.error('获取错过的计划失败', e)
  }
}

const fetchUpcomingPlans = async () => {
  if (!userId.value) return
  try {
    const res = await axios.post('http://127.0.0.1:8000/generate-user-records/upcoming-plans', {
      user_id: Number(userId.value)
    })
    upcomingPlans.value = res.data.records.map(formatRecord)
  } catch (e) {
    console.error('获取即将进行的计划失败', e)
  }
}

// 格式化记录通用方法
const formatRecord = (record: any): RecordItem => ({
  id: record.id,
  type: record.activity_type || '未知',
  duration: `${record.duration_minutes}分钟`,
  calories: `${record.calories ?? 0} kcal`,
  heartRate: `${record.average_heart_rate ?? '-'} bpm`,
  startDate: new Date(record.start_time).toLocaleString(),
  endDate: new Date(record.end_time).toLocaleString(),
  completed: record.is_completed, // 保持布尔类型
})


//计算运动时长的方法
const computedDuration = computed(() => {
  const start = newPlan.value.start_time
  const end = newPlan.value.end_time

  if (!start || !end) return ''
  const startTime = new Date(start).getTime()
  const endTime = new Date(end).getTime()
  if (startTime >= endTime) return ''

  const diffMinutes = Math.floor((endTime - startTime) / 60000)
  return `${diffMinutes} 分钟`
})


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

.btn-toggle {
  padding: 0.6rem 1.2rem;
  font-size: 1rem;
  font-weight: bold;
  border: none;
  border-radius: 8px;
  color: #fff;
  background-color: #1976d2;
  cursor: pointer;
  transition: 0.3s ease;
}



.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  width: 500px;
  max-width: 90%;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.2);
}

.modal-content form {
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
}

.modal-content input,
.modal-content select {
  padding: 0.6rem;
  font-size: 1rem;
  border-radius: 6px;
  border: 1px solid #ccc;
}

.modal-buttons {
  display: flex;
  justify-content: space-between;
}

.table-section {
  margin-top: 2rem;
  padding-top: 1rem;
  border-top: 1px solid #ccc;
  text-align: left;
}

.section-title {
  font-size: 1.2rem;
  font-weight: bold;
  margin-bottom: 0.5rem;
}

.duration-preview {
  font-size: 0.95rem;
  color: #444;
  margin-top: -8px;
  margin-bottom: 12px;
}


/* 切换分页的按钮和下栏的样式*/
.pagination {
  display: block;
  width: 100%;
  margin-top: 1rem;
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
