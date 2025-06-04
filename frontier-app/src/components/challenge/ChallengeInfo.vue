<script setup>
import {onMounted, reactive, ref, computed} from "vue";
import request from "../../utils/request.js";
import {UserFilled, Trophy, Medal, GoldMedal, ArrowLeft} from "@element-plus/icons-vue";
import {ElMessage} from "element-plus";

const userId = Number(localStorage.getItem('user_id'))
const props = defineProps(['challengeId'])
const challenge = reactive({});
const challengeInfo = reactive({data: {}})
const participants = reactive({list: []})
const currentUserData = ref(null)

const isMine = ((id)=>{return id === userId})
const isJoined = ref(false)
const isEnd = computed(()=>{return challengeInfo.data.status === '已结束'})

function update(value) {
  if (!value && value !== 0) {
    ElMessage({message: '请输入有效数值', type: 'warning'})
    return
  }

  request({
    method: "POST",
    url: '/challenges/update-progress',
    data: {
      challenge_id: props.challengeId,
      user_id: userId,
      current_value: value,
    },
  }).then((response)=>{
    ElMessage({message: '更新成功', type: 'success'})
    window.location.reload()
  }).catch((error)=>{
    console.log(error)
    ElMessage({message: '更新失败', type: 'error'})
  })
}

function endChallenge() {
  request({
    method: "POST",
    url: '/challenges/end',
    data: {
      challenge_id: props.challengeId,
    },
  }).then((response)=>{
    ElMessage({message: '已结束挑战', type: 'success'})
    window.location.reload()
  }).catch((error)=>{
    console.log(error)
  })
}

function joinChallenge() {
  request({
    method: "POST",
    url: '/challenges/join',
    data: {
      challenge_id: props.challengeId,
      user_id: userId
    },
  }).then((response)=>{
    ElMessage({message: '加入成功', type: 'success'})
    window.location.reload()
  }).catch((error)=>{
    console.log(error)
    ElMessage({message: `${error.response.data.detail}`, type: 'error'})
  })
}

function processData(data) {
  challengeInfo.data = data.challenge;
  participants.list = data.leaderboard;
  // 找到当前用户的数据
  currentUserData.value = participants.list.find(p => p.user_id === userId) || null;
  // 检查用户是否已加入挑战
  isJoined.value = participants.list.some(p => p.user_id === userId);
  console.log(isJoined.value)
}

onMounted(()=>{
  request({
    method: 'post',
    url: '/challenges/detail',
    data: {challenge_id: props.challengeId},
  }).then((response) => {
    console.log(response);
    challenge.data = response.data
    processData(response.data)
  }).catch((error) => {
    console.log(error)
  })
})


// 计算排行榜前三名
const topParticipants = computed(() => {
  return [...participants.list]
      .sort((a, b) => b.current_value - a.current_value)
      .slice(0, 3);
});

// 计算其他参与者
const otherParticipants = computed(() => {
  return [...participants.list]
      .sort((a, b) => b.current_value - a.current_value)
      .slice(3);
});

defineExpose({
  /**
   * 挑战详情数据
   * @member {import('vue').Reactive<Object>}
   */
  challenge,

  /**
   * 处理后的挑战信息
   * @member {import('vue').Reactive<{data: Object}>}
   */
  challengeInfo,

  /**
   * 参与者的分组数据
   * @member {import('vue').Reactive<{list: Array}>}
   */
  participants,

  /**
   * 当前用户是否已加入挑战
   * @member {import('vue').Ref<boolean>}
   */
  isJoined,

  /**
   * 挑战是否已结束
   * @member {import('vue').ComputedRef<boolean>}
   */
  isEnd,

  /**
   * 更新挑战进度
   * @function
   * @param {number} value - 新的进度值
   */
  update,

  /**
   * 结束当前挑战
   * @function
   */
  endChallenge,

  /**
   * 加入当前挑战
   * @function
   */
  joinChallenge,

  /**
   * 检查是否是当前用户创建的挑战
   * @function
   * @param {number} id - 用户ID
   * @returns {boolean}
   */
  isMine
})
</script>

