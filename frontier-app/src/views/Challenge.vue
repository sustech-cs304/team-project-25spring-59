<script setup>

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