<script setup>
import {onMounted, reactive, ref, markRaw} from "vue";
import {Plus, UserFilled, ChatDotRound, Star, StarFilled, Sort} from "@element-plus/icons-vue";
import request, {baseurl} from "../../utils/request.js";
import {ElMessage} from "element-plus";

defineEmits(['createShare'])

const sharings = reactive({data: []});
const userId = Number(localStorage.getItem('user_id'))
const postSortType = ref('latest') // 'latest' 或 'hot'
const commentSortTypes = reactive({}) // 存储每个帖子的评论排序方式

function processData(data) {
  sharings.data = data;
  sortPosts();
  sharings.data.forEach((sharing)=>{
    // 初始化每个帖子的评论排序方式
    if (!commentSortTypes[sharing.postId]) {
      commentSortTypes[sharing.postId] = 'latest'
    }
    sortComments(sharing);
    sharing.commentCount = sharing.comments.length;
    sharing.newComment = "";
    sharing.showComment = false;
    sharing.showWriteCommentArea = false;
    sharing.imgList = Array.from(sharing.imgList, ({ img })=>baseurl+img)
    sharing.likeIcon = sharing.likeList.indexOf(userId) !== -1 ? markRaw(StarFilled) : markRaw(Star)
    sharing.comments.forEach((comment)=>{
      comment.likeIcon = comment.likeList.indexOf(userId) !== -1 ? markRaw(StarFilled) : markRaw(Star)
    })
  });
}

// 排序帖子
function sortPosts() {
  if (postSortType.value === 'latest') {
    sharings.data.sort((a,b) => new Date(b.time) - new Date(a.time));
  } else {
    sharings.data.sort((a,b) => (b.likeCount + b.commentCount * 2) - (a.likeCount + a.commentCount * 2));
  }
}

// 排序评论
function sortComments(sharing) {
  if (commentSortTypes[sharing.postId] === 'latest') {
    sharing.comments.sort((a,b) => new Date(b.time) - new Date(a.time));
  } else {
    sharing.comments.sort((a,b) => b.likeCount - a.likeCount);
  }
}

// 切换帖子排序方式
function togglePostSort() {
  postSortType.value = postSortType.value === 'latest' ? 'hot' : 'latest';
  sortPosts();
}

// 切换评论排序方式
function toggleCommentSort(postId) {
  commentSortTypes[postId] = commentSortTypes[postId] === 'latest' ? 'hot' : 'latest';
  const sharing = sharings.data.find(s => s.postId === postId);
  if (sharing) sortComments(sharing);
}

function addComment(postId, comment) {
  if (!comment.trim()) {
    ElMessage({message: '评论内容不能为空', type: 'warning'})
    return;
  }

  request({
    method: "POST",
    url: `/posts/${postId}/comments`,
    data: {
      userId: localStorage.getItem('user_id'),
      comment: comment,
    },
  }).then((response)=>{
    ElMessage({message: '评论成功', type: 'success'})
    window.location.reload()
  }).catch((error)=>{
    ElMessage({message: '评论失败', type: 'error'})
    console.log(error)
  })
}

