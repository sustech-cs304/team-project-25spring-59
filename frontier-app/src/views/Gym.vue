<script setup>

import {ref} from "vue";
import {useRouter, useRoute} from "vue-router";
import GymList from "../components/reservation/GymList.vue";
import GymCourses from "../components/reservation/GymCourses.vue";
import TopMenu from "../components/TopMenu.vue";

const router = useRouter();
const gymId = ref('')
const gymName = ref('')
const currentCom = ref(GymList)

function goToCourse(id, name) {
  currentCom.value = GymCourses;
  gymId.value = id
  gymName.value = name
  console.log(id, name)
}


</script>

<template>
  <TopMenu/>

  <component :is="currentCom" :gymId="gymId" :gymName="gymName" @clickGym="goToCourse"></component>
</template>

<style scoped>

</style>