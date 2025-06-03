<script setup>

import {onMounted, reactive, watch} from "vue";
import request from "../../utils/request.js";

/**
 * 定义组件事件
 * @event clickChallenge - 点击挑战事件
 * @event createChallenge - 创建挑战事件
 */
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
  request({
    method: 'POST',
    url: '/challenges/my',
    data: {user_id: localStorage.getItem('user_id')}
  })
      .then((response) => {
        console.log(response);
        challenges.data = response.data
      })
      .catch((error) => {
        console.log(error)
      })
})

defineExpose({
  /**
   * 挑战列表数据
   * @type {import("vue").Reactive<Object>}
   */
  challenges,
});
</script>

<template>
  <el-row class="challenge-container">
    <el-col :span="12" :offset="6">
      <el-card shadow="never" v-for="challenge in challenges.data">
        <el-row align="top" justify="space-between">
          <el-col :span="6">
            <el-row>
              {{ challenge.title }}
            </el-row>
            <el-tag type="primary">{{ challenge.challenge_type }}</el-tag>
          </el-col>
          <el-col :span="9">
            <div>
              开始：<el-text type="info" size="small">{{ challenge.start_date }}</el-text><br/>
              结束：<el-text type="info" size="small">{{ challenge.end_date }}</el-text>
            </div>
          </el-col>
          <el-col :span="3">
            <el-button
                link
                type="primary"
                @click="$emit('clickChallenge', challenge.id)"
            >查看详情</el-button>
          </el-col>
        </el-row>
      </el-card>
    </el-col>
  </el-row>
</template>

<style scoped>

</style>