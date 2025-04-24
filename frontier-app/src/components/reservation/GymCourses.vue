<script setup>

import {onMounted, reactive, ref} from "vue";
import {ArrowLeftBold, ArrowRightBold} from "@element-plus/icons-vue";
import request from "../../utils/request.js";
import {getFullDate} from "../../utils/date.js";

const props = defineProps(['gymId'])
const courseList = reactive({})
const dateList = [
    new Date("2003-02-01 08:00:00"),
    new Date("2003-02-12 09:30:00"),
    new Date("2003-02-03 07:30:00"),
    new Date("2003-02-07 08:30:00"),
    new Date("2003-03-01 09:00:00"),
].sort((a,b)=>a-b)
const index = ref(0)
const dateListShow = (start, end) => dateList.slice(start, end)  // export date slice

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
      <div style="display: flex; justify-content: center">
        <el-image
            style="width: 1000px; height: 200px;"
            :fit="'fill'">
        </el-image>
      </div>
      <el-skeleton :rows="3" animated/>
      <div>
        <el-row align="middle" justify="space-between">
          <el-col :span="1" style="display: flex; flex-direction: row-reverse"><!--left button-->
            <el-button :icon="ArrowLeftBold" circle @click="()=>index<=0 ? index=0 : index-=5"/>
          </el-col>
          <el-col :span="4" v-for="date in dateListShow(index, index+5)"><!--dateList-->
            <el-card shadow="hover">{{getFullDate(date).month}}月{{getFullDate(date).day}}日/星期{{getFullDate(date).week}}</el-card>
          </el-col>
          <el-col :span="1"><!--right button-->
            <el-button :icon="ArrowRightBold" circle @click="()=>index+5>=dateList.length ? index : index+=5"/>
          </el-col>
        </el-row>
      </div>
    </el-col>
  </el-row>
  <el-row>
    <el-col :span="16" :offset="4">
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