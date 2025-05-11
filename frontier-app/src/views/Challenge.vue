<script setup>

import {ref} from "vue";
import ChallengeList from "../components/challenge/ChallengeList.vue";
import ChallengeInfo from "../components/challenge/ChallengeInfo.vue";

const challengeId = ref('')
const currentCom = ref(ChallengeList)

function goToChallenge(id) {
  currentCom.value = ChallengeInfo;
  challengeId.value = id
}

</script>

<template>
  <component :is="currentCom" :challengeId="challengeId" @clickChallenge="goToChallenge"></component>
</template>

<style scoped>

</style>