<script setup>

import {ref} from "vue";
import ReservationRecord from "../components/personal/ReservationRecord.vue";
import ChallengeRecord from "../components/personal/ChallengeRecord.vue";

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
    <el-tab-pane label="竞赛加入" name="challengeRecord">
      <component :is="ChallengeRecord"></component>
    </el-tab-pane>
  </el-tabs>

</template>

<style scoped>

</style>