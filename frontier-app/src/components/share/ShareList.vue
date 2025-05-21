<script setup>

import {onMounted, reactive, watch, ref} from "vue";
import {Plus, UserFilled, Edit} from "@element-plus/icons-vue";
import request from "../../utils/request.js";
import {ElMessage} from "element-plus";

defineEmits(['createShare'])

const sharings = reactive({});
const form = reactive({
  comment: "",
})


function processData(data) {
  sharings.data = data;
  // sort the sharings by time from large to small
  sharings.data.sort((a,b)=>new Date(b.time) - new Date(a.time));
  sharings.data.forEach((sharing)=>{
    // sort the sharings.comment by time from large to small
    sharing.comments.sort((a,b)=>new Date(b.time) - new Date(a.time))
    // add blank comment area
    sharing.newComment = "";
    sharing.showCommentArea = false;
  });
}

function addComment(postId, comment) {
  console.log(postId, comment)
  request({
    method: "POST",
    url: `/posts/${postId}/comments`,
    data: {
      userId: localStorage.getItem('user_id'),
      comment: comment,
    },
  }).then((response)=>{
    console.log(response)
    ElMessage({message: '评论成功', type: 'success',})
    window.location.reload()
  }).catch((error)=>{
    console.log(error)
  })
}

onMounted(()=>{
  request.get('/posts')
      .then((response) => {
        console.log(response);
        processData(response.data);
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
          <el-row justify="space-between">
            <el-text tag="b">评论：</el-text>
            <el-button :icon="Edit" link @click="sharing.showCommentArea=true">写评论</el-button>
          </el-row>
          <div v-show="sharing.showCommentArea">
            <el-input v-model="sharing.newComment" type="textarea" placeholder="说说你的想法："/>
            <el-button type="primary" @click="addComment(sharing.postId, sharing.newComment)">发布</el-button>
            <el-button @click="sharing.showCommentArea=false">取消</el-button>
          </div>

          <el-form :model="form">
            <el-form-item>

            </el-form-item>
            <el-form-item>

            </el-form-item>
          </el-form>

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