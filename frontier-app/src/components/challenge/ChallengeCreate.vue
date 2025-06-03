<script setup>

import {reactive} from "vue";
import request from "../../utils/request.js";
import {toISO} from "../../utils/date.js";
import {ElMessage} from "element-plus";

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

function submit() {
  form.start_date = toISO(form.start_date)
  form.end_date = toISO(form.end_date)
  console.log(form)
  request({
    method: "POST",
    url: '/challenges',
    data: form,
  }).then((response) => {
    console.log(response);
    ElMessage({message: '创建成功', type: 'success',})
    window.location.reload()
  }).catch((error) => {
    console.log(error)
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
              v-model="form.end_date"
              type="datetime"
              placeholder="选择结束时间"
              style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="挑战类型：">
          <el-select v-model="form.challenge_type" placeholder="选择挑战类型">
            <el-option label="distance" value="distance" />
            <el-option label="calories" value="calories" />
            <el-option label="workouts" value="workouts" />
            <el-option label="duration" value="duration" />
          </el-select>
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