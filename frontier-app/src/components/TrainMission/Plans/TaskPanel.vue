<template>
  <div class="task-panel" :style="panelStyle">
    <h3 class="panel-title">{{ title }}</h3>
    <ul>
      <li v-for="(task, i) in tasks" :key="i">{{ task }}</li>
    </ul>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  title: string
  tasks: string[]
  panelStyle?: Record<string, string>
}>()
</script>

<style scoped lang="scss">
.task-panel {
  position: absolute;
  width: 540px;
  height: 450px;
  overflow-y: auto;
  padding: 10px;
  border-radius: 10px;
  background: transparent;
  //backdrop-filter: blur(6px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  font-size: 20px;
  color: #333;
  //background-color: #df1c1c;

  clip-path: polygon(
    0 0,                    /* top-left */
    calc(100% - 60px) 0,    /* move inward before top-right */
    100% 60px,              /* cut down for right-top corner */
    100% 100%,              /* bottom-right (keep sharp) */
    60px 100%,              /* move inward before bottom-left */
    0 calc(100% - 60px)     /* cut upward for left-bottom corner */
  );

}

.panel-title {
  font-weight: bold;
  margin-bottom: 6px;
  font-size: 30px;
}
</style>
