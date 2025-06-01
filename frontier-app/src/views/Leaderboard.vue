<script setup>
import {onMounted, reactive, watch} from "vue";
import request from "../utils/request.js";

const leaderboard = reactive({})
const userId = Number(localStorage.getItem('user_id'))

watch(
    leaderboard,
    async (newValue, oldValue) => {
      // sort the leaderboard by score from large to small
      newValue.data.sort((a, b) => b.total_score - a.total_score);
    }
)

onMounted(() => {
  request.post('/leaderboard')
      .then((response) => {
        console.log(response);
        leaderboard.data = response.data;
      })
})
</script>

<template>
  <div class="leaderboard-container">
    <el-row>
      <el-col :span="18" :offset="3">
        <el-card class="leaderboard-card">
          <template #header>
            <div class="card-header">
              <h2>排行榜</h2>
            </div>
          </template>
          <el-table
              :data="leaderboard.data"
              style="width: 100%"
              :row-class-name="({row}) => {
              if (row.user_id === userId) return 'current-user-row';
              return '';
            }"
          >
            <el-table-column label="排名" width="120">
              <template #default="{ $index }">
                <div class="rank-cell" :class="{
                  'first-rank': $index === 0,
                  'second-rank': $index === 1,
                  'third-rank': $index === 2
                }">
                  {{ $index + 1 }}
                </div>
              </template>
            </el-table-column>
            <el-table-column label="昵称" prop="username">
              <template #default="{ row }">
                <span :class="{'current-user': row.user_id === userId}">
                  {{ row.username }}
                  <el-tag v-if="row.user_id === userId" size="small" type="warning" class="user-tag">我</el-tag>
                </span>
              </template>
            </el-table-column>
            <el-table-column label="积分" prop="total_score">
              <template #default="{ row }">
                <span :class="{'current-user': row.user_id === userId}">
                  {{ row.total_score }}
                </span>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<style scoped>
/* 背景和容器样式 */
.leaderboard-container {
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  min-height: 100vh;
  padding: 20px 0;
}

.leaderboard-card {
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(5px);
  border: none;
}

.card-header {
  text-align: center;
  padding: 15px 0;
}

.card-header h2 {
  margin: 0;
  color: #2c3e50;
  font-size: 24px;
  font-weight: 600;
}

/* 排名样式 */
.rank-cell {
  font-size: 16px;
  font-weight: bold;
  text-align: center;
  padding: 8px;
  border-radius: 50%;
  width: 32px;
  height: 32px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  color: #606266;
}

.first-rank {
  background-color: #ffd700;
  color: #fff;
  transform: scale(1.2);
}

.second-rank {
  background-color: #c0c0c0;
  color: #fff;
  transform: scale(1.1);
}

.third-rank {
  background-color: #cd7f32;
  color: #fff;
}

/* 当前用户样式 */
.current-user {
  font-weight: bold;
  color: #409EFF;
}

.user-tag {
  margin-left: 8px;
}

/* 当前用户行样式 */
:deep(.current-user-row) {
  --el-table-tr-bg-color: #f0f9ff;
}

/* 鼠标悬停效果 */
:deep(.el-table__body tr:hover) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

/* 确保行内容不会被阴影遮挡 */
:deep(.el-table) {
  overflow: visible;
  background: transparent;
}

:deep(.el-table__body-wrapper) {
  overflow: visible;
}

:deep(.el-table__body tr) {
  transition: all 0.3s ease;
  position: relative;
  z-index: 1;
  background: rgba(255, 255, 255, 0.7);
}

/* 悬停时提高z-index，确保阴影显示完整 */
:deep(.el-table__body tr:hover) {
  z-index: 2;
  background: white;
}

/* 表头样式 */
:deep(.el-table__header) {
  background: rgba(255, 255, 255, 0.7);
}
</style>