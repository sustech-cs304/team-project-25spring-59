<script setup>

import {onMounted, reactive, ref} from "vue";
import request from "../../utils/request.js";
import {ElMessage} from "element-plus";

const userId = localStorage.getItem('user_id')
const personalCourses = reactive({})

// sort the reservation records by reservation time from large to small
function processData(data) {
  personalCourses.data = data;
  personalCourses.data.sort((a, b)=>new Date(b.reservationTime) - new Date(a.reservationTime))
}

function denyReservation(courseId) {
  console.log(courseId)
  request({
    method: "POST",
    url: '/gym/cancelCourseReservation',
    data: {
      userId: userId,
      courseId: courseId,
    }
  }).then((response)=>{
    console.log(response)
    ElMessage({message: '已取消课程', type: 'success',})
    window.location.reload()
  }).catch((error)=>{
    console.log(error)
  })
}

onMounted(()=>{
  request.get(`/course/getReservedCourses/${userId}`)
      .then((response) => {
        console.log(response);
        personalCourses.data = response.data;
      })
      .catch((error) => {
        console.log(error)
      })
})

</script>

<template>
  <el-row>
    <el-col :span="12" :offset="6">
      <el-table :data="personalCourses.data">
        <el-table-column label="授课教师" prop="coachName"></el-table-column>
        <el-table-column label="课程名称" prop="courseName"></el-table-column>
        <el-table-column label="上课时间" prop="startTime"></el-table-column>
        <el-table-column label="操作" :fixed="'right'">
          <template #default="scope">
            <el-button type="danger" @click="denyReservation(scope.row.courseId)">取消预定</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-col>
  </el-row>
</template>

<style scoped>

</style>