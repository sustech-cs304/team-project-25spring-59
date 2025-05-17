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