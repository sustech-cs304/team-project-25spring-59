<script setup>

import {onMounted, reactive} from "vue";
import request from "../utils/request.js";

const leaderboard = reactive({})

onMounted(()=>{
  request.get('/leaderboard')
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
        <el-table-column label="排名" prop="coachName"></el-table-column>
        <el-table-column label="昵称" prop="courseName"></el-table-column>
        <el-table-column label="积分" prop="capacity"></el-table-column>
        <!--        <el-table-column label="开课日期" prop="date"></el-table-column>-->
        <el-table-column label="上课时间" prop="startTime"></el-table-column>
        <el-table-column label="操作" :fixed="'right'">
          <el-button type="primary">预定</el-button>
        </el-table-column>
      </el-table>
    </el-col>
  </el-row>
</template>

<style scoped>

</style>