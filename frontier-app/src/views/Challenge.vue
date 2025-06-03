<script setup>
/**
 * @file ChallengeView.vue
 * @description 挑战任务视图，包含挑战列表、详情和创建功能
 */

import {ref} from "vue";
import TopMenu from "../components/TopMenu.vue";
import ChallengeList from "../components/challenge/ChallengeList.vue";
import ChallengeInfo from "../components/challenge/ChallengeInfo.vue";
import ChallengeCreate from "../components/challenge/ChallengeCreate.vue";

const userId = ref('')
const challengeId = ref('')
const currentCom = ref(ChallengeList)

function goToChallenge(id) {
  currentCom.value = ChallengeInfo;
  challengeId.value = id
  console.log(id)
}

function goToCreate() {
  currentCom.value = ChallengeCreate;
}

function goToList() {
  currentCom.value = ChallengeList;
}


defineExpose({
  /**
   * 当前用户ID
   * @member {string}
   * @description 可用于父组件设置或获取当前用户
   * @example
   * // 父组件中设置用户ID
   * challengeViewRef.value.userId = 'user123';
   */
  userId,

  /**
   * 当前查看的挑战ID
   * @member {string}
   * @description 当前正在查看的挑战任务ID
   * @example
   * // 父组件获取当前挑战ID
   * const currentId = challengeViewRef.value.challengeId;
   */
  challengeId,

  /**
   * 跳转到指定挑战详情
   * @function
   * @param {string} id - 挑战任务ID
   * @description 供父组件直接跳转到指定挑战详情页
   * @example
   * // 父组件跳转到挑战详情
   * challengeViewRef.value.goToChallenge('12345');
   */
  goToChallenge,

  /**
   * 刷新挑战列表
   * @function
   * @description 返回列表页并触发数据刷新
   * @example
   * // 父组件刷新列表
   * challengeViewRef.value.goToList();
   */
  goToList
});
</script>

<template>
  <TopMenu/>
  <component
      :is="currentCom"
      :challengeId="challengeId"
      @clickChallenge="goToChallenge"
      @createChallenge="goToCreate"
      @backToList="goToList"
  ></component>
</template>

<style scoped>

</style>