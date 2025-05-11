<script setup>

import {onMounted, reactive, watch} from "vue";
import {Plus, UserFilled} from "@element-plus/icons-vue";
import request from "../../utils/request.js";

defineEmits(['createShare'])

const sharings = reactive({});

watch(
    sharings,
    async (newValue, oldValue)=>{
      // sort the sharings by time from large to small
      newValue.data.sort((a,b)=>new Date(b.time) - new Date(a.time));
      // sort the sharings.comment by time from large to small
      newValue.data.forEach((sharing)=>{
        sharing.comments.sort((a,b)=>new Date(b.time) - new Date(a.time))
      });
    }
)

onMounted(()=>{
  request.get('/share/getAll')
      .then((response) => {
        console.log(response);
        sharings.data = response.data
      })
      .catch((error) => {
        console.log(error)
      })
})

</script>

<template>
  <el-row class="sharing-container">
    <el-col :span="12" :offset="6">
      <el-card shadow="never" v-for="sharing in sharings.data">
        <template #header>
          <el-row align="bottom">
            <el-col :span="2">
              <el-icon :size="25"><UserFilled/></el-icon>
            </el-col>
            <el-col :span="4">
              {{ sharing.userName }}
            </el-col>
            <el-col :span="8" :offset="10">
              <el-text type="info" size="small">|{{ sharing.time }}</el-text>
            </el-col>
          </el-row>
        </template>
        <p>
          {{ sharing.content }}
        </p>
        <template #footer>
          <el-text tag="b">评论：</el-text>
          <el-row>
            <el-col :span="20" :offset="2">
              <el-card shadow="never" v-for="comment in sharing.comments">
                <template #header>
                  <el-row align="bottom">
                    <el-col :span="2">
                      <el-icon :size="25"><UserFilled/></el-icon>
                    </el-col>
                    <el-col :span="4">
                      {{ comment.userName }}
                    </el-col>
                    <el-col :span="8" :offset="10">
                      <el-text type="info" size="small">|{{ comment.time }}</el-text>
                    </el-col>
                  </el-row>
                </template>
                <p>
                  {{ comment.comment }}
                </p>
              </el-card>
            </el-col>
          </el-row>
        </template>
      </el-card>
    </el-col>
  </el-row>

  <!--fixed navigating bar at the bottom-->
  <el-affix target=".sharing-container" position="bottom" :offset="20">
    <el-row>
      <el-col :span="10" :offset="7">
        <div style="display: flex; justify-content: center">
          <el-button :icon="Plus" type="success" size="large" circle @click="$emit('createShare')"/>
        </div>
      </el-col>
    </el-row>
  </el-affix>

</template>

<style scoped>
.sharing-container {

}

</style>