<script setup>
import { onMounted, ref } from 'vue'
import { Spine } from 'pixi-spine'
import * as PIXI from 'pixi.js'
import { sound } from '@pixi/sound'

// 定义 L2D 资源路径
const spinePath = '/l2d/hina_swimsuit/CH0063_home.skel';
const atlasPath = '/l2d/hina_swimsuit/CH0063_home.atlas';
const bgmPath = '/l2d/hina_swimsuit/Theme_21.mp3';

// 存储解析后的 Spine 数据
const studentL2D = ref(null);

onMounted(async () => {
  try {
    // 创建 PixiJS 应用
    const app = new PIXI.Application({
      width: 2560,
      height: 1440,
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
</script>

<template>
  <div id="background"></div>
</template>

<style scoped>
#background {
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  z-index: -1;
}
</style>
