<script setup>

import {ref} from "vue";
import JoinedChallenge from "./JoinedChallenge.vue";
import ChallengeInfo from "../../components/challenge/ChallengeInfo.vue";

const userId = ref('')
const challengeId = ref('')
const currentCom = ref(JoinedChallenge)

function goToChallenge(id) {
  currentCom.value = ChallengeInfo;
  challengeId.value = id
  console.log(id)
}

function goToList() {
  currentCom.value = JoinedChallenge;
}

defineExpose({
  /**
   * 当前用户ID
   * @type {import("vue").Ref<string>}
   */
  userId,

  /**
   * 当前挑战ID
   * @type {import("vue").Ref<string>}
   */
  challengeId,

  /**
   * 跳转到指定挑战详情
   * @function
   * @param {string} id - 挑战ID
   */
  goToChallenge,

  /**
   * 返回挑战列表
   * @function
   */
  goToList
});
</script>

<template>
  <component
      :is="currentCom"
      :challengeId="challengeId"
      @clickChallenge="goToChallenge"
      @backToList="goToList"
  ></component>
</template>

<style scoped>

</style>