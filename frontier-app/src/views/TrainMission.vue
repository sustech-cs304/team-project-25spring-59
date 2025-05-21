<template>
  <div class="layout-wrapper">
    <div class="background-color-layer" />
    <div class="background-image-layer" />
    <Header :base="routeBase" />

    <main>
      <section class="banner-wrapper">
        <Banner
        cover="/assets/banner/banner.webp"
        hello="Hello, Vue"
        highText="Sensei’ TrainMission"
        motto="何気ない日常で、ほんの少しの奇跡を見つける物語。"
        :social="[
          { icon: 'fa-github', url: 'https://github.com' },
          { icon: 'fa-twitter', url: 'https://twitter.com' }
        ]"
      />
      </section>

    </main>

    <section class="plans-container">
      <PlanList />
      <InprogressPlan />
    </section>

    <SpinePlayer></SpinePlayer>
  </div>
</template>

<script setup lang="ts">
import Banner from '../components/TrainMission/Banner.vue' // 你根据实际路径调整
import Header from '../components/TrainMission/Header.vue'
import PlanList from '../components/TrainMission/MissionListVisualize/Planlist.vue'
import InprogressPlan from "../components/TrainMission/MissionListVisualize/InprogressPlan.vue";
import {ref, onMounted} from "vue";


// spine-player
import SpinePlayer from '../components/Spine-Player-MainMenu/index.vue'



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


//横向展示的容器
.plans-container {
  display: flex;
  justify-content: center;
  align-items: flex-start;
  flex-wrap: wrap;
  gap: 2rem;
  padding: 2rem;
  margin-left: 25rem;
}

// 可选：让每个计划组件宽度更合适
.plans-container > * {
  flex: 1 1 45%;
  max-width: 600px;
}

</style>
