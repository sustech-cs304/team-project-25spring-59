<template>
  <div>
    <canvas ref="lineChart"></canvas>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import Chart from "chart.js/auto";

const props = defineProps(["chartData"]);
const lineChart = ref(null);

onMounted(() => {
  new Chart(lineChart.value, {
    type: "line",
    data: props.chartData,
    options: {
      responsive: true,
      maintainAspectRatio: false
    }
  });
});
</script>

<style scoped>
canvas {
  max-width: 100%;
  height: 300px;
}
</style>
