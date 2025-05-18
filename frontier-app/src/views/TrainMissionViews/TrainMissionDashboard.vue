<template>

  <div class="layout-wrapper">
    <div class="background-color-layer" />
    <div class="background-image-layer" />
    <Header :base="routeBase" />

    <!-- 主体内容 -->
        <div class="main-content-wrapper">
      <!-- 左侧内容 -->
      <div class="main-content">
        <!-- 用户训练统计数据展示区域 -->
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
        </div>
      </div>

    </div>


    <!-- AI 建议浮动侧栏 -->
    <AITrainerAssistant :visible="showAISidebar" @close="showAISidebar = false" />



    <!-- 控制显示按钮 -->
<!--    <button class="toggle-ai-btn" @click="toggleAISidebar" v-if="!showAISidebar">查看 AI 建议</button>-->
  </div>
  <SpinePlayer @show-ai-panel="handleShowAI" />
</template>


<script setup lang="ts">
import Header from '../../components/TrainMission/Header.vue'
import TrainTimeChart from "../../components/TrainMission/Charts/TrainTimeChart.vue";
import TimeBar from "../../components/TrainMission/Charts/TimeBar.vue";
import {ref, onMounted, nextTick} from "vue";
import Weekly_Plan from "../../components/TrainMission/Plans/Weekly_Plan.vue";
import axios from "axios";
import SpinePlayer from "../../components/Spine-Player-Dashboard/index.vue";
import AITrainerAssistant from './aitrainer.vue'

const routeBase = ref('/')
const userId = ref<string | null>(null)
onMounted(() => {
  routeBase.value = window.location.origin + '/'
  userId.value = localStorage.getItem('user_id')
  fetchSummary()
})

//这一部分是显示ai界面或者隐藏的方法
const showAISidebar = ref(false)

const handleShowAI = () => {
  console.log('[debug] show-ai-panel event received!')
  showAISidebar.value = !showAISidebar.value

}






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



.main-content-wrapper {
  display: flex;
  justify-content: center;
  gap: 1rem;
  padding: 0 1rem;
}

.main-content {
  flex: 1;
  max-width: 100%;
}

.ai-float-sidebar {
  position: fixed;
  top: 80px;
  right: 0;
  width: 600px;
  height: calc(100vh - 80px);
  background: white;
  box-shadow: -4px 0 12px rgba(0, 0, 0, 0.1);
  z-index: 2000;
  display: flex;
  flex-direction: column;

  .ai-panel {
    display: flex;
    flex-direction: column;
    height: 100%;
    padding: 1rem;
  }

  .ai-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid #ddd;
    padding-bottom: 0.5rem;

    h3 {
      margin: 0;
      font-size: 1.2rem;
    }

    button {
      background: none;
      border: none;
      color: #888;
      cursor: pointer;
      font-size: 0.9rem;
    }
  }

  .ai-content {
    flex: 1;
    overflow-y: auto;
    margin: 1rem 0;

    .placeholder {
      color: #999;
      font-style: italic;
    }
  }

  .ai-input {
    display: flex;
    gap: 0.5rem;

    input {
      flex: 1;
      padding: 0.5rem;
      border: 1px solid #ddd;
      border-radius: 6px;
    }

    button {
      padding: 0.5rem 1rem;
      background-color: #1976d2;
      color: #fff;
      border: none;
      border-radius: 6px;
      cursor: pointer;

      &:hover {
        background-color: #125ca1;
      }
    }
  }
}

.ai-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #ddd;
  padding-bottom: 0.5rem;

  h3 {
    margin: 0;
    font-size: 1.2rem;
  }

  button {
    background: none;
    border: none;
    color: #888;
    cursor: pointer;
    font-size: 0.9rem;
  }
}

.ai-content {
  flex: 1;
  padding: 1rem 0;
  overflow-y: auto;

  .placeholder {
    color: #999;
    font-style: italic;
  }
}

.ai-input {
  display: flex;
  gap: 0.5rem;

  input {
    flex: 1;
    padding: 0.5rem;
    border: 1px solid #ddd;
    border-radius: 6px;
  }

  button {
    padding: 0.5rem 1rem;
    background-color: #1976d2;
    color: #fff;
    border: none;
    border-radius: 6px;
    cursor: pointer;

    &:hover {
      background-color: #125ca1;
    }
  }
}

.toggle-ai-btn {
  position: fixed;
  right: 1rem;
  bottom: 2rem;
  padding: 0.8rem 1.2rem;
  background-color: #1976d2;
  color: white;
  border: none;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.2);
  cursor: pointer;
  z-index: 1000;
}

//动画淡入淡出
.ai-float-sidebar {
  transition: transform 0.3s ease, opacity 0.3s ease;
  transform: translateX(0);
  opacity: 1;

  &.hidden {
    transform: translateX(100%);
    opacity: 0;
  }
}


.chat-message {
  display: flex;
  align-items: flex-start;
  margin-bottom: 1rem;

  &.user {
    flex-direction: row-reverse;
    .bubble {
      background-color: #1976d2;
      color: white;
      border-top-right-radius: 0;
    }
  }

  &.assistant {
    .bubble {
      background-color: #f0f0f0;
      border-top-left-radius: 0;
    }
  }

  .avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    object-fit: cover;
    margin: 0 0.75rem;
  }

  .bubble {
    max-width: 75%;
    padding: 0.75rem 1rem;
    border-radius: 1rem;
    font-size: 0.95rem;
    line-height: 1.4;
    word-break: break-word;
    background-color: #eee;
  }
}


//ai对话历史的样式
.chat-message {
  display: flex;
  align-items: flex-start;
  margin-bottom: 1rem;

  &.user {
    flex-direction: row-reverse;
    .bubble {
      background-color: #1976d2;
      color: white;
      border-top-right-radius: 0;
    }
  }

  &.assistant {
    .bubble {
      background-color: #f0f0f0;
      border-top-left-radius: 0;
    }
  }

  .avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    object-fit: cover;
    margin: 0 0.75rem;
  }

  .bubble {
    max-width: 75%;
    padding: 0.75rem 1rem;
    border-radius: 1rem;
    font-size: 0.95rem;
    line-height: 1.4;
    word-break: break-word;
    background-color: #eee;
  }
}



</style>
