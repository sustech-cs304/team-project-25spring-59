<script setup>
import {onMounted, reactive, watch} from "vue";
import request from "../../utils/request.js";
import {Plus, Clock, Calendar} from "@element-plus/icons-vue";

defineEmits(['clickChallenge', 'createChallenge']);

const challenges = reactive({})

watch(
    challenges,
    async (newValue, oldValue)=>{
      // sort the sharings by time from large to small
      newValue.data.sort((a,b)=>new Date(b.start_date) - new Date(a.start_date));
    }
)

onMounted(()=>{
  request.get('/challenges/all')
      .then((response) => {
        console.log(response);
        challenges.data = response.data.challenges
      })
      .catch((error) => {
        console.log(error)
      })
})

defineExpose({
  /**
   * 所有挑战数据
   * @member {import('vue').Reactive<{data: Array}>}
   */
  challenges,
})
</script>

<template>
  <div class="challenge-container">
    <el-row :gutter="20">
      <el-col :span="16" :offset="4">
        <div class="challenge-list">
          <el-card
              shadow="hover"
              v-for="challenge in challenges.data"
              :key="challenge.id"
              class="challenge-card"
              @click="$emit('clickChallenge', challenge.id)"
          >
            <div class="card-content">
              <div class="challenge-header">
                <h3 class="challenge-title">{{ challenge.title }}</h3>
                <div class="challenge-tags">
                  <el-tag
                      :type="challenge.challenge_type === '学习' ? 'success' : 'warning'"
                      class="type-tag"
                  >
                    {{ challenge.challenge_type }}
                  </el-tag>
                  <el-tag
                      :type="challenge.status === '进行中' ? 'danger' : 'info'"
                      class="status-tag"
                  >
                    {{ challenge.status }}
                  </el-tag>
                </div>
              </div>

              <div class="challenge-dates">
                <div class="date-item">
                  <el-icon><Calendar /></el-icon>
                  <span class="date-label">开始：</span>
                  <el-text type="info" size="small">{{ challenge.start_date }}</el-text>
                </div>
                <div class="date-item">
                  <el-icon><Calendar /></el-icon>
                  <span class="date-label">结束：</span>
                  <el-text type="info" size="small">{{ challenge.end_date }}</el-text>
                </div>
              </div>
            </div>
          </el-card>
        </div>
      </el-col>
    </el-row>

    <!-- Floating action button -->
    <el-affix target=".challenge-container" position="bottom" :offset="20">
      <el-button
          :icon="Plus"
          type="primary"
          size="large"
          circle
          class="create-btn"
          @click="$emit('createChallenge')"
      />
    </el-affix>
  </div>
</template>

<style scoped>
.challenge-container {
  padding: 20px 0;
  background-color: #f5f7fa;
  min-height: 100vh;
}

.challenge-list {
  display: grid;
  gap: 16px;
}

.challenge-card {
  border-radius: 12px;
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
}

.challenge-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.1);
}

.card-content {
  padding: 16px;
}

.challenge-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.challenge-title {
  margin: 0;
  font-size: 18px;
  font-weight: 500;
  color: #303133;
}

.challenge-tags {
  display: flex;
  gap: 8px;
}

.type-tag {
  font-weight: 500;
}

.status-tag {
  font-weight: 500;
}

.challenge-dates {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.date-item {
  display: flex;
  align-items: center;
  gap: 6px;
}

.date-item .el-icon {
  color: #909399;
  font-size: 14px;
}

.date-label {
  color: #606266;
  font-size: 14px;
}

.create-btn {
  width: 56px;
  height: 56px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  position: fixed;
  right: 40px;
  bottom: 40px;
}

.create-btn:hover {
  transform: scale(1.05);
}
</style>