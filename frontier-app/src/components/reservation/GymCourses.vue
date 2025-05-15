<script setup>

import {onMounted, reactive, ref, watch} from "vue";
import {ArrowLeftBold, ArrowRightBold} from "@element-plus/icons-vue";
import request from "../../utils/request.js";
import {getFullDate} from "../../utils/date.js";

const props = defineProps(['gymId'])
const groupByDate = reactive({})
const dateList = reactive({})
const currentCourses = reactive({data: []})

const index = ref(0)
const range = ref(5)

function processCourses(coursesData) {
  coursesData.forEach((courseInfo)=>{
    courseInfo.date = courseInfo.startTime.slice(0, 10) // separate 'date' info
    courseInfo.remain = courseInfo.capacity - courseInfo.currentReservations;
  });

  groupByDate.data = Object.groupBy(coursesData, ({ date }) => date);
  // sort the courses by startTime on each date
  for (const key in groupByDate.data) {
    groupByDate.data[key].sort((a, b)=>new Date(a.startTime) - new Date(b.startTime));
  }

  dateList.data = Object.keys(groupByDate.data);
  if(dateList.data.length > 0) {
    currentCourses.data = groupByDate.data[dateList.data[0]];  // initialize the current courses display
  }
  console.log(groupByDate.data);
  console.log(dateList.data);
  console.log(currentCourses.data);
}


onMounted(()=>{
  request.get(`/gym/getCourses/${props.gymId}`)
      .then((response) => {
        console.log(response);
        processCourses(response.data);
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
          <el-col :span="4" v-for="date in dateList.data"><!--dateList-->
            <el-card shadow="hover" @click="()=>currentCourses.data = groupByDate.data[date]">
              {{getFullDate(new Date(date)).month}}月{{getFullDate(new Date(date)).day}}日/星期{{getFullDate(new Date(date)).week}}
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
      <el-table :data="currentCourses.data">
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
        <el-table-column label="剩余" prop="remain"></el-table-column>
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