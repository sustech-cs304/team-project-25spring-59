<template>
  <div class="container">
    <!-- 左上角返回按钮 -->
    <el-button class="back-button" type="primary" @click="goToDashboard">
      返回仪表盘
    </el-button>

    <!-- 右上角登出按钮 -->
    <el-button class="logout-button" type="danger" @click="logout">
      登出
    </el-button>

    <div
      class="shell"
      @mousedown="startDrag"
      @mousemove="onDrag"
      @mouseup="endDrag"
      @mouseleave="endDrag"
    >
      <div
        class="content"
        :style="{ transform: `translateZ(-50vw) rotateY(${currentRotation}deg)` }"
      >
        <div class="item" @click="goToTrainMission">
          <div class="text">训练任务</div>
        </div>
        <div class="item" @click="goToDetail(2)">
          <div class="text">图片详情 2</div>
        </div>
        <div class="item" @click="goToDetail(3)">
          <div class="text">图片详情 3</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useRouter } from 'vue-router';

export default {
  data() {
    return {
      startX: 0,
      currentRotation: 0,
      isDragging: false,
      canRotate: true,
    };
  },
  setup() {
    const router = useRouter();

    // 点击图片跳转详情页面
    const goToDetail = (id) => {
      router.push(`/image/${id}`);
    };

    // 点击按钮跳转到 Dashboard
    const goToDashboard = () => {
      router.push('/dashboard');
    };

    // 点击图片跳转详情页面
    const goToTrainMission = () => {
      router.push(`/trainMission`);
    };

    // 登出方法
    const logout = () => {
      sessionStorage.removeItem('token');  // 删除 sessionStorage 中的 token
      router.push('/login'); // 跳转到登录页面
    };

    return { goToDetail, goToDashboard, goToTrainMission, logout };
  },
  methods: {
    startDrag(event) {
      this.startX = event.clientX;
      this.isDragging = true;
      this.canRotate = true;
    },
    onDrag(event) {
      if (!this.isDragging || !this.canRotate) return;
      const deltaX = event.clientX - this.startX;
      if (Math.abs(deltaX) > 100) {
        this.currentRotation += deltaX > 0 ? 120 : -120;
        this.canRotate = false;
      }
    },
    endDrag() {
      this.isDragging = false;
      this.canRotate = true;
    },
  }
};
</script>

<style scoped>
/* 全局容器 */
.container {
  position: relative;
  width: 100vw;
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background-image: linear-gradient(to top, #9795f0 0%, #fbc8d4 100%);
  overflow: hidden;
}

/* 返回按钮 */
.back-button {
  position: absolute;
  top: 20px;
  left: 20px;
  z-index: 10;
}

/* 登出按钮 */
.logout-button {
  position: absolute;
  top: 20px;
  right: 20px;
  z-index: 10;
}

/* 轮播图 */
.shell {
  position: absolute;
  width: 80vw;
  height: 55vw;
  max-width: 600px;
  max-height: 400px;
  perspective: 1200px;
}

/* 3D 轮播内容 */
.content {
  display: flex;
  justify-content: center;
  align-items: center;
  position: absolute;
  width: 100%;
  height: 100%;
  transform-origin: center;
  transform-style: preserve-3d;
  transition: transform 0.5s ease-out;
}

/* 图片卡片 */
.item {
  position: absolute;
  width: 80vw;
  height: 55vw;
  max-width: 600px;
  max-height: 400px;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.3);
  border-radius: 8px;
  background-size: cover;
  cursor: pointer;
  background-color: white; /* 改为纯白背景, 需要图片的话把这一行注释掉 */
}

/* 文字框 */
.text {
  font-size: 24px;
  font-weight: bold;
  color: #333;
  text-align: center;
  padding: 10px;
}

/* 轮播图三张图片 */
.item:nth-child(1) {
  //background-image: url('/01.jpg');
  transform: rotateY(0) translateZ(50vw);
}

.item:nth-child(2) {
  //background-image: url('/01.jpg');
  transform: rotateY(120deg) translateZ(50vw);
}

.item:nth-child(3) {
  //background-image: url('/01.jpg');
  transform: rotateY(240deg) translateZ(50vw);
}
</style>
