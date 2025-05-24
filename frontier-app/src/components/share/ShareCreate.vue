<script lang="ts" setup>

import {reactive, ref} from "vue";
import request from "../../utils/request.js";
import {ElMessage} from "element-plus";
import type {UploadProps, UploadUserFile} from 'element-plus'

defineEmits(['backToList'])

const userId = Number(localStorage.getItem('user_id'))
const form = reactive({
  content: '',
  files: ref<UploadUserFile[]>([]),
})
const formdata = new FormData()

function submit() {
  formdata.append('user_id', userId.toString())
  formdata.append('content', form.content)
  console.log(formdata.getAll('files'))
  request({
    method: "POST",
    url: '/posts',
    headers: {
      'Content-Type': 'multipart/form-data'
    },
    // transformRequest: [function(data, headers) {
    //   // 去除post请求默认的Content-Type
    //   console.log(headers)
    //   delete headers.post['Content-Type']
    //   return data
    // }],
    data: formdata,
  }).then((response) => {
    console.log(response);
    ElMessage({message: '发布成功', type: 'success',})
    window.location.reload()
  }).catch((error) => {
    console.log(error)
    ElMessage({message: '发布失败', type: 'error',})
  })
}

const handleChange: UploadProps['onChange'] = (uploadFile, uploadFiles) => {
  console.log(uploadFile, uploadFiles)
  formdata.append('files', uploadFile.raw)
}

const handleRemove: UploadProps['onRemove'] = (uploadFile, uploadFiles) => {
  console.log(uploadFile, uploadFiles)
}

const handlePreview: UploadProps['onPreview'] = (uploadFile) => {
  console.log(uploadFile)
}

</script>

<template>
  <el-row>
    <el-col :span="12" :offset="6">
      <el-form :model="form">
        <el-form-item label="说出你的分享：">
          <el-input v-model="form.content" type="textarea"/>
        </el-form-item>
        <el-form-item>
          <el-upload
              v-model:file-list="form.files"
              list-type="picture-card"
              :auto-upload="false"
              :on-preview="handlePreview"
              :onChange="handleChange"
              :on-remove="handleRemove"
          >
            <el-icon><Plus /></el-icon>
          </el-upload>

<!--          <el-dialog v-model="dialogVisible">-->
<!--            <img w-full :src="dialogImageUrl" alt="Preview Image" />-->
<!--          </el-dialog>-->
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="submit">创建</el-button>
          <el-button @click="$emit('backToList')">取消</el-button>
        </el-form-item>
      </el-form>
    </el-col>
  </el-row>
</template>

<style scoped>

</style>