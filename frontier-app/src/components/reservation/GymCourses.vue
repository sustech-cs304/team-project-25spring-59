<script setup>

import {onMounted, reactive} from "vue";
import request from "../../utils/request.js";

const props = defineProps(['gymId'])
const courseList = reactive({})

onMounted(()=>{
  request.get(`/course/getCourses/${props.gymId}`)
      .then((response) => {
        console.log(response);
        courseList.data = response.data;
      })
})

</script>

<template>
  <el-row>
    <el-col :span="18" :offset="3">
      <div class="block">
        <el-image
            style="width: 890px; height: 200px"
            :fit="'fill'">
        </el-image>
      </div>
      <el-skeleton :rows="3" animated/>
    </el-col>
    <el-col :span="16" :offset="4">
<!--      <el-card shadow="hover">-->
<!--        <div>-->
<!--          -->
<!--        </div>-->
<!--      </el-card>-->
      <el-table :data="courseList.data">
        <el-table-column>
          <div class="block">
            <el-image
                style="width: 50px; height: 50px"
                :fit="'fill'">
            </el-image>
          </div>
        </el-table-column>
        <el-table-column label="授课教师" prop="teacher.name"></el-table-column>
        <el-table-column label="课程名称" prop="name"></el-table-column>
        <el-table-column label="课程容量" prop="capacity"></el-table-column>
<!--        <el-table-column label="开课日期" prop="date"></el-table-column>-->
<!--        <el-table-column label="上课时间" prop="time"></el-table-column>-->
        <el-table-column label="操作" :fixed="'right'">
          <el-button type="primary">预定</el-button>
        </el-table-column>
      </el-table>
    </el-col>
  </el-row>
</template>

<style scoped>

.image-slot {
  width: 120px;

}

</style>