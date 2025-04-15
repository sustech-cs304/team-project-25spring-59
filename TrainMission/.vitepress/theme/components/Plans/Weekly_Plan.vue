<template>
  <div class="weekly-plan" :style="{ backgroundImage: `url(${bgImage})` }">
    <div class="header">
      <div class="date-range">{{ dateRange }}</div>
      <div class="controls">
        <el-button type="primary" plain size="small" @click="prevWeek">← 上一周</el-button>
        <el-button type="primary" plain size="small" @click="nextWeek">下一周 →</el-button>
      </div>
    </div>
  </div>

  <TaskPanel
      v-for="(day, index) in fullWeekTasks"
    :key="index"
    :title="day.title"
    :tasks="day.tasks"
    :panelStyle="panelPositions[index]"
  />



</template>

<script setup lang="ts">
import TaskPanel from './TaskPanel.vue'
import bgImage from '../../assets/plans/weekly_plan.png'
import { ref, computed } from 'vue'
import dayjs from 'dayjs'
import {onMounted} from "vue";
import axios from "axios";

const currentDate = ref(dayjs())

const startOfWeek = computed(() => currentDate.value.startOf('week').add(1, 'day'))
const endOfWeek = computed(() => currentDate.value.endOf('week').add(1, 'day'))
const dateRange = computed(() =>
  `${startOfWeek.value.format('YYYY年M月D日')} - ${endOfWeek.value.format('M月D日')}`
)

const prevWeek = () => currentDate.value = currentDate.value.subtract(1, 'week')
const nextWeek = () => currentDate.value = currentDate.value.add(1, 'week')

// 每天的任务
// const weekTasks = [
//   { title: '周一', tasks: ['✔️ 写周报', '🧘 冥想', '✔️ 写周报', '🧘 冥想', '✔️ 写周报', '🧘 冥想', '✔️ 写周报', '🧘 冥想'] },
//   { title: '周二', tasks: ['📖 阅读 20 页', '✅ 英语练习'] },
//   { title: '周三', tasks: ['🏃 跑步 3 公里'] },
//   { title: '周四', tasks: ['💻 写代码', '☕ 放松一下'] },
//   { title: '周五', tasks: ['✅ 总结', '🍿 电影时间'] },
//   { title: '周六', tasks: ['🧹 打扫', '🎮 玩游戏'] },
//   { title: '周日', tasks: ['📝 反思', '📅 下周计划'] }
// ]

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
  { top: '410px', left: '470px' },
  { top: '410px', left: '670px' },
  { top: '410px', left: '870px' },
  { top: '410px', left: '1070px' },
  { top: '665px', left: '470px' },
  { top: '665px', left: '670px' },
  { top: '665px', left: '870px' }
]

// 计算 weekDays 和日期格式化
// 计算 weekDays 和日期格式化
const weekDays = computed(() => {
  const start = startOfWeek.value
  const labels = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']

  return Array.from({ length: 7 }).map((_, i) => {
    const date = start.add(i, 'day')
    return {
      dateText: date.format('M月D日'), // 格式化成 "4月8日"
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
      const response = await axios.post('http://127.0.0.1:8000/get-daily-plan', {
        user_id: userId,
        date_str: dateStr
      })

      // 获取返回的训练记录
      const trainingItems = response.data.training_items || []

      // 解析训练记录并更新 tasks
      day.tasks = trainingItems.map(item => {
        // 可以根据返回的格式对 item 进行处理
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


// 在组件挂载后获取每日任务
onMounted(() => {
  updateDailyTasks()
})





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
</style>
