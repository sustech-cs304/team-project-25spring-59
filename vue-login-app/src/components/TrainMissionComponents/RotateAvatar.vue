<template>
  <div class="rotate-avatar" @mousemove="handleMouseMove" @mouseleave="resetRotation">
    <img
      class="avatar"
      :style="{ transform: rotationStyle }"
      src="/assets/banner/avatar.webp"
      alt="Avatar"
    />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const rotationStyle = ref('rotate(0deg)')

const handleMouseMove = (e: MouseEvent) => {
  const { clientX: x, clientY: y } = e
  const centerX = window.innerWidth / 2
  const centerY = window.innerHeight / 2

  const deltaX = (x - centerX) / centerX
  const deltaY = (y - centerY) / centerY

  const rotateX = deltaY * 20
  const rotateY = -deltaX * 20

  rotationStyle.value = `rotateX(${rotateX}deg) rotateY(${rotateY}deg)`
}

const resetRotation = () => {
  rotationStyle.value = 'rotate(0deg)'
}
</script>

<style scoped lang="less">
.rotate-avatar {
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
}

.avatar {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  border: 5px solid white;
  object-fit: cover;
  transition: transform 0.3s ease-in-out;
}

/* 鼠标悬停时顺时针旋转 360° */
.avatar:hover {
  transform: rotate(360deg);
}
</style>
