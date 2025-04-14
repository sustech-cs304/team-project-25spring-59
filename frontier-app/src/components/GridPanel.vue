<template>
  <div class="grid-container">
    <div
      v-for="(item, index) in items"
      :key="index"
      class="grid-item"
    >
      <!-- ✅ 图片容器：透明背景 -->
      <div class="image-box">
        <img :src="item.image" :alt="item.title" class="grid-image" />
      </div>

      <!-- 图片下方文字 -->
      <p class="grid-title">{{ item.title }}</p>
    </div>
  </div>
</template>

<script setup>
const items = [
  {
    image: new URL('/Images/icon/Common/notice.png', import.meta.url).href,
    title: "图片说明 1",
    buttonText: "进入功能 1",
    action: () => alert("点击了功能 1"),
  },
  {
    image: new URL('/Images/icon/Common/momotalk.png', import.meta.url).href,
    title: "图片说明 2",
    buttonText: "进入功能 2",
    action: () => alert("点击了功能 2"),
  },
  {
    image: new URL('/Images/icon/Common/schedule.png', import.meta.url).href,
    title: "图片说明 3",
    buttonText: "进入功能 3",
    action: () => alert("点击了功能 3"),
  },
  {
    image: new URL('/Images/icon/Common/store.png', import.meta.url).href,
    title: "图片说明 4",
    buttonText: "进入功能 4",
    action: () => alert("点击了功能 4"),
  },
];
</script>

<style scoped>
.grid-container {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;
  max-width: 800px;
  margin: 0 auto;
  padding: 40px;
}

.grid-item {
  padding: 10px;
  border-radius: 16px;
  text-align: center;
}

/* ✅ 新增：包裹图片的 div，确保无背景色 */
.image-box {
  background: transparent;
}

/* ✅ 图片样式 */
.grid-image {
  width: 80px;
  height: auto;
  object-fit: contain; /* 或 cover，根据图片实际效果可调整 */
  border-radius: 12px;
}

/* 标题文字 */
.grid-title {
  font-size: 20px;
  margin: 5px;
  text-align: center;
  color: #000000;
  font-weight: 500;
}

</style>
