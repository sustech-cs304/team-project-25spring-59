<script setup>
import { useRouter } from "vue-router"; // 🔹 需要引入 Vue Router
const router = useRouter(); // 🔹 获取 Vue Router 实例

import { onMounted, ref } from 'vue'
import { Spine } from 'pixi-spine'
import * as PIXI from 'pixi.js'
import { sound } from '@pixi/sound'
import FooterMenu from "../components/FooterMenu.vue";
import LevelBox from "../components/LevelBox.vue";
import GridPanel from "../components/GridPanel.vue";
import SpinePlayer from "../components/Spine-Player/index.vue";


// 定义 L2D 资源路径
const spinePath = '/l2d/aris/Aris_home.skel';
const atlasPath = '/l2d/aris/Aris_home.atlas';
const bgmPath = '/l2d/hina_swimsuit/Theme_21.mp3';

// 存储解析后的 Spine 数据
const studentL2D = ref(null);

//右下角跳转DASHBOARD之前播放转业动画的控制变量
const isPlaying = ref(false);
const transitionVideo = ref(null);

// 是否显示“关于”弹窗
const showAbout = ref(false);

onMounted(async () => {
  try {
    // 创建 PixiJS 应用
    const app = new PIXI.Application({
      resizeTo: window, // ⬅️ 让 PixiJS 自动适应浏览器窗口大小
      backgroundAlpha: 0
    });

    const container = document.querySelector('#background');
    if (!container) {
      console.error('❌ 未找到 #background 元素！');
      return;
    }
    container.appendChild(app.view);

    // **加载 Atlas 资源**
    await PIXI.Assets.load(atlasPath).catch(err => {
      console.error('🔥 Atlas 文件加载失败:', err);
      return null;
    });

    // **加载 Spine 资源**
    studentL2D.value = await PIXI.Assets.load(spinePath).catch(err => {
      console.error('🔥 Spine 文件加载失败:', err);
      return null;
    });

    if (!studentL2D.value) {
      console.error('❌ Spine 数据加载失败！');
      return;
    }

    // **确保数据格式正确**
    if (!studentL2D.value.spineData) {
      console.error('❌ Spine 解析失败，spineData 不存在');
      return;
    }

    // 创建 Spine 动画
    const animation = new Spine(studentL2D.value.spineData);
    app.stage.addChild(animation);

    if (animation.state.hasAnimation('Idle_01')) {
      animation.scale.set(0.85);
      animation.state.setAnimation(0, 'Idle_01', true);
      animation.state.timeScale = 1;
      animation.autoUpdate = true;
      animation.y = 1440;
      animation.x = 2560 / 2;
    }

    // **预加载并播放背景音乐**
    sound.add('bgm', {
      url: bgmPath,
      loop: true,
      preload: true
    });
    sound.play('bgm');

  } catch (error) {
    console.error('🔥 发生错误:', error);
  }
});

//右下角播放转页动画
const playTransition = () => {
  isPlaying.value = true;

  // 等待 Vue DOM 更新
  setTimeout(() => {
    transitionVideo.value.play();
    transitionVideo.value.onended = () => {
      isPlaying.value = false;
      router.push("/dashboard"); // 播放完跳转
    };
  }, 100); // 确保 DOM 渲染完成
};

//右上角内容
const infoItems = ref([
  { image: "img/ap.png", text: "267/266" },
  { image: "img/gold.png", text: "114,514" },
  { image: "img/pyroxene.png", text: "24,000" }
]);
</script>




