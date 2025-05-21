<template>
  <div class="weekly-plan" :style="{ backgroundImage: `url(${bgImage})` }">
    <div class="header">
      <div class="date-range">{{ dateRange }}</div>
      <div class="controls">
        <el-button type="primary" plain size="small" @click="prevWeek">← 上一周</el-button>
        <el-button type="primary" plain size="small" @click="nextWeek">下一周 →</el-button>
      </div>
    </div>

    <!-- 添加用于定位的容器 -->
    <div class="task-panel-container">
      <TaskPanel
        v-for="(day, index) in fullWeekTasks"
        :key="index"
        :title="day.title"
        :tasks="day.tasks"
        :style="panelPositions[index]"
      />
    </div>
  </div>
</template>


<script setup lang="ts">
import TaskPanel from './TaskPanel.vue'
// @ts-ignore
import bgImage from '../../../assets/plans/weekly_plan.png'
import { ref, computed, watch } from 'vue'
import dayjs from 'dayjs'
import { onMounted } from "vue";
import axios from "axios";

const currentDate = ref(dayjs())

const startOfWeek = computed(() => currentDate.value.startOf('week').add(1, 'day'))
const endOfWeek = computed(() => currentDate.value.endOf('week').add(1, 'day'))
const dateRange = computed(() =>
  `${startOfWeek.value.format('YYYY年M月D日')} - ${endOfWeek.value.format('M月D日')}`
)


// 将 weekTasks 定义为 ref 数组
const weekTasks = ref([
  { title: '周一', tasks: [] },
  { title: '周二', tasks: [] },
  { title: '周三', tasks: [] },
  { title: '周四', tasks: [] },
  { title: '周五', tasks: [] },
  { title: '周六', tasks: [] },
  { title: '周日', tasks: [] }
])

const panelPositions = [
  { top: '350px', left: '80px' },
  { top: '350px', left: '680px' },
  { top: '350px', left: '1280px' },
  { top: '350px', left: '1880px' },
  { top: '1100px', left: '80px' },
  { top: '1100px', left: '680px' },
  { top: '1100px', left: '1280px' }
]

// 计算 weekDays 和日期格式化
const weekDays = computed(() => {
  const start = startOfWeek.value
  const labels = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']

  return Array.from({ length: 7 }).map((_, i) => {
    const date = start.add(i, 'day')
    return {
      dateText: date.format('YYYY年M月D日'), // 格式化成 "4月8日"
      weekday: labels[i],
      fullTitle: `${date.format('M月D日')}（${labels[i]}）`,
      tasks: [] // placeholder，下面替换进去
    }
  })
})

// 获取用户ID
const userId = localStorage.getItem('user_id')

const updateDailyTasks = async () => {
  if (!userId) return

  // 遍历 weekDays 获取每天的任务
  for (let i = 0; i < 7; i++) {
    const day = weekDays.value[i]
    const dateStr = day.dateText // 获取几月几日格式的日期

    try {
      console.log("当前调用的命令："+userId+" "+ dateStr)
      // 发送 API 请求，获取当天的训练记录
      const response = await axios.post('http://10.12.184.92:8000/get-daily-plan', {
        user_id: String(userId),
        date_str: dateStr
      })

      // 获取返回的训练记录
      const trainingItems = response.data.training_items || []

      // 解析训练记录并更新 tasks
      day.tasks = trainingItems.map(item => {
        return item.replace(/\*\*/g, '') // 清除 ** 标记（如果有的话）
      })

      // 控制台输出每一天的任务
      console.log(`任务 - ${day.fullTitle}:`, day.tasks)

      // 更新 weekTasks 中对应的任务内容
      weekTasks.value[i].tasks = day.tasks

    } catch (error) {
      console.error("获取每日任务失败", error)
      day.tasks = [] // 请求失败时，清空任务
    }
  }
}

// 在组件挂载后获取每日任务
onMounted(() => {
  updateDailyTasks()
})

// 更新 weekDays 数据，计算每一周的日期
const updateWeekDays = () => {
  // 更新 currentDate，触发 weekDays 的重新计算
  currentDate.value = dayjs(currentDate.value) // 强制触发响应式更新
}

const prevWeek = () => {
  currentDate.value = currentDate.value.subtract(1, 'week')
  updateWeekDays() // 更新 weekDays
  updateDailyTasks() // 刷新任务
}

const nextWeek = () => {
  currentDate.value = currentDate.value.add(1, 'week')
  updateWeekDays() // 更新 weekDays
  updateDailyTasks() // 刷新任务
}


const fullWeekTasks = computed(() =>
  weekDays.value.map((item, index) => ({
    title: item.fullTitle,     // M月D日（周X）
    tasks: weekTasks.value[index]?.tasks || [] // 使用动态的 weekTasks
  }))
)

</script>

<style lang="scss" scoped>
.weekly-plan {
  width: 100%;
  max-width: 2526px;
  aspect-ratio: 2526 / 1787;
  margin: 100px auto;
  padding: 24px;
  border-radius: 20px;
  position: relative;
  color: #333;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
  backdrop-filter: blur(4px);
  overflow: hidden;

  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;

  .header {
    position: absolute;
    top: 20px;
    left: 430px;
    display: flex;
    align-items: center;
    gap: 6px;
    padding: 4px 6px;
    background: rgba(255, 255, 255, 0.5);
    border-radius: 6px;
    font-size: 20px;
    transform: scale(0.6);
    transform-origin: top right;
    box-shadow: 0 1px 4px rgba(0, 0, 0, 0.06);

    .date-range {
      font-size: 20px;
      padding: 2px 4px;
      white-space: nowrap;
    }

    .controls {
      display: flex;
      gap: 4px;

      .el-button {
        font-size: 11px;
        padding: 2px 5px;
        height: auto;
        line-height: 1;
        background-color: rgba(255, 255, 255, 0.4);
        border: none;
        color: #333;
      }
    }
  }
}

.task-panel-container {
  position: relative; // 相对于 .weekly-plan 定位
  width: 100%;
  height: 100%;
}

.task-panel-container :deep(.task-panel) {
  position: absolute; // 每个 TaskPanel 使用 style 动态设置位置
}

</style>
