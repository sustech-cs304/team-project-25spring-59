<script setup>

import {onMounted, reactive, watch, ref} from "vue";
import request from "../../utils/request.js";
import {UserFilled} from "@element-plus/icons-vue";

const props = defineProps(['challengeId'])
const challenge = reactive({});
const challengeInfo = reactive({})
const participants = reactive({})

const myValue = ref()

function update() {
  console.log(localStorage)
  request({
    method: "POST",
    url: '/challenges/update-progress',
    data: {
      challenge_id: props.challengeId,
      user_id: localStorage.getItem('user_id'),
      current_value: myValue,
    },
  }).then((response)=>{
    console.log(response)
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
  console.log(props.challengeId)
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
        <el-row>
          <el-text tag="b" size="large">挑战：</el-text>
          {{ challengeInfo.data }}
        </el-row>
<!--        <el-row>-->
<!--          <el-text tag="b" size="large">挑战：</el-text>-->
<!--          {{ challengeInfo.data.title }}-->
<!--        </el-row>-->
<!--        <el-row>-->
<!--          <el-text tag="b" size="large">创建者：</el-text>-->
<!--          <el-text>{{ challengeInfo.data.created_by }}</el-text>-->
<!--        </el-row>-->
<!--        <el-row>-->
<!--          <el-text tag="b" size="large">挑战类型：</el-text>-->
<!--          <el-tag>{{ challengeInfo.data.challenge_type }}</el-tag>-->
<!--        </el-row>-->
<!--        <el-row>-->
<!--          <el-text tag="b" size="large">挑战说明：</el-text>-->
<!--          <el-text>{{ challengeInfo.data.description }}</el-text>-->
<!--        </el-row>-->
<!--        <el-row>-->
<!--          <el-text tag="b" size="large">目标：</el-text>-->
<!--          <el-text>{{ challengeInfo.data.target_value }}</el-text>-->
<!--        </el-row>-->
<!--        <el-row>-->
<!--          <el-text tag="b" size="large">开始时间：</el-text>-->
<!--          <el-text>{{ challengeInfo.data.start_date }}</el-text>-->
<!--        </el-row>-->
<!--        <el-row>-->
<!--          <el-text tag="b" size="large">结束时间：</el-text>-->
<!--          <el-text>{{ challengeInfo.data.end_date }}</el-text>-->
<!--        </el-row>-->

        <el-button type="primary" @click="joinChallenge">加入</el-button>
        <el-button type="primary" @click="endChallenge">结束挑战</el-button>

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
<!--                    <el-col :span="8" :offset="10">-->
<!--                      <el-text type="info" size="small">|{{ sharing.time }}</el-text>-->
<!--                    </el-col>-->
                  </el-row>
                </template>
                <div>
                  完成量：
                  <el-input
                    type="number"
                    v-model="myValue"
                    :placeholder="participant.current_value"
                  ></el-input>
                  <el-button type="primary" @click="update">更新</el-button>
                  <br/>
                  <el-tag type="primary">{{ participant.completed }}</el-tag><br/>
                </div>
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