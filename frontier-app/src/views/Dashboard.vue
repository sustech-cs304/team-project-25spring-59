<template>
  <div class="dashboard-container">
    <h2>📊 训练数据仪表板</h2>
     <el-button type="primary" @click="fetchTrainingData">刷新数据</el-button>

    <!-- 训练总览 -->
    <el-row :gutter="20">
      <el-col :span="6">
        <el-card class="stat-card">
          <h3>训练总时长</h3>
          <p>{{ totalDuration }} 分钟</p>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <h3>消耗卡路里</h3>
          <p>{{ totalCalories }} kcal</p>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <h3>训练次数</h3>
          <p>{{ totalSessions }} 次</p>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <h3>目标进度</h3>
          <el-progress :percentage="goalProgress" />
        </el-card>
      </el-col>
    </el-row>

    <!-- 数据可视化 -->
    <el-row :gutter="20">
      <el-col :span="12">
        <el-card>
          <h3>📈 训练时长趋势</h3>
          <LineChart :chart-data="chartData" />
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card>
          <h3>🍕 训练类别占比</h3>
          <PieChart :chart-data="pieData" />
        </el-card>
      </el-col>
    </el-row>

    <!-- 训练记录 -->
    <el-card class="history-section">
      <h3>📅 训练记录</h3>
      <el-date-picker v-model="selectedDate" type="daterange" placeholder="选择日期范围" />
      <el-table :data="filteredRecords">
        <el-table-column prop="date" label="日期" width="120"></el-table-column>
        <el-table-column prop="type" label="类型" width="120"></el-table-column>
        <el-table-column prop="duration" label="时长 (分钟)" width="120"></el-table-column>
        <el-table-column prop="calories" label="消耗卡路里" width="120"></el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import axios from "axios";
import LineChart from "../components/LineChart.vue";
import PieChart from "../components/PieChart.vue";
import {API_BASE_URL} from "../configs/network_config.js";


// 训练数据
const records = ref([]);

// 统计数据
const totalDuration = computed(() => records.value.reduce((sum, r) => sum + r.duration, 0));
const totalCalories = computed(() => records.value.reduce((sum, r) => sum + r.calories, 0));
const totalSessions = computed(() => records.value.length);
const goalProgress = computed(() => Math.min((totalDuration.value / 500) * 100, 100)); // 假设目标是 500 分钟

// 日期筛选
const selectedDate = ref(null);
const filteredRecords = computed(() => {
  if (!selectedDate.value) return records.value;
  const [start, end] = selectedDate.value;
  return records.value.filter(r => new Date(r.date) >= start && new Date(r.date) <= end);
});

// 折线图数据
const chartData = computed(() => ({
  labels: records.value.map(r => r.date),
  datasets: [{ label: "训练时长", data: records.value.map(r => r.duration), borderColor: "#42A5F5" }]
}));

// 饼图数据
const pieData = computed(() => {
  const typeCounts = records.value.reduce((acc, r) => {
    acc[r.type] = (acc[r.type] || 0) + r.duration;
    return acc;
  }, {});
  return {
    labels: Object.keys(typeCounts),
    datasets: [{ data: Object.values(typeCounts), backgroundColor: ["#FF6384", "#36A2EB", "#FFCE56"] }]
  };
});

// 获取训练数据（模拟 API）
const fetchTrainingData = async () => {
  try {
    // 获取训练总览数据
    const summaryResponse = await axios.post(`${API_BASE_URL}/stats/summary`, { user_id: 1 });
    totalDuration.value = summaryResponse.data.total_minutes;
    totalCalories.value = summaryResponse.data.estimated_calories;

    // 获取每周趋势数据
    const weeklyTrendResponse = await axios.post(`${API_BASE_URL}/stats/weekly-trend`, { user_id: 1 });
    const trendData = weeklyTrendResponse.data;

    // 更新折线图数据
    chartData.value = {
      labels: Object.keys(trendData),
      datasets: [{ label: "训练时长", data: Object.values(trendData), borderColor: "#42A5F5" }]
    };

    // 模拟训练记录数据（如果需要）
    records.value = Object.keys(trendData).map(date => ({
      date,
      type: "有氧", // 示例类型
      duration: trendData[date],
      calories: (trendData[date] / 60) * 8 * 60 // 假设体重60kg，MET=8
    }));
  } catch (error) {
    console.error("获取训练数据失败:", error.response ? error.response.data : error.message);
}
};


