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
    const summaryResponse = await axios.post("http://127.0.0.1:5000/stats/summary", { user_id: 1 });
    totalDuration.value = summaryResponse.data.total_minutes;
    totalCalories.value = summaryResponse.data.estimated_calories;

    // 获取每周趋势数据
    const weeklyTrendResponse = await axios.post("http://127.0.0.1:5000/stats/weekly-trend", { user_id: 1 });
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
