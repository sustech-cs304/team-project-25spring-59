<script setup>

import {onMounted, reactive, computed} from "vue";
import request from "../../utils/request.js";

const emit = defineEmits(['clickGym']);

const state = reactive({
  allGyms: [],
  currentPage: 1,
  pageSize: 5,
  searchTime: null
});


const convertTimeToSeconds = (timeStr) => {
  if (!timeStr) return 0;
  const parts = timeStr.split(':');
  if (parts.length !== 3) return 0;

  const [hours, minutes, seconds] = parts.map(Number);
  return hours * 3600 + minutes * 60 + seconds;
};

const filteredGyms = computed(() => {
  if (!state.searchTime) return state.allGyms;

  const searchSeconds = convertTimeToSeconds(state.searchTime);
  if (searchSeconds === 0) return state.allGyms;

  return state.allGyms.filter(gym => {
    if (!gym.openTime) return false;

    const [gymOpenTime, gymCloseTime] = gym.openTime.split('-');
    const gymOpenSeconds = convertTimeToSeconds(gymOpenTime);
    const gymCloseSeconds = convertTimeToSeconds(gymCloseTime);

    // 检查搜索时间是否在健身房开放时间段内
    return searchSeconds >= gymOpenSeconds && searchSeconds <= gymCloseSeconds;
  });
});

const paginatedGyms = computed(() => {
  const start = (state.currentPage - 1) * state.pageSize;
  const end = start + state.pageSize;
  return filteredGyms.value.slice(start, end);
});

const totalGyms = computed(() => filteredGyms.value.length);

onMounted(()=>{
  request.get('/gym/getGyms')
      .then((response) => {
        console.log(response);
        state.allGyms = response.data;
      })
      .catch((error) => {
        console.error("获取健身房数据失败:", error);
      })
})

const handleCurrentChange = (page) => {
  state.currentPage = page;
};

const handleReset = () => {
  state.searchTime = null;
  state.currentPage = 1;
};

</script>

<template>
  <div class="gym-background">
    <div class="overlay">
      <el-row>
        <el-col :span="16" :offset="4">
          <div class="search-container">
            <el-time-picker
                v-model="state.searchTime"
                placeholder="选择查询时间"
                format="HH:mm:ss"
                value-format="HH:mm:ss"
                :clearable="true"
                style="width: 180px; margin-right: 10px;"
            />
            <el-button @click="handleReset">重置</el-button>
          </div>

          <template v-if="filteredGyms.length > 0">
            <el-card
                v-for="gym in paginatedGyms"
                :key="gym.id"
                class="gym-card"
                shadow="hover"
            >
              <div @click="emit('clickGym', gym.id, gym.name)" class="gym-content">
                <span class="gym-name">{{ gym.name }}</span>
                <div class="bottom">
                  <span>开放时间：{{ gym.openTime }}</span><br/>
                  <span>地址：{{ gym.address }}</span>
                </div>
              </div>
            </el-card>

            <div class="pagination-container">
              <el-pagination
                  @current-change="handleCurrentChange"
                  :current-page="state.currentPage"
                  :page-size="state.pageSize"
                  layout="prev, pager, next, jumper"
                  :total="totalGyms"
                  background
              />
            </div>
          </template>

          <div v-else class="no-data">
            <el-empty :description="state.searchTime ? '没有找到此时段开放的健身房' : '暂无健身房数据'" />
          </div>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<style scoped>

.gym-background {
  background-image: url('https://images.unsplash.com/photo-1571902943202-507ec2618e8f?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80');
  background-size: cover;
  background-position: center;
  background-attachment: fixed;
  min-height: 100vh;
  padding: 20px 0;
}

.overlay {
  background-color: rgba(255, 255, 255, 0.9);
  border-radius: 8px;
  padding: 20px;
}

.search-container {
  margin-bottom: 20px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.gym-card {
  margin-bottom: 15px;
  cursor: pointer;
  transition: transform 0.3s;
}

.gym-card:hover {
  transform: translateY(-5px);
}

.gym-content {
  padding: 10px;
}

.gym-name {
  font-weight: bold;
  font-size: 18px;
}

.bottom {
  margin-top: 10px;
  border-top: 1px solid darkgrey;
  padding-top: 10px;
  font-size: 12px;
  color: #666;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

.no-data {
  margin-top: 50px;
  text-align: center;
}
</style>