<template>
  <div id="background"></div>

  <div class="main-container">
    <LevelBox /> <!--  左上角的等级组件 -->

    <router-view />
    <!-- 底部状态栏 -->
    <FooterMenu />

    <!--  左上角的四宫格组件 -->
    <GridPanel class="grid-panel-fixed" />


    <!--  右下角按钮容器 -->
    <div class="switch-wrapper" @click="playTransition">
      <img
        src="../../public/task.png"
        alt="切换按钮"
        class="switch-button"
      />
      <div class="switch-label">训练数据</div>
    </div>

    <!--  按钮左侧图标，单独存在 -->
    <img
      src="../assets/Images/icon/Common/event.png"
      alt="左侧图标"
      class="left-of-switch"
    />

    <!--  按钮左侧图标，单独存在 -->
    <img
      src="../assets/Images/widget/Enter/60000_Jp.png"
      alt="右侧图标"
      class="under-right-component"
    />


    <!--  按钮左侧图标，单独存在 -->
    <img
      src="../assets/Images/widget/Banner/50000_Jp.png"
      alt="左下banner"
      class="activity-banner"
    />



    <!-- 过渡动画（默认隐藏） -->
    <div v-if="isPlaying" class="transition-overlay">
      <video ref="transitionVideo" class="transition-video" playsinline>
        <source src="../../public/transfrom.webm" type="video/webm" />
      </video>
    </div>

    <!-- 📌 右上角信息框容器 -->
    <div class="info-box-container">
      <div class="info-box" v-for="(item, index) in infoItems" :key="index">
        <img :src="item.image" alt="Info Image" class="info-image" />
        <p class="info-text">{{ item.text }}</p>
      </div>

      <!-- 🔹 新增：右侧信息栏（带感叹号） -->
      <div class="info-box alert-box" @click="showAbout = true">
        <div class="alert-circle">!</div>
      </div>
    </div>

     <!-- 📌 弹窗 (Modal) -->
    <div v-if="showAbout" class="modal-overlay">
      <div class="modal-content">
        <!-- 🔹 头部（标题 + 关闭按钮） -->
        <div class="modal-header">
          <h2>关于</h2>
          <span class="close-button" @click="showAbout = false">×</span>
        </div>
        <hr />

        <!-- 🔹 主体 -->
        <div class="modal-body">
          <p>本项目由111111111111111团队开发，致力于.........。</p>
        </div>

        <!-- 🔹 底部 -->
        <div class="modal-footer">
          <p>项目成员：1, 2, 3, 4, 5</p>
          <p>发布地址：www.baidu.com</p>
        </div>
      </div>

    </div>
  </div>
</template>



<style scoped>
@font-face {
  font-family: "BlueakaBeta";
  src: url("../assets/fonts/BlueakaBeta2GBK-Bold.ttf") format("truetype");
  font-weight: normal;
  font-style: normal;
}

#background {
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  z-index: -1;
}

/* 📌 确保页面下方留出空间 */
.main-container {
  padding-bottom: 200px; /* 确保不遮挡内容 */
}

/* 字体 */
@font-face {
  font-family: TVPS-Vain-Capital-2;
  src: url(https://webcnstatic.yostar.net/ba_cn_web/prod/web/assets/TVPS-Vain-Capital-2.cca90a05.ttf);
}

/* 📌 右下角按钮样式 */
.switch-button {
  position: fixed;
  bottom: 180px;
  right: 30px;
  width: 150px;
  height: 150px;
  cursor: pointer;
  transition: transform 0.3s ease-in-out;
}

.switch-button:hover {
  transform: scale(1.1);
}
/* ✅ 整个按钮 + 文字容器 */
.switch-wrapper {
  position: fixed;
  bottom: 180px;
  right: 30px;
  display: flex;
  flex-direction: column;
  align-items: center;
  cursor: pointer;
  z-index: 999;
}

/* ✅ 说明文字 */
.switch-label {
  position: absolute;
  left: -110px;
  font-size: 20px;
  color: #ffffff;
  font-weight: bold;
  font-family: "BlueakaBeta", sans-serif;
}


/*  单独添加在按钮左侧的图片 */
.left-of-switch {
  position: fixed;
  bottom: 180px;  /* 跟按钮对齐，可微调 */
  right: 170px;   /* 控制它离右边有多远，贴近按钮左边 */
  width: 150px;
  height: auto;
  z-index: 998;
  pointer-events: none; /* 不干扰鼠标点击 */
}

/*  添加在右上角的图片 */
.under-right-component {
  position: fixed;
  bottom: 800px;  /* 跟按钮对齐，可微调 */
  right: 0px;   /* 控制它离右边有多远，贴近按钮左边 */
  width: 200px;
  height: auto;
  z-index: 998;
  pointer-events: none; /* 不干扰鼠标点击 */
}

/*  添加在左下角的banner的样式 */
.activity-banner {
  position: fixed;
  bottom: 200px;  /* 跟按钮对齐，可微调 */
  left:80px;   /* 控制它离右边有多远，贴近按钮左边 */
  width: 450px;
  height: auto;
  z-index: 998;
  pointer-events: none; /* 不干扰鼠标点击 */
}







/* 📌 过渡动画遮罩 */
.transition-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10000; /* 最高层级，保证在 UI 之上 */
  pointer-events: none; /* 允许点击穿透，避免影响交互 */
  background: none; /* ✅ 移除黑色背景，防止遮盖 */
}

