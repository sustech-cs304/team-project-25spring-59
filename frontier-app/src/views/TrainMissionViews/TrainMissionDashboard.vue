<template>
  <div class="layout-wrapper">
    <div class="background-color-layer" />
    <div class="background-image-layer" />
    <Header :base="routeBase" />

    <!--  用户训练统计数据展示区域 -->
    <div class="stats-summary-cards" v-if="summary">
      <p>用户 ID：{{ userId }}</p>
      <div class="cards-container">
        <div class="stat-card">
          <h4>总训练时长</h4>
          <p>{{ summary.total_minutes }} 分钟</p>
        </div>
        <div class="stat-card">
          <h4>估算卡路里</h4>
          <p>{{ summary.estimated_calories }} kcal</p>
        </div>
        <div class="stat-card">
          <h4>实际卡路里</h4>
          <p>{{ summary.actual_calories }} kcal</p>
        </div>
        <div class="stat-card">
          <h4>平均心率</h4>
          <p>{{ summary.average_heart_rate ?? '-' }} bpm</p>
        </div>
        <div class="stat-card">
          <h4>最大心率</h4>
          <p>{{ summary.max_heart_rate ?? '-' }} bpm</p>
        </div>
      </div>
    </div>


    <!-- 图表部分 -->
    <div class="chart-container">
      <TrainTimeChart />
<!--      <TimeBar />-->
    </div>

  </div>
</template>

<script setup lang="ts">
import Header from '../../components/TrainMission/Header.vue'
import TrainTimeChart from "../../components/TrainMission/Charts/TrainTimeChart.vue";
import TimeBar from "../../components/TrainMission/Charts/TimeBar.vue";
import {ref, onMounted} from "vue";
import Weekly_Plan from "../../components/TrainMission/Plans/Weekly_Plan.vue";
import axios from "axios";
const routeBase = ref('/')
const userId = ref<string | null>(null)


onMounted(() => {
  routeBase.value = window.location.origin + '/'
  userId.value = localStorage.getItem('user_id')
  fetchSummary()
})




const summary = ref<null | {
  total_minutes: number
  estimated_calories: number
  actual_calories: number
  average_heart_rate: number | null
  max_heart_rate: number | null
}>(null)

const fetchSummary = async () => {
  if (!userId.value) return
  try {
    const res = await axios.post('http://localhost:8000/stats/summary', {
      user_id: Number(userId.value)
    })
    summary.value = res.data
  } catch (e) {
    console.error('获取训练汇总失败:', e)
  }
}

</script>

<style lang="scss">
.layout-wrapper {
  position: relative;
  min-height: 400vh;
  overflow-x: hidden;
  top: 100px;

  .background-color-layer {
    background-color: #eaebed;
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    z-index: -1000;
  }

  .background-image-layer {
    background: url('/assets/background.svg') no-repeat center bottom;
    background-size: cover;
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    z-index: -999;
    pointer-events: none;
  }
}

main {
  position: relative;
  z-index: 1;
  padding: 0; // 去掉默认 padding
}


.chart-container {
  display: flex;
  flex-direction: column; // 如果你想图表竖着排列
  align-items: center;
  justify-content: center;
  padding: 2rem 1rem;
  gap: 2rem; // 图表之间的间距
}


.stats-summary {
  text-align: center;
  margin-bottom: 2rem;
  font-size: 1.05rem;
  font-weight: 500;
  color: #333;
  line-height: 1.6;
}


/*用户总体数据显示 */
.stats-summary-cards {
  text-align: center;
  margin-bottom: 2rem;

  .cards-container {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 1.5rem;
  }

  .stat-card {
    background: white;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgb(0 0 0 / 0.1);
    padding: 1.5rem 2rem;
    width: 160px;
    color: #333;

    h4 {
      margin-bottom: 0.6rem;
      font-weight: 600;
      font-size: 1.1rem;
    }

    p {
      font-size: 1.3rem;
      font-weight: 700;
      color: #1976d2; /* 主色调 */
      margin: 0;
    }
  }
}


</style>
