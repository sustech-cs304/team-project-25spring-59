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

const currentDate = ref(dayjs())

const startOfWeek = computed(() => currentDate.value.startOf('week').add(1, 'day'))
const endOfWeek = computed(() => currentDate.value.endOf('week').add(1, 'day'))
const dateRange = computed(() =>
  `${startOfWeek.value.format('YYYY年M月D日')} - ${endOfWeek.value.format('M月D日')}`
)

const prevWeek = () => currentDate.value = currentDate.value.subtract(1, 'week')
const nextWeek = () => currentDate.value = currentDate.value.add(1, 'week')

// 每天的任务
const weekTasks = [
  { title: '周一', tasks: ['✔️ 写周报', '🧘 冥想', '✔️ 写周报', '🧘 冥想', '✔️ 写周报', '🧘 冥想', '✔️ 写周报', '🧘 冥想'] },
  { title: '周二', tasks: ['📖 阅读 20 页', '✅ 英语练习'] },
  { title: '周三', tasks: ['🏃 跑步 3 公里'] },
  { title: '周四', tasks: ['💻 写代码', '☕ 放松一下'] },
  { title: '周五', tasks: ['✅ 总结', '🍿 电影时间'] },
  { title: '周六', tasks: ['🧹 打扫', '🎮 玩游戏'] },
  { title: '周日', tasks: ['📝 反思', '📅 下周计划'] }
]

const panelPositions = [
  { top: '410px', left: '470px' },
  { top: '410px', left: '670px' },
  { top: '410px', left: '870px' },
  { top: '410px', left: '1070px' },
  { top: '665px', left: '470px' },
  { top: '665px', left: '670px' },
  { top: '665px', left: '870px' }
]

const weekDays = computed(() => {
  const start = startOfWeek.value
  const labels = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']

  return Array.from({ length: 7 }).map((_, i) => {
    const date = start.add(i, 'day')
    return {
      dateText: date.format('YYYY年M月D日'),
      weekday: labels[i],
      fullTitle: `${date.format('M月D日')}（${labels[i]}）`,
      tasks: [] // placeholder，下面替换进去
    }
  })
})

const fullWeekTasks = computed(() =>
  weekDays.value.map((item, index) => ({
    title: item.fullTitle,     // ✅ M月D日（周X）
    tasks: weekTasks[index]?.tasks || []
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
