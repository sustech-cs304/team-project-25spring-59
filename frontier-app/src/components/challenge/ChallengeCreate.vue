<script setup>
import {reactive, ref} from "vue";
import request from "../../utils/request.js";
import {toISO} from "../../utils/date.js";
import {ElMessage} from "element-plus";
import {ArrowLeft} from "@element-plus/icons-vue";

defineEmits(['backToList'])
const userId = Number(localStorage.getItem('user_id'))

const form = reactive({
  title: '',
  description: '',
  start_date: '',
  end_date: '',
  challenge_type: '',
  target_value: '',
  created_by: userId,
})

const isLoading = ref(false)

function validateForm() {
  if (!form.title.trim()) {
    ElMessage({message: '请输入挑战名称', type: 'warning'})
    return false
  }
  if (!form.description.trim()) {
    ElMessage({message: '请输入挑战说明', type: 'warning'})
    return false
  }
  if (!form.start_date) {
    ElMessage({message: '请选择开始时间', type: 'warning'})
    return false
  }
  if (!form.end_date) {
    ElMessage({message: '请选择结束时间', type: 'warning'})
    return false
  }
  if (new Date(form.end_date) <= new Date(form.start_date)) {
    ElMessage({message: '结束时间必须晚于开始时间', type: 'warning'})
    return false
  }
  if (!form.challenge_type) {
    ElMessage({message: '请选择挑战类型', type: 'warning'})
    return false
  }
  if (!form.target_value || Number(form.target_value) <= 0) {
    ElMessage({message: '请输入有效的目标值', type: 'warning'})
    return false
  }
  return true
}

function submit() {
  if (!validateForm()) return

  isLoading.value = true
  form.start_date = toISO(form.start_date)
  form.end_date = toISO(form.end_date)

  request({
    method: "POST",
    url: '/challenges',
    data: form,
  }).then((response) => {
    ElMessage({message: '挑战创建成功', type: 'success'})
    window.location.reload()
  }).catch((error) => {
    console.log(error)
    ElMessage({message: '创建失败，请重试', type: 'error'})
  }).finally(() => {
    isLoading.value = false
  })
}

defineExpose({
  /**
   * 表单数据对象
   * @member {import('vue').Reactive<{
   *   title: string,
   *   description: string,
   *   start_date: string,
   *   end_date: string,
   *   challenge_type: string,
   *   target_value: string,
   *   created_by: number
   * }>}
   */
  form,

  /**
   * 提交表单数据
   * @function
   * @async
   * @returns {Promise<void>}
   * @description 提交挑战表单数据到服务器，成功后显示成功消息并刷新页面
   */
  submit,
})
</script>

<template>
  <div class="create-container">
    <el-card class="create-card">
      <template #header>
        <div class="card-header">
          <el-button
              type="text"
              :icon="ArrowLeft"
              @click="$emit('backToList')"
              class="back-btn"
          >返回</el-button>
          <h2>创建新挑战</h2>
        </div>
      </template>

      <el-form
          :model="form"
          label-position="top"
          class="challenge-form"
      >
        <el-form-item label="挑战名称" prop="title">
          <el-input
              v-model="form.title"
              placeholder="输入挑战名称"
              class="form-input"
          />
        </el-form-item>

        <el-form-item label="挑战说明" prop="description">
          <el-input
              v-model="form.description"
              type="textarea"
              :rows="4"
              placeholder="详细描述挑战内容"
              resize="none"
              class="form-textarea"
              maxlength="300"
              show-word-limit
          />
        </el-form-item>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="开始时间" prop="start_date">
              <el-date-picker
                  v-model="form.start_date"
                  type="datetime"
                  placeholder="选择开始时间"
                  format="YYYY-MM-DD HH:mm"
                  value-format="YYYY-MM-DD HH:mm"
                  class="form-date-picker"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="结束时间" prop="end_date">
              <el-date-picker
                  v-model="form.end_date"
                  type="datetime"
                  placeholder="选择结束时间"
                  format="YYYY-MM-DD HH:mm"
                  value-format="YYYY-MM-DD HH:mm"
                  class="form-date-picker"
              />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="挑战类型" prop="challenge_type">
              <el-select
                  v-model="form.challenge_type"
                  placeholder="选择挑战类型"
                  class="form-select"
              >
                <el-option label="距离 (distance)" value="distance" />
                <el-option label="卡路里 (calories)" value="calories" />
                <el-option label="锻炼次数 (workouts)" value="workouts" />
                <el-option label="持续时间 (duration)" value="duration" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="目标值" prop="target_value">
              <el-input
                  v-model="form.target_value"
                  type="number"
                  placeholder="输入目标数值"
                  class="form-input"
              >
                <template #append>
                  <span v-if="form.challenge_type === 'distance'">公里</span>
                  <span v-else-if="form.challenge_type === 'calories'">卡路里</span>
                  <span v-else-if="form.challenge_type === 'workouts'">次</span>
                  <span v-else-if="form.challenge_type === 'duration'">分钟</span>
                  <span v-else>单位</span>
                </template>
              </el-input>
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item class="form-actions">
          <el-button
              type="primary"
              @click="submit"
              :loading="isLoading"
              class="submit-btn"
          >创建挑战</el-button>
          <el-button
              @click="$emit('backToList')"
              class="cancel-btn"
          >取消</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<style scoped>
.create-container {
  padding: 20px;
  background-color: #f5f7fa;
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: flex-start;
}

.create-card {
  width: 100%;
  max-width: 800px;
  border-radius: 12px;
  border: none;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.card-header {
  display: flex;
  align-items: center;
  padding: 10px 0;
  position: relative;
}

.card-header h2 {
  margin: 0 auto;
  color: #303133;
  font-size: 20px;
}

.back-btn {
  position: absolute;
  color: #606266;
}

.back-btn:hover {
  color: #409eff;
}

.challenge-form {
  padding: 0 20px;
}

:deep(.el-form-item__label) {
  font-weight: 500;
  color: #606266;
  padding-bottom: 8px;
}

.form-input, .form-textarea, .form-select, .form-date-picker {
  width: 100%;
}

.form-input :deep(.el-input__inner),
.form-textarea :deep(.el-textarea__inner),
.form-select :deep(.el-input__inner),
.form-date-picker :deep(.el-input__inner) {
  border-radius: 8px;
  transition: all 0.3s;
}

.form-input :deep(.el-input__inner):focus,
.form-textarea :deep(.el-textarea__inner):focus,
.form-select :deep(.el-input__inner):focus,
.form-date-picker :deep(.el-input__inner):focus {
  border-color: #409eff;
  box-shadow: 0 0 0 2px rgba(64, 158, 255, 0.2);
}

.form-actions {
  margin-top: 30px;
  display: flex;
  justify-content: flex-end;
}

.submit-btn {
  padding: 10px 25px;
  border-radius: 6px;
  font-weight: 500;
}

.cancel-btn {
  padding: 10px 25px;
  border-radius: 6px;
  margin-left: 15px;
}

:deep(.el-input-group__append) {
  background-color: #f5f7fa;
}
</style>