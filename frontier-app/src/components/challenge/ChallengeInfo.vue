<script setup>

import {onMounted, reactive, watch, ref, computed} from "vue";
import request from "../../utils/request.js";
import {UserFilled} from "@element-plus/icons-vue";
import {ElMessage} from "element-plus";

const props = defineProps(['challengeId'])
const challenge = reactive({});
const challengeInfo = reactive({data: {}})
const participants = reactive({})

const isMine = ((id)=>{return id === Number(localStorage.getItem('user_id'))})

function update(value) {
  console.log(value)
  request({
    method: "POST",
    url: '/challenges/update-progress',
    data: {
      challenge_id: props.challengeId,
      user_id: localStorage.getItem('user_id'),
      current_value: value,
    },
  }).then((response)=>{
    console.log(response)
    ElMessage({message: '更新成功', type: 'success',})
  }).catch((error)=>{
    console.log(error)
  })
}

function endChallenge() {
  console.log(localStorage)
  request({
    method: "POST",
    url: '/challenges/end',
    data: {
      challenge_id: props.challengeId,
    },
  }).then((response)=>{
    console.log(response)
  }).catch((error)=>{
    console.log(error)
  })
}

function joinChallenge() {
  console.log(localStorage)
  request({
    method: "POST",
    url: '/challenges/join',
    data: {
      challenge_id: props.challengeId,
      user_id: localStorage.getItem('user_id')
    },
  }).then((response)=>{
    console.log(response)
  }).catch((error)=>{
    console.log(error)
  })
}

function processData(data) {
  challengeInfo.data = data.challenge;
  loadParticipants(data.leaderboard);
}

function loadParticipants(list) {
  let pairList = [];
  for (let i = 0; i < list.length; i+=2) {
    if (i+1 < list.length) {
      pairList.push([list[i], list[i+1]]);
    } else {
      pairList.push([list[i]]);
    }
  }
  participants.pairs = pairList;
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

</script>

<template>
  <el-row>
    <el-col :span="16" :offset="4">
      <el-card>
        <el-descriptions :title="challengeInfo.data.title">
          <template #extra>
            <el-button type="primary" @click="joinChallenge">加入挑战</el-button>
            <el-button type="primary" @click="endChallenge" v-if="isMine(challengeInfo.data.created_by)">结束挑战</el-button>
          </template>
          <el-descriptions-item label="创建者：">{{ challengeInfo.data.created_by }}</el-descriptions-item>
          <el-descriptions-item label="挑战类型：">
            <el-tag>{{ challengeInfo.data.challenge_type }}</el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="挑战说明：">{{ challengeInfo.data.description }}</el-descriptions-item>
          <el-descriptions-item label="目标：">{{ challengeInfo.data.target_value }}</el-descriptions-item>
          <el-descriptions-item label="开始时间：">{{ challengeInfo.data.start_date }}</el-descriptions-item>
          <el-descriptions-item label="结束时间：">{{ challengeInfo.data.end_date }}</el-descriptions-item>
        </el-descriptions>

      </el-card>

      <el-carousel indicator-position="outside" :autoplay="false" :loop="false" trigger="click">
        <el-carousel-item v-for="pair in participants.pairs">
          <el-row>
            <el-col :span="12" v-for="participant in pair">
              <el-card >
                <template #header>
                  <el-row align="bottom">
                    <el-col :span="2">
                      <el-icon :size="25"><UserFilled/></el-icon>
                    </el-col>
                    <el-col :span="4">
                      {{ participant.username }}
                    </el-col>
                  </el-row>
                </template>
                <el-row align="middle">
                  <el-col :span="18">
                    <span>完成量：</span>
                    <el-input
                        type="number"
                        v-model="participant.current_value"
                        style="width: 150px"
                        :disabled="!isMine(participant.user_id)"
                    />
                  </el-col>
                  <el-col :span="6">
                    <el-button type="primary" @click="update(participant.current_value)">更新</el-button>
                  </el-col>
                </el-row>
                <el-tag type="primary">{{ participant.completed }}</el-tag><br/>
              </el-card>
            </el-col>
          </el-row>
        </el-carousel-item>
      </el-carousel>

    </el-col>
  </el-row>
</template>

<style scoped>

</style>