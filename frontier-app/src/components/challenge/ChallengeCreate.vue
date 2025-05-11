<script setup>

import {reactive} from "vue";
import request from "../../utils/request.js";

defineEmits(['backToList'])

const props = defineProps(['userId'])
const form = reactive({
  title: '',
  description: '',
  start_date: '',
  end_date: '',
  challenge_type: '',
  target_value: '',
  created_by: props.userId,
})

function submit() {
  request({
    method: "POST",
    url: '/challenges',
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
        <el-form-item label="挑战名称：">
          <el-input v-model="form.title"/>
        </el-form-item>
        <el-form-item label="挑战说明：">
          <el-input v-model="form.description" type="textarea"/>
        </el-form-item>
        <el-form-item label="开始时间：">
          <el-date-picker
            v-model="form.start_date"
            type="datetime"
            placeholder="选择开始时间"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="结束时间：">
          <el-date-picker
              v-model="form.start_date"
              type="datetime"
              placeholder="选择结束时间"
              style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="挑战类型：">
          <el-input v-model="form.challenge_type"/>
        </el-form-item>
        <el-form-item label="目标">
          <el-input v-model="form.target_value" type="number"/>
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