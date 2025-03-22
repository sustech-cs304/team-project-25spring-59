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
  width: 160px;
  height: 180px;
  overflow-y: auto;
  padding: 10px;
  border-radius: 10px;
  background: transparent;
  backdrop-filter: blur(6px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  font-size: 14px;
  color: #333;

}

.panel-title {
  font-weight: bold;
  margin-bottom: 6px;
  font-size: 16px;
}
</style>
