<script setup>

import {onMounted, reactive, watch} from "vue";
import request from "../../utils/request.js";
import {UserFilled} from "@element-plus/icons-vue";

const props = defineProps(['challengeId'])
const challenge = reactive({})
const participants = reactive({})

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
    data: {'challenge_id': props.challengeId},
  }).then((response) => {
    console.log(response);
    challenge.data = response.data
    loadParticipants(response.data.leaderboard)
  }).catch((error) => {
    console.log(error)
  })
})

</script>

<template>
  <el-row>
    <el-col :span="16" :offset="4">

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
                <el-row>
                  挑战：
                  <el-tag>{{ challenge.data.challenge.challenge_type }}</el-tag>
                  <el-text>{{ challenge.data.challenge.title }}</el-text><br/>
                </el-row>
                <div>
                  挑战说明：<el-text size="small">{{ challenge.data.challenge.description }}</el-text><br/>
                  目标：<el-text>{{ challenge.data.challenge.target_value }}</el-text><br/>
                  完成个数： <el-text>{{ participant.current_value }}</el-text><br/>
                  <el-tag type="primary">{{ participant.completed }}</el-tag><br/>
                </div>
                <el-row>
                  <el-col>

                  </el-col>
                </el-row>
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