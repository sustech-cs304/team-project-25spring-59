<template>
  <div class="layout-wrapper">
    <div class="background-color-layer" />
    <div class="background-image-layer" />
    <!-- 顶部 Header 固定 -->
    <Header :base="routeBase" />

    <!-- 主体内容 -->
    <main class="train-mission-main">
      <LevelBox />
      <Specification />
    </main>

  </div>
</template>

<script setup lang="ts">
import Header from '../../components/TrainMission/Header.vue'
import LevelBox from '../../components/TrainMission/MissionListVisualize/LevelBoxTrainMission.vue'
import {ref, onMounted} from "vue";
import Specification from "../../components/TrainMission/MissionListVisualize/Specification.vue";
const routeBase = ref('/')
const userid = ref('')

onMounted(() => {
  routeBase.value = window.location.origin + '/'
  userid.value = localStorage.getItem('user_id') || '未知用户'
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

.train-mission-main {
  position: relative;
  z-index: 1;
  padding: 0;
  margin-top: 120px;
}

</style>