/* 📌 过渡视频 */
.transition-video {
  width: 100vw;
  height: 100vh;
  object-fit: cover;
}


/* 📌 右上角信息框整体布局 */
.info-box-container {
  position: fixed;
  top: 60px;
  right: 20px;
  display: flex;
  flex-direction: row;
  gap: 15px;
  z-index: 1000;
}

/* 📌 圆角平行四边形框 */
.info-box {
  width: 300px; /* ✅ 调整宽度 */
  height: 50px; /* ✅ 调整高度 */
  background-color: #e6e5f0;
  display: flex;
  align-items: center;
  justify-content: flex-start; /* ✅ 让内容靠左 */
  padding-left: 15px; /* ✅ 让整个内容（图片+文字）离左边远一些 */
  padding: 5px;
  box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.2);
  transition: transform 0.3s ease-in-out;
  position: relative;
  border-radius: 12px; /* ✅ 添加圆角 */

  /* ✅ 使用伪元素模拟圆角平行四边形 */
  clip-path: polygon(5% 0%, 100% 0%, 95% 100%, 0% 100%);
}
.info-box:hover {
  transform: scale(1.05);
}

/* 📌 里面的图片 */
.info-image {
  width: 50px;
  height: 50px;
  margin-left: 20px;
}

/* 📌 文字 */
.info-text {
  font-size: 30px; /* ✅ 让文字更大 */
  font-weight: 500; /* ✅ 让文字不要太粗（比 bold 轻） */
  color: #333;
  text-align: left; /* ✅ 让文字靠左对齐（可以改成 right 或 center） */
}

/* 📌 右侧较短的感叹号框 */
.alert-box {
  width: 80px; /* ✅ 保持较短的宽度 */
  height: 50px; /* ✅ 与 `info-box` 相同的高度 */
  background-color: #e6e5f0;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.2);
  transition: transform 0.3s ease-in-out;
  position: relative;
  border-radius: 12px; /* ✅ 保持圆角 */
  /* ✅ 让它的倾斜度与 `info-box` 一致 */
  transform: skewX(-10deg);
}

.alert-box:hover {
  transform: scale(1.05);
}

/* 📌 感叹号圈 */
.alert-circle {
  font-size: 24px;
  font-weight: bold;
  color: #214b6a;
  border-radius: 50%;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 5px rgb(33, 75, 106);
}


/* 📌 弹窗遮罩层 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.5); /* 半透明黑色背景 */
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10000;
}

/* 📌 弹窗内容 */
.modal-content {
  width: 400px;
  background: white;
  border-radius: 15px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
  padding: 20px;
  text-align: center;
  animation: fadeIn 0.3s ease-in-out;
}

/* 📌 头部 */
.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 22px;
  font-weight: bold;
}

/* 📌 关闭按钮 */
.close-button {
  cursor: pointer;
  font-size: 28px;
  font-weight: bold;
  color: #ff4d4d;
  transition: 0.3s;
}

.close-button:hover {
  color: #cc0000;
}

/* 📌 分割线 */
hr {
  border: none;
  border-top: 1px solid #ccc;
  margin: 10px 0;
}

/* 📌 主体 */
.modal-body {
  font-size: 16px;
  color: #333;
  padding: 15px 0;
}

/* 📌 底部 */
.modal-footer {
  font-size: 14px;
  color: #666;
  text-align: center;
  padding-top: 10px;
}

/* 左上角四宫格ui的样式 */
.grid-panel-fixed {
  position: fixed;
  top: 150px;
  left: -50px;
  z-index: 999;
  width: 400px; /* 可以自定义宽度 */
}



</style>