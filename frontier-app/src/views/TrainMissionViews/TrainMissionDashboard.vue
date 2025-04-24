<template>
  <div class="layout-wrapper">
    <div class="background-color-layer" />
    <div class="background-image-layer" />
    <Header :base="routeBase" />

    <CalorieChart/>
    <TimeBar/>

  </div>
</template>

<script setup lang="ts">
import Header from '../../components/TrainMission/Header.vue'
import CalorieChart from "../../components/TrainMission/Charts/CalorieChart.vue";
import TimeBar from "../../components/TrainMission/Charts/TimeBar.vue";
import {ref, onMounted} from "vue";
import Weekly_Plan from "../../components/TrainMission/Plans/Weekly_Plan.vue";
const routeBase = ref('/')
onMounted(() => {
  routeBase.value = window.location.origin + '/'  // 自动拼接 /
})


</script>

<style lang="scss">
.layout-wrapper {
  position: relative;
  min-height: 400vh;
  overflow-x: hidden;

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

</style>