<template>
  <div class="challenge-container">
    <el-row :gutter="20">
      <el-col :span="16" :offset="4">
        <!-- 挑战信息卡片 -->
        <el-card class="challenge-info-card">
          <div slot="header">
            <div class="card-header">
              <el-button
                  type="text"
                  :icon="ArrowLeft"
                  @click="$emit('backToList')"
                  class="back-btn"
              >返回</el-button>
            </div>
          </div>
          <el-descriptions :title="challengeInfo.data.title" border>
            <template #extra>
              <el-button
                  v-if="isJoined"
                  type="info"
                  disabled
                  class="action-btn"
              >已加入</el-button>
              <el-button
                  v-else
                  type="primary"
                  @click="joinChallenge"
                  class="action-btn"
              >加入挑战</el-button>
              <el-button
                  v-if="isMine(challengeInfo.data.created_by) && !isEnd"
                  type="danger"
                  @click="endChallenge"
                  class="action-btn"
              >结束挑战</el-button>
              <el-button
                  v-else-if="isMine(challengeInfo.data.created_by) && isEnd"
                  type="info"
                  disabled
                  class="action-btn"
              >已结束</el-button>
            </template>
            <el-descriptions-item label="创建者" label-class-name="desc-label">
              <el-tag>{{ challengeInfo.data.created_by_name || challengeInfo.data.created_by }}</el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="挑战类型" label-class-name="desc-label">
              <el-tag :type="challengeInfo.data.challenge_type === '学习' ? 'success' : 'warning'">
                {{ challengeInfo.data.challenge_type }}
              </el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="挑战状态" label-class-name="desc-label">
              <el-tag :type="challengeInfo.data.status === '进行中' ? 'success' : 'info'">
                {{ challengeInfo.data.status }}
              </el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="挑战说明" label-class-name="desc-label">
              {{ challengeInfo.data.description }}
            </el-descriptions-item>
            <el-descriptions-item label="目标值" label-class-name="desc-label">
              {{ challengeInfo.data.target_value }}
            </el-descriptions-item>
            <el-descriptions-item label="开始时间" label-class-name="desc-label">
              {{ challengeInfo.data.start_date }}
            </el-descriptions-item>
            <el-descriptions-item label="结束时间" label-class-name="desc-label">
              {{ challengeInfo.data.end_date }}
            </el-descriptions-item>
          </el-descriptions>
        </el-card>

        <!-- 参与者区域 -->
        <el-row :gutter="20" class="participants-section">
          <!-- 左侧：当前用户卡片 -->
          <el-col :span="12" v-if="currentUserData">
            <el-card class="user-card">
              <template #header>
                <div class="user-header">
                  <el-avatar :size="40" :icon="UserFilled" />
                  <div class="user-info">
                    <h3>{{ currentUserData.username }}</h3>
                    <el-text type="info">我的进度</el-text>
                  </div>
                </div>
              </template>

              <div class="progress-section">
                <el-progress
                    :percentage="(currentUserData.current_value / challengeInfo.data.target_value) * 100"
                    :color="customColors"
                    :format="formatProgress"
                />
                <div class="progress-input">
                  <el-input-number
                      v-model="currentUserData.current_value"
                      :min="0"
                      :max="challengeInfo.data.target_value"
                      :disabled="isEnd"
                      controls-position="right"
                  />
                  <el-button
                      type="primary"
                      :disabled="isEnd"
                      @click="update(currentUserData.current_value)"
                      class="update-btn"
                  >更新</el-button>
                </div>
                <el-text class="progress-text">
                  已完成 {{ currentUserData.current_value }} / {{ challengeInfo.data.target_value }}
                </el-text>
              </div>
            </el-card>
          </el-col>

          <!-- 右侧：排行榜 -->
          <el-col :span="12">
            <el-card class="leaderboard-card">
              <template #header>
                <div class="leaderboard-header">
                  <el-icon :size="24" color="#ffd700"><Trophy /></el-icon>
                  <h3>排行榜</h3>
                </div>
              </template>

              <!-- 前三名 -->
              <div class="top-three">
                <div
                    v-for="(participant, index) in topParticipants"
                    :key="participant.user_id"
                    class="top-participant"
                    :class="{'first-place': index === 0, 'second-place': index === 1, 'third-place': index === 2}"
                >
                  <div class="rank-icon">
                    <el-icon v-if="index === 0" color="#ffd700"><GoldMedal /></el-icon>
                    <el-icon v-else-if="index === 1" color="#c0c0c0"><Medal /></el-icon>
                    <el-icon v-else-if="index === 2" color="#cd7f32"><Medal /></el-icon>
                    <span v-else>{{ index + 1 }}</span>
                  </div>
                  <el-avatar :size="32" :icon="UserFilled" />
                  <div class="participant-info">
                    <span class="participant-name">{{ participant.username }}</span>
                    <el-progress
                        :percentage="(participant.current_value / challengeInfo.data.target_value) * 100"
                        :show-text="false"
                        :color="index === 0 ? '#ffd700' : index === 1 ? '#c0c0c0' : '#cd7f32'"
                    />
                  </div>
                  <span class="participant-value">{{ participant.current_value }}</span>
                </div>
              </div>

              <!-- 其他参与者 -->
              <div class="other-participants">
                <div
                    v-for="(participant, index) in otherParticipants"
                    :key="participant.user_id"
                    class="participant-item"
                >
                  <span class="rank">{{ index + 4 }}</span>
                  <el-avatar :size="28" :icon="UserFilled" />
                  <span class="name">{{ participant.username }}</span>
                  <el-progress
                      :percentage="(participant.current_value / challengeInfo.data.target_value) * 100"
                      :show-text="false"
                      color="#409eff"
                  />
                  <span class="value">{{ participant.current_value }}</span>
                </div>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </el-col>
    </el-row>
  </div>