// 加载数据
onMounted(() => {
  fetchTrainingData();
});

/**
 * 暴露给父组件的API和数据
 */
defineExpose({
  /**
   * 原始训练记录数据
   * @member {Array<{date: string, type: string, duration: number, calories: number}>}
   * @description 包含所有训练记录的数组，每个记录包含日期、类型、时长和卡路里
   * @example
   * // 父组件中获取原始数据
   * const rawData = dashboardRef.value.records;
   */
  records,

  /**
   * 总训练时长（分钟）
   * @member {number}
   * @description 计算所有训练记录的总时长（单位：分钟）
   * @example
   * // 父组件中获取总时长
   * const minutes = dashboardRef.value.totalDuration;
   */
  totalDuration,

  /**
   * 总消耗卡路里
   * @member {number}
   * @description 计算所有训练记录的总卡路里消耗
   * @example
   * // 父组件中获取总卡路里
   * const cals = dashboardRef.value.totalCalories;
   */
  totalCalories,

  /**
   * 总训练次数
   * @member {number}
   * @description 训练记录的总数量
   * @example
   * // 父组件中获取训练次数
   * const sessions = dashboardRef.value.totalSessions;
   */
  totalSessions,

  /**
   * 目标进度百分比
   * @member {number}
   * @description 当前训练时长与目标时长的百分比（上限100%）
   * @example
   * // 父组件中获取进度
   * const progress = dashboardRef.value.goalProgress;
   */
  goalProgress,

  /**
   * 根据日期筛选后的记录
   * @member {Array}
   * @description 基于selectedDate范围筛选后的训练记录
   * @example
   * // 父组件中设置日期范围
   * dashboardRef.value.selectedDate = [new Date('2023-01-01'), new Date('2023-12-31')];
   * // 然后获取筛选结果
   * const filtered = dashboardRef.value.filteredRecords;
   */
  filteredRecords,

  /**
   * 折线图数据
   * @member {Object}
   * @property {string[]} labels - 日期标签数组
   * @property {Object[]} datasets - 图表数据集
   * @description 用于LineChart组件的格式化数据
   * @example
   * // 父组件中获取图表数据
   * const lineData = dashboardRef.value.chartData;
   */
  chartData,

  /**
   * 饼图数据
   * @member {Object}
   * @property {string[]} labels - 训练类型标签
   * @property {Object[]} datasets - 图表数据集
   * @description 用于PieChart组件的格式化数据
   * @example
   * // 父组件中获取饼图数据
   * const pieData = dashboardRef.value.pieData;
   */
  pieData,

  /**
   * 重新加载训练数据
   * @function
   * @async
   * @description 强制刷新所有统计数据和图表
   * @example
   * // 父组件中刷新数据
   * await dashboardRef.value.fetchTrainingData();
   */
  fetchTrainingData,

  /**
   * 当前选择的日期范围
   * @member {[Date, Date]|null}
   * @description 用于筛选的双日期范围（开始日期和结束日期）
   * @example
   * // 父组件中设置日期范围
   * dashboardRef.value.selectedDate = [new Date(), new Date()];
   */
  selectedDate
});
</script>

<style scoped>
.dashboard-container {
  max-width: 1200px;
  margin: 20px auto;
  text-align: center;
}
.stat-card {
  text-align: center;
  padding: 20px;
}
.history-section {
  margin-top: 20px;
}
</style>
