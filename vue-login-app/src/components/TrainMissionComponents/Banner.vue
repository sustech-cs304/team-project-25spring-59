<template>
  <div class="banner">
    <canvas id="wave"></canvas>
    <div class="bg-img"></div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'

class WaveEffect {
  constructor() {
    this.K = 1;
    this.F = 15;
    this.speed = 0.1;
    this.noise = 30;
    this.phase = 0;
    this.devicePixelRatio = window.devicePixelRatio || 1;
    this.width = this.devicePixelRatio * window.innerWidth;
    this.height = this.devicePixelRatio * 100;
    this.MAX = this.height / 2;
    this.canvas = document.getElementById('wave');
    this.canvas.width = this.width;
    this.canvas.height = this.height;
    this.canvas.style.width = this.width / this.devicePixelRatio + 'px';
    this.canvas.style.height = this.height / this.devicePixelRatio + 'px';
    this.ctx = this.canvas.getContext('2d');
    this.run = false;
    this.animationFrameID = null;
  }

  _drawLine(attenuation, color, width, noise, F) {
    this.ctx.beginPath();
    this.ctx.moveTo(0, this.height / 2); // 从画布中间开始

    this.ctx.lineWidth = width || 1;
    noise = noise * this.MAX || this.noise;

    // 绘制波浪线
    for (let i = -this.K; i <= this.K; i += 0.01) {
      const x = this.width * ((i + this.K) / (this.K * 2));
      const y =
        this.height / 2 +
        noise * Math.sin(i * 10 * attenuation) * Math.sin(F * i - this.phase);
      this.ctx.lineTo(x, y);
    }

    // 填充颜色区域：从波浪线的底部到图片底部
    this.ctx.lineTo(this.width, this.height); // 到画布底部
    this.ctx.lineTo(0, this.height); // 从另一边返回
    this.ctx.closePath();

    // 填充波浪区域，使用 rgba(234, 239, 245, 0.3) 颜色
    this.ctx.fillStyle = color;
    this.ctx.fill();
  }

  _clear() {
    this.ctx.clearRect(0, 0, this.width, this.height);
  }

  _draw() {
    if (!this.run) return;
    this.phase = (this.phase + this.speed) % (Math.PI * 64);
    this._clear();
    this._drawLine(0.5, 'rgba(234, 239, 245, 0.3)', 2, 0.35, 6);
    this._drawLine(1, 'rgba(234, 239, 245, 0.6)', 2, 0.25, 6);
    this.animationFrameID = requestAnimationFrame(this._draw.bind(this));
  }

  start() {
    this.run = true;
    this._draw();
  }

  stop() {
    this.run = false;
    if (this.animationFrameID !== null) {
      cancelAnimationFrame(this.animationFrameID);
      this.animationFrameID = null;
    }
  }
}

let waveInstance = null;

onMounted(() => {
  waveInstance = new WaveEffect();
  waveInstance.start();
  window.addEventListener('resize', () => {
    waveInstance.stop();
    waveInstance = new WaveEffect();
    waveInstance.start();
  });
});
</script>

<style scoped>
.banner {
  position: absolute;
  top: 0;
  width: 100%;
  height: 75vh;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  background-size: cover;
  background-position: center;
}

.bg-img {
  background-image: url('/assets/banner/banner.webp');
  position: absolute;
  top: 0;
  width: 100%;
  height: 100%;
  background-size: cover;
  background-position: center;
  z-index: -1;
}

#wave {
  position: absolute;
  bottom: 0;
  width: 100%;
  height: 100px;
  z-index: 1;
}
</style>
