<script setup>

import {onMounted, reactive, watch, ref, markRaw} from "vue";
import {Plus, UserFilled, ChatDotRound, Star, StarFilled} from "@element-plus/icons-vue";
import request, {baseurl} from "../../utils/request.js";
import {ElMessage} from "element-plus";

defineEmits(['createShare'])

const sharings = reactive({data: []});
const userId = Number(localStorage.getItem('user_id'))


function processData(data) {
  sharings.data = data;
  // sort the sharings by time from large to small
  sharings.data.sort((a,b)=>new Date(b.time) - new Date(a.time));
  sharings.data.forEach((sharing)=>{
    // sort the sharings.comment by time from large to small
    sharing.comments.sort((a,b)=>new Date(b.time) - new Date(a.time))
    sharing.commentCount = sharing.comments.length;
    // add comment attribute
    sharing.newComment = "";
    sharing.showComment = false;
    sharing.showWriteCommentArea = false;
    // process imgList
    sharing.imgList = Array.from(sharing.imgList, ({ img })=>baseurl+img)
    // add like identifier
    sharing.likeIcon = sharing.likeList.indexOf(userId) !== -1 ? markRaw(StarFilled) : markRaw(Star)
    sharing.comments.forEach((comment)=>{
      comment.likeIcon = comment.likeList.indexOf(userId) !== -1 ? markRaw(StarFilled) : markRaw(Star)
    })
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

function clickLike(postId, icon) {
  const sharing = sharings.data.find((sharing)=>sharing.postId === postId)
  console.log(sharing, markRaw(Star))
  const url = ref('')
  if(icon === markRaw(Star)) {
    sharing.likeIcon = markRaw(StarFilled);
    sharing.likeCount += 1;
    url.value = `/posts/${postId}/like`
  }
  else {
    sharing.likeIcon = markRaw(Star);
    sharing.likeCount -= 1;
    url.value = `/posts/${postId}/unlike`
  }
  request({
    method: "POST",
    url: url.value,
    data: {user_id: userId,},
  }).then((response)=>{
    console.log(response)
  }).catch((error)=>{
    console.log(error)
  })
}

function clickCommentLike(postId, commentId, icon) {
  const sharing = sharings.data.find((sharing)=>sharing.postId === postId)
  const comment = sharing.comments.find((comment)=>comment.commentId === commentId)
  console.log(comment)
  const url = ref('')
  if(icon === markRaw(Star)) {
    comment.likeIcon = markRaw(StarFilled);
    comment.likeCount += 1;
    url.value = `/comments/${commentId}/like`
  }
  else {
    comment.likeIcon = markRaw(Star);
    comment.likeCount -= 1;
    url.value = `/comments/${commentId}/unlike`
  }
  request({
    method: "POST",
    url: url.value,
    data: {user_id: userId,},
  }).then((response)=>{
    console.log(response)
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
        <div slot="header">
          <el-row align="top">
            <el-col :span="2">
              <el-icon :size="35"><UserFilled/></el-icon>
            </el-col>
            <el-col :span="8">
              <el-text>{{ sharing.userName }}</el-text><br/>
              <el-text type="info" size="small">{{ sharing.time }}</el-text>
            </el-col>
          </el-row>
        </div>

        <el-row>
          <el-col :offset="2">
            <p>
              {{ sharing.content }}
            </p>
            <div v-for="url in sharing.imgList" style="display: inline-block">
              <el-image
                  style="width: 100px; height: 100px; margin: 1px"
                  :src="url"
                  fit="cover"
                  :preview-src-list="sharing.imgList"
              />
            </div>
          </el-col>
        </el-row>
        <el-row justify="space-around">
          <el-col :span="1">
            <el-button type="info" link @click="sharing.showComment=!sharing.showComment">
              <el-icon :size="20"><ChatDotRound/></el-icon>
              <el-text size="small">{{ sharing.commentCount }}</el-text>
            </el-button>
          </el-col>
          <el-col :span="1">
            <el-button type="info" link @click="clickLike(sharing.postId, sharing.likeIcon)">
              <el-icon :size="20">
                <Component :is="sharing.likeIcon"/>
              </el-icon>
              <el-text size="small">{{ sharing.likeCount }}</el-text>
            </el-button>
          </el-col>
        </el-row>

        <div slot="footer" v-show="sharing.showComment" style="margin-top: 10px">
          <el-row>
            <el-text tag="b" size="large">评论：</el-text>
          </el-row>
          <el-row style="margin-top: 10px;" justify="end">
            <el-input v-model="sharing.newComment" type="textarea" placeholder="说说你的想法："/>
            <el-button type="primary" @click="addComment(sharing.postId, sharing.newComment)">发布</el-button>
          </el-row>
          <el-row>
            <el-col :span="20" :offset="2">
              <el-card shadow="never" v-for="comment in sharing.comments">
                <div slot="header">
                  <el-row align="top">
                    <el-col :span="2">
                      <el-icon :size="35"><UserFilled/></el-icon>
                    </el-col>
                    <el-col :span="10">
                      <el-text>{{ comment.userName }}</el-text><br/>
                      <el-text type="info" size="small">{{ comment.time }}</el-text>
                    </el-col>
                  </el-row>
                </div>
                <el-row align="bottom">
                  <el-col :offset="2" :span="20">
                    <span>{{ comment.comment }}</span>
                  </el-col>
                  <el-col :span="2">
                    <el-button type="info" link @click="clickCommentLike(sharing.postId, comment.commentId, comment.likeIcon)">
                      <el-icon :size="20">
                        <component :is="comment.likeIcon"/>
                      </el-icon>
                      <el-text size="small">{{ comment.likeCount }}</el-text>
                    </el-button>
                  </el-col>
                </el-row>
              </el-card>
            </el-col>
          </el-row>
        </div>
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