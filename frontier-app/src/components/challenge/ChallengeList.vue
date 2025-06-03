<script setup>

import {onMounted, reactive, watch} from "vue";
import request from "../../utils/request.js";
import {Plus} from "@element-plus/icons-vue";

defineEmits(['clickChallenge', 'createChallenge']);

const challenges = reactive({})

watch(
    challenges,
    async (newValue, oldValue)=>{
      // sort the sharings by time from large to small
      newValue.data.sort((a,b)=>new Date(b.start_date) - new Date(a.start_date));
    }
)

onMounted(()=>{
  request.get('/challenges/all')
      .then((response) => {
        console.log(response);
        challenges.data = response.data.challenges
      })
      .catch((error) => {
        console.log(error)
      })
})

defineExpose({
  /**
   * 所有挑战数据
   * @type {import('vue').Reactive<{data: Array}>}
   */
  challenges,
})
</script>

<template>
  <el-row class="challenge-container">
    <el-col :span="12" :offset="6">
      <el-card
          shadow="hover"
          v-for="challenge in challenges.data"
          @click="$emit('clickChallenge', challenge.id)">
        <el-row align="middle">
          <el-col :span="12">
            <el-row>
              {{ challenge.title }}
            </el-row>
            <el-row>
              <el-col :span="8">
                <el-tag type="primary">{{ challenge.challenge_type }}</el-tag>
              </el-col>
              <el-col :span="8">
                <el-tag type="primary">{{ challenge.status }}</el-tag>
              </el-col>
            </el-row>
          </el-col>
          <el-col :span="8" :offset="4">
            <div>
              开始：<el-text type="info" size="small">{{ challenge.start_date }}</el-text><br/>
              结束：<el-text type="info" size="small">{{ challenge.end_date }}</el-text>
            </div>
          </el-col>
        </el-row>
      </el-card>
    </el-col>
  </el-row>

  <!--fixed navigating bar at the bottom-->
  <el-affix target=".challenge-container" position="bottom" :offset="20">
    <el-row>
      <el-col :span="10" :offset="7">
        <div style="display: flex; justify-content: center">
          <el-button :icon="Plus" type="primary" size="large" circle @click="$emit('createChallenge')"></el-button>
        </div>
      </el-col>
    </el-row>
  </el-affix>
</template>

<style scoped>

</style>