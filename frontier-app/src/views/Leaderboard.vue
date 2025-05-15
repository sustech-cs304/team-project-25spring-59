<script setup>

import {onMounted, reactive, watch} from "vue";
import request from "../utils/request.js";

const leaderboard = reactive({})

watch(
    leaderboard,
    async (newValue, oldValue)=>{
      // sort the leaderboard by score from large to small
      newValue.data.sort((a,b)=>b.total_score - a.total_score);
    }
)

onMounted(()=>{
  request.post('/leaderboard')
      .then((response)=>{
        console.log(response);
        leaderboard.data = response.data;
      })
})

</script>

<template>
  <el-row>
    <el-col :span="12" :offset="6">
      <el-table :data="leaderboard.data">
        <el-table-column label="排名" type="index" width="150"></el-table-column>
        <el-table-column label="昵称" prop="username"></el-table-column>
        <el-table-column label="积分" prop="total_score"></el-table-column>
      </el-table>
    </el-col>
  </el-row>
</template>

<style scoped>

</style>