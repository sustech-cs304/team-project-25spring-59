<script setup>

import {ref} from "vue";
import TopMenu from "../components/TopMenu.vue";
import ReservationRecord from "../components/personal/ReservationRecord.vue";
import ChallengeRecord from "../components/personal/ChallengeRecord.vue";

const activeName = ref('reservationRecord')

defineExpose({
  /**
   * 当前激活的标签页名称
   * @member {import('vue').Ref<string>}
   * @description 控制显示'reservationRecord'(预约记录)或'challengeRecord'(挑战记录)
   * @default 'reservationRecord'
   */
  activeName,

  /**
   * 预约记录组件实例
   * @member {import('vue').Component}
   */
  ReservationRecord,

  /**
   * 挑战记录组件实例
   * @member {import('vue').Component}
   */
  ChallengeRecord
});
</script>

<template>
  <TopMenu/>
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