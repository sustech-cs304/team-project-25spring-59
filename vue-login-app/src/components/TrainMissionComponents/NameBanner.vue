<template>
  <div class="name-banner">
    <!-- 主要标题区域 -->
    <div class="title">
      <h1>Hello, Sensei</h1>
    </div>

    <!-- 用户信息区域 -->
    <div class="info-box" @mousemove="boxMove" @mouseleave="resetBox" :style="boxStyle">
      <!-- 圆形头像 -->
<!--      <img class="avatar" :style="{ transform: avatarRotation }" src="/assets/banner/avatar.webp" alt="Avatar" />-->

      <!-- 用户信息文本 -->
      <div class="text">
        <h2>Sensei‘s Train Missions</h2>
        <p>何気ない日常で、ほんの少しの奇跡を見つける物语。</p>
      </div>
    </div>

    <RotateAvatar/>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import RotateAvatar from "./RotateAvatar.vue";

// 用来控制盒子的动画
const boxStyle = ref({
  transform: 'scale(1)',
  transition: 'transform 0.3s ease, box-shadow 0.3s ease',
  boxShadow: '0 4px 12px rgba(0, 0, 0, 0.1)',
})

// 鼠标位置和旋转控制
const avatarRotation = ref('rotate(0deg)')

const boxMove = (e: MouseEvent) => {
  const box = e.currentTarget as HTMLElement
  const { left, top, width, height } = box.getBoundingClientRect()
  const x = e.clientX - left
  const y = e.clientY - top

  const rotateX = (y - height / 2) / (height / 2) * 10
  const rotateY = -(x - width / 2) / (width / 2) * 10

  avatarRotation.value = `rotateX(${rotateX}deg) rotateY(${rotateY}deg)`

  boxStyle.value = {
    transform: 'scale(1.05)',
    boxShadow: '0 8px 24px rgba(0, 0, 0, 0.2)',
    transition: 'transform 0.3s ease, box-shadow 0.3s ease',
  }
}

const resetBox = () => {
  boxStyle.value = {
    transform: 'scale(1)',
    boxShadow: '0 4px 12px rgba(0, 0, 0, 0.1)',
    transition: 'transform 0.3s ease, box-shadow 0.3s ease',
  }
}
</script>

<style scoped lang="less">
/* NameBanner 样式 */
.name-banner {
  position: absolute;
  top: 100px; /* 调整 top 值，移动 NameBanner */
  width: 100%;
  z-index: 2; /* 保证在 Banner 上方 */
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-top: 20px;
  color: white;
}

/* 大字 Hello, Sensei */
.title h1 {
  font-size: 4vw;
  font-weight: bold;
  text-shadow: 3px 3px 5px rgba(0, 0, 0, 0.5);
  margin-bottom: 80px; /* 增加与下面内容的距离 */
  user-select: none;
}

/* 用户信息区域 - 使用磨砂玻璃背景，调大宽度并居中 */
.info-box {
  position: relative;
  background: rgba(255, 255, 255, 0.1); /* 半透明背景 */
  border-radius: 20px;
  padding: 15px;
  width: 40%; /* 调大宽度 */
  height: 250px; /* 增大高度，确保头像能突出 */
  box-shadow: 0 0 15px rgba(0, 0, 0, 0.5);
  text-align: center;
  margin-bottom: 20px;
  backdrop-filter: blur(10px); /* 磨砂效果 */
  display: flex;
  flex-direction: column;
  align-items: center; /* 使内容居中 */
  transition: transform 0.3s ease, box-shadow 0.3s ease; /* 添加过渡效果 */
}

///* 圆形头像 - 使一部分头像在外面 */
//.avatar {
//  width: 120px; /* 增大头像尺寸 */
//  height: 120px; /* 增大头像尺寸 */
//  border-radius: 50%;
//  border: 5px solid white;
//  margin-bottom: 10px;
//  object-fit: cover;
//  position: absolute;
//  top: -60px; /* 把头像的一部分放到矩形外面 */
//  left: calc(50% - 50px);
//  transform: translateX(-50%); /* 这确保头像水平居中 */
//  z-index: 1; /* 头像放在矩形外面 */
//  transition: transform 0.3s ease-in-out; /* 旋转动画 */
//}

/* 文本内容 */
.text {
  margin-top: 100px; /* 增加顶部间距，使得文本远离头像 */
}

/* 文本标题 */
.text h2 {
  font-size: 2vw;
  font-weight: bold;
  margin-bottom: 10px;
}

.text p {
  font-size: 1.2vw;
  font-weight: normal;
  color: #000000;
  margin-bottom: 20px;
}

/* 响应式调整 */
//@media (max-width: 768px) {
//  .title h1 {
//    font-size: 8vh;
//  }
//
//  .info-box {
//    width: 85%;
//    padding: 15px;
//    height: 200px; /* 短小的高度适应小屏 */
//  }
//
//  .avatar {
//    width: 20vh;
//    height: 20vh;
//    top: -10vh; /* 调整头像位置 */
//  }
//
//  .text h2 {
//    font-size: 4vh;
//  }
//
//  .text p {
//    font-size: 2vh;
//  }
//}
</style>
