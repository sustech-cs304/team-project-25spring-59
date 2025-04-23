<template>
  <div class="layout-wrapper">
    <div class="background-color-layer" />
    <div class="background-image-layer" />
    <Header :base="routeBase" />

    <main>
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
    </main>

  </div>
</template>

<script setup lang="ts">
import Header from '../../components/TrainMission/Header.vue'
import {ref, onMounted} from "vue";
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
