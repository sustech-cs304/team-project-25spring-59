<script setup>

import {onMounted, reactive} from "vue";
import request from "../../utils/request.js";

defineEmits(['clickChallenge']);

const challenges = reactive({})

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

</script>

<template>
  <el-row>
    <el-col :span="12" :offset="6">
      <el-card shadow="hover" v-for="challenge in challenges.data" @click="$emit('clickChallenge', challenge.id)">
        <template #header>
          <el-row align="middle">
            <el-col :span="12">
              {{ challenge.title }} <el-tag type="primary">{{ challenge.challenge_type }}</el-tag>
            </el-col>
            <el-col :span="8" :offset="4">
              <div>
                开始：<el-text type="info" size="small">{{ challenge.start_date }}</el-text><br/>
                结束：<el-text type="info" size="small">{{ challenge.end_date }}</el-text>
              </div>
            </el-col>
          </el-row>
        </template>
        {{ challenge.description }}
        <template #footer>
          <el-row>
            <el-tag type="primary">{{ challenge.status }}</el-tag>
            <el-text>目标：{{ challenge.target_value }}</el-text>
          </el-row>

        </template>
      </el-card>
    </el-col>
  </el-row>
</template>

<style scoped>

</style>