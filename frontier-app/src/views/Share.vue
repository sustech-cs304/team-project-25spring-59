<script setup>

import {ref} from "vue";
import ShareList from "../components/share/ShareList.vue";
import ShareCreate from "../components/share/ShareCreate.vue";

const userId = ref('')
const challengeId = ref('')
const currentCom = ref(ShareList)


function goToCreate() {
  currentCom.value = ShareCreate;
}

function goToList() {
  currentCom.value = ShareList;
}

</script>

<template>
  <component
      :is="currentCom"
      @createShare="goToCreate"
      @backToList="goToList"
  ></component>

</template>

<style scoped>
.sharing-container {

}

</style>