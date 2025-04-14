<template>
  <footer class="footer-menu">
    <!--  1. 灰色背景（圆角平行四边形） -->
    <div class="footer-bg">
      <!--  2. 反向白色装饰（圆角平行四边形） -->
      <div class="footer-decoration"></div>

      <!-- 叠加的图片装饰 -->
      <!-- ✅ 左侧装饰图片 -->
      <img src="../assets/Images/widget/deco-lobby.png" alt="left overlay" class="footer-overlay footer-overlay-left" />

      <!-- ✅ 右侧装饰图片 -->
      <img src="../assets/Images/widget/deco-lobby.png" alt="right overlay" class="footer-overlay footer-overlay-right" />

      <!--  3. 菜单项 -->
      <nav class="footer-nav">
        <ul>
          <li>
            <img src="../assets/Images/icon/Common/cafe.png" alt="训练任务" class="menu-icon" />
            <span @click="handleTrainMissionClick">训练任务</span>
          </li>
          <li>
            <img src="../assets/Images/icon/Common/lesson.png" alt="健身排课" class="menu-icon" />
            <span @click="navigateTo('/about')">健身排课</span>
          </li>
          <li>
            <img src="../assets/Images/icon/Common/students.png" alt="竞技排行" class="menu-icon" />
            <span @click="navigateTo('/services')">竞技排行</span>
          </li>
          <li>
            <img src="../assets/Images/icon/Common/formation.png" alt="社交分享" class="menu-icon" />
            <span @click="navigateTo('/contact')">社交分享</span>
          </li>
          <li>
            <img src="../assets/Images/icon/Common/club.png" alt="Button5" class="menu-icon" />
            <span @click="navigateTo('/trainMission')">Button5</span>
          </li>
          <li>
            <img src="../assets/Images/icon/Common/crafting.png" alt="Button6" class="menu-icon" />
            <span @click="navigateTo('/trainMission')">Button6</span>
          </li>
          <li>
            <img src="../assets/Images/icon/Common/shop.png" alt="Button7" class="menu-icon" />
            <span @click="navigateTo('/trainMission')">Button7</span>
          </li>
          <li>
            <img src="../assets/Images/icon/Common/recruit.png" alt="Button8" class="menu-icon" />
            <span @click="navigateTo('/trainMission')">Button8</span>
          </li>
        </ul>
      </nav>

      <!-- 📌 4. 右侧符号 + 时间 -->
      <div class="footer-right">
        <div class="symbols">△×+○</div>
        <div class="time">{{ currentTime }}</div>
      </div>
    </div>
  </footer>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import axios from 'axios'
import {API_BASE_URL} from "../configs/network_config.js";

const router = useRouter();
const currentTime = ref("");

// **更新当前时间**
const updateTime = () => {
  const now = new Date();
  currentTime.value = now.toLocaleTimeString();
};

// **每秒更新时间**
onMounted(() => {
  updateTime();
  setInterval(updateTime, 1000);
});

// **导航跳转**
const navigateTo = (path) => {
  router.push(path);
};

const handleTrainMissionClick = async () => {
  try {
    const userId = localStorage.getItem('user_id')
    if (!userId) {
      console.error("未找到用户 ID")
      return
    }

    await axios.post(`${API_BASE_URL}/generate-user-records`, {
      user_id: userId
    })
    console.log('${API_BASE_URL}/generate-user-records')
    console.log("成功调用api: /generate-user-records调用对应用户的运动记录")

    router.push('/trainMission') //请求成功后跳转
  } catch (error) {
    console.error("生成用户记录失败:", error)
  }
}
</script>











<style scoped>
/* 📌 整体 Footer 位置 */
.footer-menu {
  position: fixed;
  bottom: 50px;
  left: 50%;
  transform: translateX(-50%);
  width: 95%;
  height: 80px;
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}





.footer-bg{
  width: 100%;
  height: 100%;
  background-color: #dde7f6;
  transform: skewX(-10deg);
  border-radius: 15px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
  position: relative;

}

/* ✅ 覆盖在 footer 背景上的透明图片 */
/* 公共样式：两张图片共有的 */
.footer-overlay {
  position: absolute;
  top: 0;
  height: 100%;
  object-fit: contain;
  z-index: 2;
  pointer-events: none;
}
/* 左侧图片 */
.footer-overlay-left {
  left: 0;
}
/* 右侧图片 */
.footer-overlay-right {
  right: 0;
  transform: scaleX(-1); /* ✅ 水平翻转以镜像左边装饰图（可选） */
}



/* 📌 反向白色装饰（圆角平行四边形） */
.footer-decoration {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 80%;
  height: 100%;
  background-color: white;
  border-radius: 10px;
  transform: skewX(30deg) translate(-50%, -50%);
}

/* 📌 菜单导航 */
.footer-nav {
  position: relative;
  z-index: 10;
  transform: skewX(10deg);
}

.footer-nav ul {
  display: flex;
  gap: 120px; /* 🔹 调整菜单项间距 */
  list-style: none;
  padding: 0;
  margin: 0;
  margin-left: 100px;
  align-items: flex-end; /* 🔹 让文字和图标更贴合 */
}

/* 📌 每个菜单项 */
.footer-nav ul li {
  cursor: pointer;
  color: black;
  font-size: 20px;
  font-weight: bold;
  transition: color 0.3s ease-in-out;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  position: relative;
  font-family: "BlueakaBeta", sans-serif;
}

/* 📌 鼠标悬停颜色 */
.footer-nav ul li span:hover {
  color: #ffd700;
}

/* 📌 菜单项上方的图标 */
.menu-icon {
  width: 60px; /* 🔹 缩小图片 */
  height: auto;
  position: absolute;
  top: -80px; /* 🔹 让图片超出 footer */
  left: 50%;
  transform: translateX(-50%);
}

/* 📌 右侧符号 + 时间 */
.footer-right {
  text-align: right;
  font-size: 18px;
  font-weight: bold;
}

/* 📌 符号（△×+○） */
.symbols {
  font-family: "BlueakaBeta", sans-serif;
  color: #abb3c4;
  font-size: 28px;
  margin-bottom: 5px;
}

/* 📌 时间 */
.time {
  color: #525f72;
  font-size: 24px;
}

@font-face {
  font-family: "BlueakaBeta";
  src: url("../assets/fonts/BlueakaBeta2GBK-Bold.ttf") format("truetype");
  font-weight: normal;
  font-style: normal;
}
</style>
