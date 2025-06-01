<script setup>

import {onMounted, reactive, ref} from "vue";
import {ArrowLeftBold, ArrowRightBold} from "@element-plus/icons-vue";
import request from "../../utils/request.js";
import {getFullDate} from "../../utils/date.js";
import {ElMessage} from "element-plus";

const userId = localStorage.getItem('user_id')
const props = defineProps(['gymId', 'gymName'])
const groupByDate = reactive({})
const dateList = reactive({})
const currentCourses = reactive({data: []})
const personalCourses = reactive([])

const index = ref(0)
const range = ref(5)
const isLoading = ref(true);

const isReserved = ((courseId)=>{
  return personalCourses.indexOf(courseId) !== -1;
})

function processCourses(coursesData) {
  coursesData.forEach((courseInfo)=>{
    courseInfo.date = courseInfo.startTime.slice(0, 10) // separate 'date' info
    courseInfo.remain = courseInfo.capacity - courseInfo.currentReservations;
    courseInfo.startTimeFormatted = formatTime(courseInfo.startTime);
    courseInfo.endTimeFormatted = formatTime(courseInfo.endTime);
  });

  groupByDate.data = Object.groupBy(coursesData, ({ date }) => date);
  // sort the courses by startTime on each date
  for (const key in groupByDate.data) {
    groupByDate.data[key].sort((a, b)=>new Date(a.startTime) - new Date(b.startTime));
  }

  dateList.data = Object.keys(groupByDate.data);
  if(dateList.data.length > 0) {
    dateList.data.sort((a, b)=>new Date(a) - new Date(b))
    currentCourses.data = groupByDate.data[dateList.data[0]];  // initialize the current courses display
  }
  console.log(groupByDate.data);
  console.log(dateList.data);
  console.log(currentCourses.data);
}

