<script setup>

import {onMounted, reactive, ref, watch} from "vue";
import request from "../../utils/request.js";

const userId = ref(1)
const personalCourses = reactive({})

// sort the reservation records by reservation time from large to small
watch(
    personalCourses,
    async (newValue, oldValue)=>{
      newValue.data.sort((a, b)=>new Date(b.reservationTime) - new Date(a.reservationTime))
    }
)

function denyReservation(courseId, gymId) {
  console.log(courseId, gymId)
  request({
    method: "POST",
    url: '/gym/denyReservation',
    data: {
      userId: userId,
      courseId: courseId,
      gymId: gymId,
    }
  }).then((response)=>{
    console.log(response)
  }).catch((error)=>{
    console.log(error)
  })
}

onMounted(()=>{
  request.get(`/gym/getPersonalCourses/${userId}`)
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
            <el-button
                type="danger"
                @click="denyReservation(scope.row.courseId, scope.row.gymId)"
            >取消预定</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-col>
  </el-row>
</template>

<style scoped>

</style>