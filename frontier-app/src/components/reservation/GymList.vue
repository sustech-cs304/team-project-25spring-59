<script setup>

import {onMounted, reactive} from "vue";
import request from "../../utils/request.js";

defineEmits(['clickGym']);

const gyms = reactive({});

onMounted(()=>{
  request.get('/gym/getGyms')
      .then((response) => {
        console.log(response);
        gyms.data = response.data
      })
      .catch((error) => {
        console.log(error)
      })
})

</script>

<template>
  <el-row>
    <el-col :span="12" :offset="6">
      <el-card shadow="hover" v-for="gym in gyms.data">
        <div @click="$emit('clickGym', gym.id)">
          <span>{{ gym.name }}</span>
          <div class="bottom">
            <span>开放时间：{{ gym.openTime }}</span><br/>
            <span>地址：{{ gym.address }}</span>
          </div>
        </div>
      </el-card>
    </el-col>
  </el-row>
</template>

<style scoped>

.bottom {
  margin-top: 10px;
  border-top: 1px solid darkgrey;
  padding-top: 10px;
  font-size: 10px;
}

</style>