function formatTime(timeString) {
  if (!timeString) return '';
  const date = new Date(timeString);
  return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

function getPersonalCourses(data) {
  data.forEach((course)=>{
    personalCourses.push(course.courseId);
  })
}

function reserveCourse(courseId) {
  console.log(localStorage)
  request({
    method: "POST",
    url: '/gym/reserveCourse',
    data: {
      userId: localStorage.getItem('user_id'),
      courseId: courseId,
    }
  }).then((response)=>{
    console.log(response)
    ElMessage({message: '预定成功', type: 'success',})
    personalCourses.push(courseId);
    // update the status
    currentCourses.data.forEach(course => {
      if (course.id === courseId) {
        course.currentReservations += 1;
        course.remain = course.capacity - course.currentReservations;
      }
    });
  }).catch((error)=>{
    console.log(error)
    ElMessage({ message: '预约失败: ' + (error.response?.data?.message || error.message), type: 'error' });
  })
}

onMounted(()=>{
  isLoading.value = true;

  Promise.all([
    // get all courses from the gymId
    request.get(`/gym/getCourses/${props.gymId}`),
    // get all courses that the user reserved
    request.get(`/course/getReservedCourses/${userId}`)
  ]).then(([coursesResponse, reservedResponse]) => {
    processCourses(coursesResponse.data);
    getPersonalCourses(reservedResponse.data);
  }).catch((error) => {
    console.error("加载数据失败:", error);
    ElMessage({ message: '加载课程数据失败', type: 'error' });
  }).finally(() => {
    isLoading.value = false;
  });
})

function handleDateClick(date) {
  currentCourses.data = groupByDate.data[date];
}

function handlePrevClick() {
  if (index.value > 0) {
    index.value = Math.max(0, index.value - range.value);
  }
}

function handleNextClick() {
  if (index.value + range.value < dateList.data?.length) {
    index.value += range.value;
  }
}

</script>

<template>
  <div class="gym-courses-background">
    <div class="overlay">
      <div class="container">
        <div class="header-container">
          <h1 class="page-title">{{ gymName }}</h1>
        </div>

        <el-skeleton :rows="5" animated v-if="isLoading" />

        <template v-else>
          <div class="date-navigator">
            <el-button
                :icon="ArrowLeftBold"
                circle
                @click="handlePrevClick"
                :disabled="index <= 0"
            />

            <div class="date-cards-container">
              <el-card
                  v-for="date in dateList.data?.slice(index, index + range)"
                  :key="date"
                  shadow="hover"
                  class="date-card"
                  :class="{ 'active-date': currentCourses.data === groupByDate.data[date] }"
                  @click="() => handleDateClick(date)"
              >
                <div class="date-content">
                  <div class="date-month-day">
                    {{ getFullDate(new Date(date)).month }}月{{ getFullDate(new Date(date)).day }}日
                  </div>
                  <div class="date-week">
                    星期{{ getFullDate(new Date(date)).week }}
                  </div>
                </div>
              </el-card>
            </div>

            <el-button
                :icon="ArrowRightBold"
                circle
                @click="handleNextClick"
                :disabled="index + range >= dateList.data?.length"
            />
          </div>

          <div class="table-wrapper">
            <el-table
                :data="currentCourses.data"
                stripe
                v-if="currentCourses.data?.length > 0"
                class="wide-table"
            >
              <el-table-column
                  label="授课教师"
                  prop="coachName"
                  align="center"
                  width="180">
              </el-table-column>
              <el-table-column
                  label="课程名称"
                  prop="courseName"
                  align="center"
                  width="220">
              </el-table-column>
              <el-table-column
                  label="时间"
                  align="center"
                  width="260">
                <template #default="scope">
                  {{ scope.row.startTimeFormatted }} - {{ scope.row.endTimeFormatted }}
                </template>
              </el-table-column>
              <el-table-column
                  label="容量"
                  align="center"
                  width="160">
                <template #default="scope">
                  <el-tag :type="scope.row.remain > 0 ? 'success' : 'danger'">
                    {{ scope.row.remain }}/{{ scope.row.capacity }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column
                  label="操作"
                  align="center"
                  width="180">
                <template #default="scope">
                  <el-button
                      v-if="isReserved(scope.row.id)"
                      type="info"
                      disabled
                      size="small"
                  >已预定</el-button>
                  <el-button
                      v-else-if="scope.row.remain > 0"
                      type="primary"
                      size="small"
                      @click="reserveCourse(scope.row.id)"
                  >预定</el-button>
                  <el-button
                      v-else
                      type="danger"
                      disabled
                      size="small"
                  >已满</el-button>
                </template>
              </el-table-column>
            </el-table>

            <el-empty v-else description="暂无课程数据" />
          </div>
        </template>
      </div>
    </div>
  </div>
<!--  <el-row>-->
<!--    <el-col :span="18" :offset="3">-->
<!--      <div style="display: flex; justify-content: center">-->
<!--        <el-image-->
<!--            style="width: 1000px; height: 200px;"-->
<!--            :fit="'fill'">-->
<!--        </el-image>-->
<!--      </div>-->
<!--      <el-skeleton :rows="3" animated/>-->
<!--      <div>-->
<!--        <el-row align="middle" justify="space-between">-->
<!--          <el-col :span="1" style="display: flex; flex-direction: row-reverse">&lt;!&ndash;left button&ndash;&gt;-->
<!--            <el-button :icon="ArrowLeftBold" circle @click="()=>index<=0 ? index=0 : index-=5"/>-->
<!--          </el-col>-->
<!--          <el-col :span="4" v-for="date in dateList.data">&lt;!&ndash;dateList&ndash;&gt;-->
<!--            <el-card shadow="hover" @click="()=>currentCourses.data = groupByDate.data[date]">-->
<!--              {{getFullDate(new Date(date)).month}}月{{getFullDate(new Date(date)).day}}日/星期{{getFullDate(new Date(date)).week}}-->
<!--            </el-card>-->
<!--          </el-col>-->
<!--          <el-col :span="1">&lt;!&ndash;right button&ndash;&gt;-->
<!--            <el-button :icon="ArrowRightBold" circle @click="()=>index+range>=dateList.length ? index : index+=range"/>-->
<!--          </el-col>-->
<!--        </el-row>-->
<!--      </div>-->
<!--    </el-col>-->
<!--  </el-row>-->
<!--  <el-row>-->
<!--    <el-col :span="16" :offset="4">-->
<!--      <el-table :data="currentCourses.data">-->
<!--        <el-table-column>-->
<!--          <div class="block">-->
<!--            <el-image-->
<!--                style="width: 50px; height: 50px"-->
<!--                :fit="'fill'">-->
<!--            </el-image>-->
<!--          </div>-->
<!--        </el-table-column>-->
<!--        <el-table-column label="授课教师" prop="coachName"></el-table-column>-->
<!--        <el-table-column label="课程名称" prop="courseName"></el-table-column>-->
<!--        <el-table-column label="课程容量" prop="capacity"></el-table-column>-->
<!--        <el-table-column label="剩余" prop="remain"></el-table-column>-->
<!--        <el-table-column label="上课时间" prop="startTime"></el-table-column>-->
<!--        <el-table-column label="操作" :fixed="'right'">-->
<!--          <template #default="scope">-->
<!--            <el-button-->
<!--                v-if="isReserved(scope.row.id)"-->
<!--                type="info"-->
<!--                disabled-->
<!--                @click="reserveCourse(scope.row.id)"-->
<!--            >已预定</el-button>-->
<!--            <el-button-->
<!--                v-else-->
<!--                type="primary"-->
<!--                @click="reserveCourse(scope.row.id)"-->
<!--            >预定</el-button>-->
<!--          </template>-->
<!--        </el-table-column>-->
<!--      </el-table>-->
<!--    </el-col>-->
<!--  </el-row>-->
</template>

<style scoped>
.gym-courses-background {
  background-image: url('https://images.unsplash.com/photo-1571902943202-507ec2618e8f?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80');
  background-size: cover;
  background-position: center;
  background-attachment: fixed;
  min-height: 100vh;
  padding: 20px;
  display: flex;
  justify-content: center;
}

.overlay {
  background-color: rgba(255, 255, 255, 0.95);
  border-radius: 8px;
  padding: 30px 40px;
  width: 100%;
  max-width: 1400px;
}

.container {
  width: 100%;
  margin: 0 auto;
}

.header-container {
  text-align: center;
  margin-bottom: 30px;
}

.page-title {
  color: #333;
  font-size: 28px;
  margin-bottom: 10px;
}

.date-navigator {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 30px;
  gap: 15px;
}

.date-cards-container {
  display: flex;
  gap: 15px;
  overflow-x: auto;
  padding: 10px 0;
  flex-grow: 1;
  justify-content: center;
}

.date-card {
  width: 120px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.date-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.active-date {
  border: 2px solid var(--el-color-primary);
  background-color: rgba(64, 158, 255, 0.1);
}

.date-content {
  text-align: center;
  padding: 10px;
}

.date-month-day {
  font-size: 16px;
  font-weight: bold;
  margin-bottom: 5px;
}

.date-week {
  font-size: 14px;
  color: #666;
}

.table-wrapper {
  display: flex;
  justify-content: center;
  width: 100%;
}

.wide-table {
  width: 100%;
  margin: 0 auto;
}

.el-table {
  border-radius: 8px;
  overflow: hidden;
}

.el-table :deep(th) {
  background-color: #f5f7fa;
  font-weight: bold;
  text-align: center;
}

.el-table :deep(td) {
  text-align: center;
  padding: 12px 0;
}

.el-table :deep(.el-table__body-wrapper) {
  width: 100% !important;
}
</style>