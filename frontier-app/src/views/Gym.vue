<script setup>
/**
 * 健身房预约页面组件，处理健身房列表和课程选择
 */
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

// 用于文档生成的组件定义

defineExpose({
  /**
   * 当前健身房ID
   * @type {string}
   */
  gymId,
  /**
   * 当前健身房名称
   * @type {string}
   */
  gymName,
  /**
   * 当前显示的组件
   * @type {Component}
   */
  currentCom,
  /**
   * 跳转到课程页面的方法
   * @method
   * @param {string} id - 所选健身房的ID
   * @param {string} name - 所选健身房的名称
   */
  goToCourse
});
</script>

<template>
  <TopMenu/>

  <component :is="currentCom" :gymId="gymId" :gymName="gymName" @clickGym="goToCourse"></component>
</template>

<style scoped>

</style>