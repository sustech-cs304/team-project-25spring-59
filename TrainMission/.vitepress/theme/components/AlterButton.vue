<template>
  <button @click="showEditModal" class="alter-button">修改记录</button>

  <!-- 编辑弹窗 -->
  <div v-if="showModal" class="modal-overlay">
    <div class="modal">
      <h2>📅 修改运动数据</h2>
      <label>开始时间：</label>
      <input type="datetime-local" v-model="startTime" />

      <label>结束时间：</label>
      <input type="datetime-local" v-model="endTime" />

      <label>运动类型：</label>
      <select v-model="exerciseType">
        <option>跑步</option>
        <option>骑行</option>
        <option>健身</option>
        <option>游泳</option>
      </select>

      <button @click="saveAlteredWorkout">✅ 保存修改</button>
      <button @click="showModal = false">❌ 取消</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRoute } from 'vitepress'

const route = useRoute()

// 控制弹窗显示
const showModal = ref(false)
const startTime = ref('')
const endTime = ref('')
const exerciseType = ref('🏃‍♂️ 跑步')

// 触发编辑弹窗
const showEditModal = () => {
  showModal.value = true
}

// 获取当前路径并生成文件名
const getFileName = () => {
  const path = route.path // 获取当前路径
  const filename = path.substring(path.lastIndexOf("/") + 1, path.lastIndexOf(".html")) + ".md"
  return filename
}

// 获取user_id
const getUserId = () => {
  const userId = localStorage.getItem('user_id')
  return userId ? parseInt(userId) : null
}

// 保存修改的运动记录
const saveAlteredWorkout = async () => {
  if (!startTime.value || !endTime.value || !exerciseType.value) {
    alert("请填写所有字段！");
    return;
  }

  // 构建新的.md内容
  const mdContent = `---
title: "${exerciseType.value} 运动记录"
date: "${new Date().toISOString()}"
tags: [${exerciseType.value.replace(/\s/g, '')}]
cover: ""
---
## 运动详情
- **开始时间**: ${startTime.value}
- **结束时间**: ${endTime.value}
- **运动类型**: ${exerciseType.value}
- **时长**: ${calculateDuration()} 分钟
`;

  const filename = getFileName() // 获取文件名
  const userId = getUserId() // 获取用户ID

  try {
    const response = await fetch('http://127.0.0.1:8000/edit-record', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        filename, // 传递文件名
        content: mdContent, // 传递修改后的内容
        user_id: userId // 传递用户ID
      })
    })

    const result = await response.json()

    if (response.ok) {
      alert('运动记录修改成功！')
    } else {
      alert('修改失败: ' + result.detail)
    }
  } catch (error) {
    alert('请求失败，请检查网络连接。')
  }

  showModal.value = false
}

// 计算时长
const calculateDuration = () => {
  const start = new Date(startTime.value)
  const end = new Date(endTime.value)
  return Math.round((end.getTime() - start.getTime()) / (1000 * 60)) || 0
}
</script>

<style scoped>
.alter-button {
  background-color: #28a745;
  color: white;
  border: none;
  padding: 10px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 14px;
}

.alter-button:hover {
  background: #218838;
}

/* 弹窗样式 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal {
  background: white;
  padding: 20px;
  border-radius: 10px;
  width: 300px;
  text-align: center;
}

.modal h2 {
  margin-bottom: 10px;
}

.modal input,
.modal select {
  width: 100%;
  margin: 10px 0;
  padding: 5px;
}

.modal button {
  margin: 5px;
  padding: 8px;
  border: none;
  cursor: pointer;
  border-radius: 5px;
}

.modal button:first-child {
  background: #28a745;
  color: white;
}

.modal button:last-child {
  background: #dc3545;
  color: white;
}
</style>
