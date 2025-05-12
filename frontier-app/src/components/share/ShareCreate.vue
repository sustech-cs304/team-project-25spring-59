<script setup>

import {reactive} from "vue";
import {toISO} from "../../utils/date.js";
import request from "../../utils/request.js";

defineEmits(['backToList'])

const form = reactive({
  userId: 1,
  username: 'testuser',
  content: '',
  time: '',
  imgList: [],
})

function submit() {
  form.time = toISO(new Date())
  request({
    method: "POST",
    url: '/share/create',
    data: form,
  }).then((response) => {
    console.log(response);
    console.log(form)
  }).catch((error) => {
    console.log(error)
  })
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
          <el-button type="primary" @click="submit">创建</el-button>
          <el-button @click="$emit('backToList')">取消</el-button>
        </el-form-item>
      </el-form>
    </el-col>
  </el-row>
</template>

<style scoped>

</style>