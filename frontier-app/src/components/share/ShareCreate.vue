<script lang="ts" setup>
import {reactive, ref} from "vue";
import request from "../../utils/request.js";
import {ElMessage} from "element-plus";
import type {UploadProps, UploadUserFile} from 'element-plus'
import {Plus, ArrowLeft} from "@element-plus/icons-vue";

defineEmits(['backToList'])

const userId = Number(localStorage.getItem('user_id'))
const form = reactive({
  content: '',
  files: ref<UploadUserFile[]>([]),
})
const formdata = new FormData()
const isLoading = ref(false)

function submit() {
  if (!form.content.trim()) {
    ElMessage({message: '分享内容不能为空', type: 'warning'})
    return;
  }

  isLoading.value = true;
  formdata.append('user_id', userId.toString())
  formdata.append('content', form.content)

  request({
    method: "POST",
    url: '/posts',
    headers: {
      'Content-Type': 'multipart/form-data'
    },
    data: formdata,
  }).then((response) => {
    ElMessage({message: '发布成功', type: 'success'})
    window.location.reload()
  }).catch((error) => {
    console.log(error)
    ElMessage({message: '发布失败', type: 'error'})
  }).finally(() => {
    isLoading.value = false;
  })
}

const handleChange: UploadProps['onChange'] = (uploadFile, uploadFiles) => {
  if (uploadFiles.length > 9) {
    ElMessage({message: '最多只能上传9张图片', type: 'warning'})
    return false;
  }
  formdata.append('files', uploadFile.raw)
}

const handleRemove: UploadProps['onRemove'] = (uploadFile, uploadFiles) => {
  // 这里可以添加从formdata中移除对应文件的逻辑
}

const handlePreview: UploadProps['onPreview'] = (uploadFile) => {
  // 预览逻辑
}
</script>

<template>
  <div class="share-create-container">
    <el-card class="share-create-card">
      <template #header>
        <div class="card-header">
          <el-button
              type="text"
              :icon="ArrowLeft"
              @click="$emit('backToList')"
              class="back-btn"
          >返回</el-button>
          <h2>创建分享</h2>
        </div>
      </template>

      <el-form :model="form" label-position="top">
        <el-form-item label="分享内容" class="form-item">
          <el-input
              v-model="form.content"
              type="textarea"
              :rows="5"
              placeholder="写下你想分享的内容..."
              resize="none"
              class="content-input"
              maxlength="500"
              show-word-limit
          />
        </el-form-item>

        <el-form-item label="添加图片 (最多9张)" class="form-item">
          <el-upload
              v-model:file-list="form.files"
              list-type="picture-card"
              :auto-upload="false"
              :on-preview="handlePreview"
              :on-change="handleChange"
              :on-remove="handleRemove"
              :limit="9"
              accept="image/*"
              class="image-uploader"
          >
            <el-icon><Plus /></el-icon>
          </el-upload>
        </el-form-item>

        <el-form-item class="action-buttons">
          <el-button
              type="primary"
              @click="submit"
              :loading="isLoading"
              class="submit-btn"
          >发布分享</el-button>
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
.share-create-container {
  padding: 20px;
  background-color: #f5f7fa;
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: flex-start;
}

.share-create-card {
  width: 100%;
  max-width: 800px;
  border-radius: 12px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  border: none;
}

.card-header {
  display: flex;
  align-items: center;
  padding: 10px 0;
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

.form-item {
  margin-bottom: 25px;
}

.content-input {
  font-size: 15px;
}

.content-input :deep(.el-textarea__inner) {
  border-radius: 8px;
  padding: 12px;
  box-shadow: none;
  border: 1px solid #dcdfe6;
  transition: all 0.3s;
}

.content-input :deep(.el-textarea__inner):focus {
  border-color: #409eff;
  box-shadow: 0 0 0 2px rgba(64, 158, 255, 0.2);
}

.image-uploader :deep(.el-upload) {
  width: 100px;
  height: 100px;
  border-radius: 8px;
  border: 1px dashed #dcdfe6;
  background-color: #fafafa;
  transition: all 0.3s;
  display: flex;
  justify-content: center;
  align-items: center;
}

.image-uploader :deep(.el-upload):hover {
  border-color: #409eff;
  background-color: #f0f7ff;
}

.image-uploader :deep(.el-upload-list__item) {
  width: 100px;
  height: 100px;
  border-radius: 8px;
  transition: all 0.3s;
}

.image-uploader :deep(.el-upload-list__item):hover {
  transform: translateY(-3px);
}

.action-buttons {
  display: flex;
  justify-content: flex-end;
  margin-top: 30px;
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

:deep(.el-form-item__label) {
  font-weight: 500;
  color: #606266;
  padding-bottom: 8px;
}
</style>