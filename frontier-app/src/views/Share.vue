<script setup>

import {ref} from "vue";
import TopMenu from "../components/TopMenu.vue";
import ShareList from "../components/share/ShareList.vue";
import ShareCreate from "../components/share/ShareCreate.vue";
import {Top} from "@element-plus/icons-vue";

const userId = ref('')
const challengeId = ref('')
const currentCom = ref(ShareList)


function goToCreate() {
  currentCom.value = ShareCreate;
}

function goToList() {
  currentCom.value = ShareList;
}

/**
 * 分享功能组件暴露的API
 */
defineExpose({
  /**
   * 当前用户ID
   * @member {import('vue').Ref<string>}
   */
  userId,

  /**
   * 当前挑战ID
   * @member {import('vue').Ref<string>}
   */
  challengeId,

  /**
   * 当前显示的组件
   * @member {import('vue').Ref<Component>}
   * @description 控制显示 ShareList 或 ShareCreate 组件
   */
  currentCom,

  /**
   * 跳转到创建分享页面
   * @function
   */
  goToCreate,

  /**
   * 返回分享列表页面
   * @function
   */
  goToList
});
</script>

<template>
  <TopMenu/>
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