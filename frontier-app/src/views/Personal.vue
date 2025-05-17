<script setup>

import {ref} from "vue";
import ReservationRecord from "../components/personal/ReservationRecord.vue";


const activeName = ref('reservationRecord')

</script>

<template>
  <el-tabs
      tab-position="left"
      v-model="activeName"
  >
    <el-tab-pane label="课程预约" name="reservationRecord">
      <component :is="ReservationRecord"></component>
    </el-tab-pane>
  </el-tabs>

</template>

<style scoped>

</style>