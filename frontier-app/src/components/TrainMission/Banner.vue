<template>
  <div class="banner" :style="`background-image: url(${props.cover})`">
    <div class="wave1"></div>
    <div class="wave2"></div>
    <div class="info">
      <GlitchText :text="hello" />
      <span
        class="box"
        ref="boxRef"
        @mousemove="parallax"
        @mouseleave="reset"
        :style="{ transform: `perspective(1000px) rotateY(${calcY}deg) rotateX(${calcX}deg)` }"
      >
        <p class="highText">
          {{ highText }}
        </p>

        <p class="text">
          {{ motto }}
          <span class="pointer"></span>
        </p>
        <div class="contact">
          <a :href="s.url" v-for="s in social" aria-label="icon" target="_blank">
            <i :class="['fab', s.icon]"></i>
          </a>
        </div>
      </span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, defineProps } from 'vue'
import GlitchText from './GlitchText.vue'

const props = defineProps<{
  cover: string
  hello?: string
  highText?: string
  motto?: string
  social?: { icon: string; url: string }[]
}>()

const boxRef = ref<HTMLElement | null>(null)
const calcY = ref(0)
const calcX = ref(0)
const multiple = 20

const parallax = (e: MouseEvent) => {
  if (boxRef.value) {
    const box = boxRef.value.getBoundingClientRect()
    const centerX = box.x + box.width / 2
    const centerY = box.y + box.height / 2
    const offsetX = (e.clientX - centerX) / multiple
    const offsetY = (e.clientY - centerY) / multiple

    calcY.value = offsetX
    calcX.value = -offsetY
  }
}

const reset = () => {
  calcX.value = calcY.value = 0
}

// 打字效果
let index = 0
const motto = ref('')
const mottoFull = props.motto || '何気ない日常で、ほんの少しの奇跡を見つける物語。'

const startTypingEffect = () => {
  if (index < mottoFull.length) {
    motto.value += mottoFull[index]
    index++
    setTimeout(startTypingEffect, Math.random() * 150 + 50)
  }
}

onMounted(() => {
  startTypingEffect()
})

</script>

<style lang="scss">

.banner {
  width: 100vw;            /* 覆盖整个宽度 */
  height: 100vh;           /* 高度覆盖整个视口高度 */
  background-repeat: no-repeat;
  background-position: center top;
  background-size: cover;  /* 背景图等比填充，可能会裁剪 */
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 0;
  padding: 0;

  .wave1,
  .wave2 {
    position: absolute;
    width: 400%;
    bottom: 0;
  }

  .wave1 {
    background: url("../../assets/TrainMissionAssets/wave1.png") repeat-x;
    height: 65px;
    animation: wave-animation-1 30s infinite linear;
  }

  .wave2 {
    background: url("../../assets/TrainMissionAssets/wave2.png") repeat-x;
    height: 80px;
    animation: wave-animation-2 20s infinite linear;
  }

  .info {
    font-family: Arial, Helvetica, sans-serif;
    font-weight: bold;
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  .box {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    width: 1000px;
    height: 400px;
    padding: 20px;
    color: black;
    border-radius: 60px;
    text-align: center;
    background-color: rgba(255, 255, 255, 0.3);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    transition: transform 0.1s ease-out;
    will-change: transform;
  }

  .highText {
    text-align: center;
    font-size: 60px; /* 你可以调整字体大小 */
    font-weight: bold; /* 让字体更醒目 */
    line-height: 1.2; /* 适当增加行高 */
    color: rgba(0, 0, 0, 0.6); /* 你可以更改颜色 */
  }


  .text {
    text-align: center;
    font-size: 30px;
    line-height: 24px;
  }

  .contact {
    display: flex;
    justify-content: center;
    font-size: 24px;
    padding-bottom: 12px;

    a {
      color: white;
      margin: 6px;
    }
  }

  .text {
  text-align: center;
  font-size: 30px;
  line-height: 24px;
  position: relative; /* 确保光标正确定位 */
}

/* 光标动画 */
.pointer {
  display: inline-block;
  width: 6px; /* 光标宽度 */
  height: 1.2em; /* 让光标与文本高度匹配 */
  background-color: black; /* 光标颜色 */
  margin-left: 5px; /* 与文字保持距离 */
  vertical-align: middle; /* 保持居中 */
  animation: blink 0.8s infinite; /* 让光标闪烁 */
}

/* 闪烁动画 */
@keyframes blink {
  0%, 40% {
    opacity: 1;
  }
  60%, 100% {
    opacity: 0;
  }
}

}

@media (max-width: 720px) {
  .banner {
    .info {
      margin: 0 0.5em;
    }

    .box {
      width: 100%;
    }

    .text {
      margin: 1em 0.5em;
    }
  }
}

@keyframes wave-animation-1 {
  0% {
    left: 0;
  }

  100% {
    left: -997px;
  }
}

@keyframes wave-animation-2 {
  0% {
    left: 0;
  }

  100% {
    left: -1009px;
  }
}
</style>
