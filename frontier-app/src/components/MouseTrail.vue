<template>
  <canvas id="mouse-trail"></canvas>
</template>

<script setup>
import { onMounted } from "vue";

onMounted(() => {
  const canvas = document.getElementById("mouse-trail");
  const ctx = canvas.getContext("2d");

  let width = (canvas.width = window.innerWidth);
  let height = (canvas.height = window.innerHeight);

  let trail = []; // 鼠标拖尾
  let particles = []; // 三角形粒子
  let rings = []; // 存储光环动画

  window.addEventListener("resize", () => {
    width = canvas.width = window.innerWidth;
    height = canvas.height = window.innerHeight;
  });

  // 🌟 监听鼠标移动，生成鼠标拖尾的三角形
  document.addEventListener("mousemove", (e) => {
    // 记录鼠标轨迹
    trail.push({ x: e.clientX, y: e.clientY, opacity: 1 });

    // 生成鼠标拖尾的三角形粒子
    particles.push({
      x: e.clientX,
      y: e.clientY,
      size: Math.random() * 3 + 2,
      opacity: 1,
      speedX: Math.random() * 1.5 - 0.75,
      speedY: Math.random() * 1.5 - 0.75,
      rotation: Math.random() * 360,
    });

    // 限制轨迹长度
    if (trail.length > 15) {
      trail.shift();
    }
  });

  // 🌟 监听鼠标按下，生成三角形粒子和光环动画
  document.addEventListener("mousedown", (e) => {
    // 生成多个三角形粒子
    for (let i = 0; i < 10; i++) {
      const angle = Math.random() * Math.PI * 2;
      const distance = Math.random() * 30 + 10; // 随机距离
      const x = e.clientX + Math.cos(angle) * distance;
      const y = e.clientY + Math.sin(angle) * distance;
      const size = Math.random() * 3 + 2;
      const speedX = Math.random() * 1.5 - 0.75;
      const speedY = Math.random() * 1.5 - 0.75;
      const rotation = Math.random() * 360;

      particles.push({
        x,
        y,
        size,
        opacity: 1,
        speedX,
        speedY,
        rotation,
      });
    }

    // 生成光环
    rings.push({
      x: e.clientX,
      y: e.clientY,
      radius1: 10, // 内圈半径
      radius2: 12, // 外圈半径（更接近）
      angle: 0, // 旋转角度
      opacity: 1, // 透明度
      lineWidth: 3, // 线宽
    });
  });

  function animate() {
    ctx.clearRect(0, 0, width, height); // 清空画布

    // 🔹 1. 绘制蓝色渐变线条（鼠标拖尾）
    if (trail.length > 1) {
      ctx.beginPath();
      ctx.moveTo(trail[0].x, trail[0].y);
      for (let i = 1; i < trail.length; i++) {
        ctx.lineTo(trail[i].x, trail[i].y);
      }
      const gradient = ctx.createLinearGradient(0, 0, width, height);
      gradient.addColorStop(0, "rgba(66, 165, 245, 1)");
      gradient.addColorStop(1, "rgba(66, 165, 245, 0)");
      ctx.strokeStyle = gradient;
      ctx.lineWidth = 2;
      ctx.globalAlpha = 0.7;
      ctx.stroke();
    }

    // 🔹 2. 绘制蓝色渐变三角形粒子（保留所有粒子）
    particles.forEach((p, i) => {
      ctx.save();
      ctx.translate(p.x, p.y);
      ctx.rotate((p.rotation * Math.PI) / 180);
      ctx.globalAlpha = p.opacity;

      const gradient = ctx.createLinearGradient(-p.size, -p.size, p.size, p.size);
      gradient.addColorStop(0, "rgba(66, 165, 245, 1)");
      gradient.addColorStop(1, "rgba(144, 202, 249, 0.8)");

      ctx.fillStyle = gradient;
      ctx.beginPath();
      ctx.moveTo(0, -p.size);
      ctx.lineTo(-p.size, p.size);
      ctx.lineTo(p.size, p.size);
      ctx.closePath();
      ctx.fill();
      ctx.restore();

      // 更新粒子位置和透明度
      p.x += p.speedX;
      p.y += p.speedY;
      p.opacity -= 0.03;

      // 删除透明度为0的粒子
      if (p.opacity <= 0) particles.splice(i, 1);
    });

    // 🌟 3. 绘制旋转光环
    rings.forEach((ring, i) => {
      ctx.globalAlpha = ring.opacity;

      // 计算旋转光点的位置
      let light1X = ring.x + Math.cos(ring.angle) * ring.radius1;
      let light1Y = ring.y + Math.sin(ring.angle) * ring.radius1;

      let light2X = ring.x + Math.cos(ring.angle + Math.PI) * ring.radius2;
      let light2Y = ring.y + Math.sin(ring.angle + Math.PI) * ring.radius2;

      // 绘制旋转光点
      ctx.beginPath();
      ctx.fillStyle = `rgba(255, 255, 255, ${ring.opacity})`;
      ctx.arc(light1X, light1Y, 3, 0, Math.PI * 2);
      ctx.fill();

      ctx.beginPath();
      ctx.fillStyle = `rgba(255, 255, 255, ${ring.opacity * 0.9})`;
      ctx.arc(light2X, light2Y, 3, 0, Math.PI * 2);
      ctx.fill();

      // 绘制光泽感的光环
      ctx.beginPath();
      let ringGradient = ctx.createRadialGradient(ring.x, ring.y, ring.radius1 - 2, ring.x, ring.y, ring.radius2 + 5);
      ringGradient.addColorStop(0, `rgba(255, 255, 255, ${ring.opacity * 0.5})`);
      ringGradient.addColorStop(1, `rgba(255, 255, 255, 0)`);
      ctx.strokeStyle = ringGradient;
      ctx.lineWidth = ring.lineWidth;
      ctx.arc(ring.x, ring.y, (ring.radius1 + ring.radius2) / 2, 0, Math.PI * 2);
      ctx.stroke();

      // 旋转 & 扩展
      ring.angle += 0.1; // 旋转速度
      ring.radius1 += 0.2;
      ring.radius2 += 0.3;
      ring.opacity -= 0.02;

      if (ring.opacity <= 0) rings.splice(i, 1);
    });

    requestAnimationFrame(animate); // 动画循环
  }

  animate(); // 启动动画
});
</script>

<style scoped>
#mouse-trail {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none; /* 确保画布不会干扰鼠标事件 */
  z-index: 1000; /* 使画布显示在页面的最上层 */
}
</style>
