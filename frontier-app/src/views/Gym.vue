<script setup>

import {ref} from "vue";
import GymList from "../components/reservation/GymList.vue";
import GymCourses from "../components/reservation/GymCourses.vue";

const gymId = ref('')
const currentCom = ref(GymList)

function goToCourse(id) {
  currentCom.value = GymCourses;
  gymId.value = id
  console.log(id)
}


</script>

<template>
  <el-menu :default-active="activeIndex" class="el-menu-demo" mode="horizontal" @select="handleSelect">
    <el-menu-item index="1">Processing Center</el-menu-item>
    <el-menu-item index="2" disabled>Info</el-menu-item>
    <el-menu-item index="3"><a href="https://www.ele.me" target="_blank">Orders</a></el-menu-item>
  </el-menu>

  <el-tabs type="border-card">
    <el-tab-pane label="健身房">
      <component :is="currentCom" :gymId="gymId" @clickGym="goToCourse"></component>
    </el-tab-pane>
  </el-tabs>
</template>

<style scoped>

</style>