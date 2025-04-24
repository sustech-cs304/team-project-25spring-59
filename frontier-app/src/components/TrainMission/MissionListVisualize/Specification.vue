<template>
  <div class="spec-container">
    <!-- 顶部选择栏 -->
    <div class="top-bar">
      <div class="current-record">
        <h3>当前记录：{{ selectedRecord.name }}</h3>
        <p>{{ selectedRecord.date }} | {{ selectedRecord.type }}</p>
      </div>

      <select v-model="selectedId" @change="onChange">
        <option v-for="record in records" :key="record.id" :value="record.id">
          {{ record.name }}
        </option>
      </select>
    </div>

    <!-- 主要数据展示 -->
    <div class="metrics">
      <div class="metric-box">
        <h4>当前心率</h4>
        <p class="value">{{ selectedRecord.heartRate }} bpm</p>
      </div>
      <div class="metric-box">
        <h4>当前速度</h4>
        <p class="value">{{ selectedRecord.speed }} km/h</p>
      </div>
      <div class="metric-box">
        <h4>已消耗卡路里</h4>
        <p class="value">{{ selectedRecord.calories }} kcal</p>
      </div>
    </div>

    <!-- 底部进度条 -->
    <div class="progress-section">
      <p>已运动时间：{{ selectedRecord.timeElapsed }} 分钟 / 总时长：{{ selectedRecord.totalTime }} 分钟</p>
      <progress :value="selectedRecord.timeElapsed" :max="selectedRecord.totalTime" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

interface RecordItem {
  id: number
  name: string
  type: string
  date: string
  heartRate: number
  speed: number
  calories: number
  timeElapsed: number
  totalTime: number
}

const records = ref<RecordItem[]>([
  {
    id: 1,
    name: '周一 跑步',
    type: '有氧',
    date: '2025-04-20',
    heartRate: 128,
    speed: 8.2,
    calories: 320,
    timeElapsed: 25,
    totalTime: 40
  },
  {
    id: 2,
    name: '周三 骑行',
    type: '耐力',
    date: '2025-04-17',
    heartRate: 112,
    speed: 16.5,
    calories: 410,
    timeElapsed: 30,
    totalTime: 60
  }
])

const selectedId = ref(1)
const selectedRecord = computed(() =>
  records.value.find((r) => r.id === selectedId.value) || records.value[0]
)

const onChange = () => {

}
</script>

<style scoped>
.spec-container {
  max-width: 800px;
  margin: 2rem auto;
  padding: 2rem;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
}

.top-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.current-record {
  font-weight: bold;
  font-size: 1rem;
  color: #333;
}

select {
  padding: 0.4rem 1rem;
  border-radius: 8px;
  border: 1px solid #ccc;
  background: #fff;
  font-size: 1rem;
}

.metrics {
  display: flex;
  justify-content: space-around;
  margin-bottom: 2rem;
  text-align: center;
}

.metric-box {
  background-color: rgba(255, 255, 255, 0.85);
  padding: 1rem;
  border-radius: 10px;
  width: 30%;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.metric-box .value {
  font-size: 1.5rem;
  font-weight: bold;
  color: #3a7bd5;
  margin-top: 0.5rem;
}

.progress-section {
  text-align: center;
}

progress {
  width: 100%;
  height: 18px;
  border-radius: 10px;
  overflow: hidden;
  appearance: none;
}

progress::-webkit-progress-bar {
  background-color: #eee;
  border-radius: 10px;
}

progress::-webkit-progress-value {
  background-color: #4caf50;
  border-radius: 10px;
}
</style>
