<script setup>

import {onMounted, reactive, ref, watch} from "vue";
import {ArrowLeftBold, ArrowRightBold} from "@element-plus/icons-vue";
import request from "../../utils/request.js";
import {getFullDate} from "../../utils/date.js";

const props = defineProps(['gymId'])
const courses = reactive({})
const groupByDate = reactive({})
const dates = reactive({})
const dateList = [
    new Date("2003-02-01 08:00:00"),
    new Date("2003-02-12 09:30:00"),
    new Date("2003-02-03 07:30:00"),
    new Date("2003-02-07 08:30:00"),
    new Date("2003-03-01 09:00:00"),
].sort((a,b)=>a-b)  // sorted from small to large
const index = ref(0)
const range = ref(5)
const dateSlice = (start, end) => dateList.slice(start, end)  // export date slice

function dateslice(dateList, start, end) {
  if(end > dateList.length) {
    return dateList.slice(start)
  }
  return dateList.slice(start, end)
}

function processCourses(coursesData) {
  coursesData.forEach((courseInfo)=>{
    courseInfo.date = courseInfo.startTime.slice(0, 10)
  });
  groupByDate.data = Object.groupBy(coursesData, ({ date }) => date);
  for (const key in groupByDate.data) {
    // sorted date from small to large
    groupByDate.data[key].sort((a, b)=>new Date(a.startTime) - new Date(b.startTime))
  }
  console.log(groupByDate.data)
  dates.data = Object.keys(groupByDate.data)
  console.log(dates.data)


  coursesData.sort((a, b)=>{
    let date_a = new Date(a.date), date_b = new Date(b.date);
    if(date_a === date_b) {
      return new Date(a.startTime) - new Date(b.startTime)
    }
    return date_a - date_b
  });
  return coursesData;
}


onMounted(()=>{
  request.get(`/gym/getCourses/${props.gymId}`)
      .then((response) => {
        console.log(response);
        courses.data = processCourses(response.data);
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
          <el-col :span="4" v-for="date in dates.data"><!--dateList-->
            <el-card shadow="hover">
              {{getFullDate(date).month}}月{{getFullDate(date).day}}日/星期{{getFullDate(date).week}}
            </el-card>
          </el-col>
          <el-col :span="1"><!--right button-->
            <el-button :icon="ArrowRightBold" circle @click="()=>index+range>=dateList.length ? index : index+=range"/>
          </el-col>
        </el-row>
      </div>
    </el-col>
  </el-row>
  <el-row>
    <el-col :span="16" :offset="4">
      <el-table :data="courses.data">
        <el-table-column>
          <div class="block">
            <el-image
                style="width: 50px; height: 50px"
                :fit="'fill'">
            </el-image>
          </div>
        </el-table-column>
        <el-table-column label="授课教师" prop="coachName"></el-table-column>
        <el-table-column label="课程名称" prop="courseName"></el-table-column>
        <el-table-column label="课程容量" prop="capacity"></el-table-column>
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

.image-slot {
  width: 120px;

}

</style>