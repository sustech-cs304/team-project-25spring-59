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

defineExpose({
  /**
   * 当前登录用户ID
   * @description 从localStorage中获取的用户唯一标识符
   * @member {string}
   */
  userId,

  /**
   * 用户预约的课程列表
   * @description 包含用户所有预约课程信息的响应式对象，数据已按预约时间排序
   * @member {import("vue").Reactive<{data?: Array<{
   *   id: number,
   *   courseName: string,
   *   reservationTime: string,
   *   status: string,
   *   coach: string,
   *   location: string
   * }>}>}
   */
  personalCourses,

  /**
   * 处理课程数据的方法
   * @description 对获取的课程数据进行处理并按预约时间从新到旧排序
   * @function
   * @param {Array} data - 从API获取的原始课程数据
   * @returns {void}
   */
  processData,

  /**
   * 取消课程预约的方法
   * @description 向服务器发送请求取消指定课程预约，成功后刷新页面
   * @function
   * @param {number} courseId - 要取消的课程ID
   * @returns {Promise<void>}
   */
  denyReservation
});
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