function clickLike(postId, icon) {
  const sharing = sharings.data.find((sharing)=>sharing.postId === postId)
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
    <el-col :span="16" :offset="4">
      <!-- 帖子排序按钮 -->
      <div class="sort-controls">
        <el-button
            type="primary"
            plain
            @click="togglePostSort"
            class="sort-btn"
        >
          <el-icon><Sort /></el-icon>
          <span>{{ postSortType === 'latest' ? '最新' : '最热' }}</span>
        </el-button>
      </div>

      <el-card
          shadow="never"
          v-for="sharing in sharings.data"
          class="sharing-card"
      >
        <div class="card-header">
          <el-row align="middle" :gutter="10">
            <el-col :span="2">
              <el-avatar :size="40">
                <el-icon :size="25"><UserFilled/></el-icon>
              </el-avatar>
            </el-col>
            <el-col :span="18">
              <div class="user-info">
                <el-text class="username">{{ sharing.userName }}</el-text>
                <el-text class="post-time" type="info">{{ sharing.time }}</el-text>
              </div>
            </el-col>
          </el-row>
        </div>

        <div class="card-content">
          <p class="content-text">{{ sharing.content }}</p>
          <div v-for="url in sharing.imgList" style="display: inline-block">
            <el-image
                style="width: 100px; height: 100px; margin: 1px"
                :src="url"
                fit="cover"
                :preview-src-list="sharing.imgList"
            />
          </div>
        </div>

        <div class="card-actions">
          <el-button
              type="text"
              class="action-btn"
              @click="sharing.showComment=!sharing.showComment"
          >
            <el-icon :size="18"><ChatDotRound/></el-icon>
            <span class="action-count">{{ sharing.commentCount }}</span>
          </el-button>
          <el-button
              type="text"
              class="action-btn"
              @click="clickLike(sharing.postId, sharing.likeIcon)"
          >
            <el-icon :size="18">
              <Component :is="sharing.likeIcon"/>
            </el-icon>
            <span class="action-count">{{ sharing.likeCount }}</span>
          </el-button>
        </div>

        <div class="comment-section" v-show="sharing.showComment">
          <el-divider />
          <div class="comment-sort-controls">
            <el-button
                type="text"
                size="small"
                @click="toggleCommentSort(sharing.postId)"
                class="comment-sort-btn"
            >
              <el-icon><Sort /></el-icon>
              <span>{{ commentSortTypes[sharing.postId] === 'latest' ? '最新' : '最热' }}</span>
            </el-button>
          </div>
          <div class="comment-input-area">
            <el-input
                v-model="sharing.newComment"
                type="textarea"
                placeholder="说说你的想法..."
                :rows="2"
                resize="none"
                class="comment-input"
            />
            <el-button
                type="primary"
                size="small"
                @click="addComment(sharing.postId, sharing.newComment)"
                class="comment-submit-btn"
            >
              发布
            </el-button>
          </div>

          <div class="comments-list">
            <div class="comment-item" v-for="comment in sharing.comments">
              <el-row align="middle" :gutter="10">
                <el-col :span="2">
                  <el-avatar :size="32">
                    <el-icon :size="18"><UserFilled/></el-icon>
                  </el-avatar>
                </el-col>
                <el-col :span="18">
                  <div class="comment-info">
                    <el-text class="comment-username">{{ comment.userName }}</el-text>
                    <el-text class="comment-time" type="info">{{ comment.time }}</el-text>
                  </div>
                  <p class="comment-content">{{ comment.comment }}</p>
                </el-col>
                <el-col :span="4" class="comment-like">
                  <el-button
                      type="text"
                      size="small"
                      @click="clickCommentLike(sharing.postId, comment.commentId, comment.likeIcon)"
                  >
                    <el-icon :size="14">
                      <component :is="comment.likeIcon"/>
                    </el-icon>
                    <span class="action-count">{{ comment.likeCount }}</span>
                  </el-button>
                </el-col>
              </el-row>
              <el-divider class="comment-divider" />
            </div>
          </div>
        </div>
      </el-card>
    </el-col>
  </el-row>

  <!-- Floating action button -->
  <el-affix target=".sharing-container" position="bottom" :offset="20">
    <el-button
        :icon="Plus"
        type="primary"
        size="large"
        circle
        class="create-btn"
        @click="$emit('createShare')"
    />
  </el-affix>
</template>

<style scoped>
.sharing-container {
  padding: 20px 0;
  background-color: #f5f7fa;
  min-height: 100vh;
}

.sharing-card {
  margin-bottom: 20px;
  border-radius: 12px;
  border: none;
  transition: all 0.3s ease;
}

.card-header {
  padding: 15px 0;
  border-bottom: 1px solid #f0f2f5;
}

.user-info {
  display: flex;
  flex-direction: column;
}

.username {
  font-size: 16px;
  font-weight: 500;
  margin-bottom: 2px;
}

.post-time {
  font-size: 12px;
}

.card-content {
  padding: 15px 0;
}

.content-text {
  font-size: 15px;
  line-height: 1.6;
  margin-bottom: 15px;
  color: #333;
}

.image-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  gap: 8px;
  margin-top: 10px;
}

.post-image {
  width: 100%;
  height: 120px;
  border-radius: 6px;
  cursor: pointer;
  transition: transform 0.3s;
}

.post-image:hover {
  transform: scale(1.02);
}

.card-actions {
  display: flex;
  align-items: center;
  padding: 10px 0;
}

.action-btn {
  margin-right: 20px;
  color: #606266;
}

.action-btn:hover {
  color: #409eff;
}

.action-count {
  margin-left: 5px;
  font-size: 14px;
}

.comment-section {
  margin-top: 10px;
}

.comment-input-area {
  display: flex;
  margin-bottom: 15px;
}

.comment-input {
  flex: 1;
  margin-right: 10px;
}

.comment-submit-btn {
  align-self: flex-end;
  height: 60px;
}

.comments-list {
  margin-top: 10px;
}

.comment-item {
  margin-bottom: 10px;
}

.comment-info {
  display: flex;
  align-items: center;
  margin-bottom: 5px;
}

.comment-username {
  font-size: 14px;
  font-weight: 500;
  margin-right: 10px;
}

.comment-time {
  font-size: 12px;
}

.comment-content {
  font-size: 14px;
  line-height: 1.5;
  color: #333;
  margin: 0;
}

.comment-divider {
  margin: 10px 0;
}

.create-btn {
  width: 56px;
  height: 56px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  background-color: #409eff;
  color: white;
  position: fixed;
  right: 40px;
  bottom: 40px;
}

.create-btn:hover {
  background-color: #66b1ff;
  transform: scale(1.05);
}
</style>