</template>

<style scoped>
.challenge-container {
  padding: 20px 0;
  background-color: #f5f7fa;
  min-height: 100vh;
}

.challenge-info-card {
  margin-bottom: 20px;
  border-radius: 12px;
  border: none;
}

:deep(.desc-label) {
  font-weight: 500;
  color: #606266;
}

.action-btn {
  margin-left: 10px;
}

.participants-section {
  margin-top: 20px;
}

.user-card, .leaderboard-card {
  border-radius: 12px;
  border: none;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  height: 100%;
}

.user-header {
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-info {
  display: flex;
  flex-direction: column;
}

.user-info h3 {
  margin: 0;
  font-size: 16px;
}

.progress-section {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

:deep(.el-progress-bar) {
  padding-right: 0;
}

:deep(.el-progress__text) {
  min-width: 50px;
}

.progress-input {
  display: flex;
  gap: 10px;
  align-items: center;
}

.update-btn {
  width: 80px;
}

.progress-text {
  text-align: center;
  font-size: 14px;
}

.leaderboard-header {
  display: flex;
  align-items: center;
  gap: 8px;
}

.leaderboard-header h3 {
  margin: 0;
  color: #303133;
}

.top-three {
  display: flex;
  flex-direction: column;
  gap: 15px;
  margin-bottom: 20px;
}

.top-participant {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px;
  border-radius: 8px;
  background-color: #fafafa;
}

.first-place {
  background: linear-gradient(135deg, rgba(255,215,0,0.1) 0%, rgba(255,215,0,0.05) 100%);
  border-left: 3px solid #ffd700;
}

.second-place {
  background: linear-gradient(135deg, rgba(192,192,192,0.1) 0%, rgba(192,192,192,0.05) 100%);
  border-left: 3px solid #c0c0c0;
}

.third-place {
  background: linear-gradient(135deg, rgba(205,127,50,0.1) 0%, rgba(205,127,50,0.05) 100%);
  border-left: 3px solid #cd7f32;
}

.rank-icon {
  width: 24px;
  text-align: center;
  font-weight: bold;
}

.participant-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.participant-name {
  font-size: 14px;
  font-weight: 500;
}

.participant-value {
  font-weight: bold;
  color: #303133;
}

.other-participants {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.participant-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px;
  border-radius: 6px;
  transition: all 0.3s;
}

.participant-item:hover {
  background-color: #f5f7fa;
}

.rank {
  width: 24px;
  text-align: center;
  font-size: 14px;
  color: #909399;
}

.name {
  flex: 1;
  font-size: 14px;
}

.value {
  font-size: 14px;
  color: #409eff;
  font-weight: 500;
}

:deep(.el-progress-bar__outer) {
  border-radius: 0;
}

:deep(.el-progress-bar__inner) {
  border-radius: 0;
}

.custom-colors {
  --el-color-primary: #ffd700;
}

.custom-colors .el-progress-bar__inner {
  background-color: var(--el-color-primary);
}
</style>