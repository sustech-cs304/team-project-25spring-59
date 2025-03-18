<template>
  <div>
    <canvas ref="pieChart"></canvas>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import Chart from "chart.js/auto";

const props = defineProps(["chartData"]);
const pieChart = ref(null);

onMounted(() => {
  new Chart(pieChart.value, {
    type: "pie",
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
