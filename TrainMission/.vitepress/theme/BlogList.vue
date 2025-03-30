<template>
  <div class="bloglist">
    <div class="section">
      <i class="fa-solid fa-book"></i> 运动记录列表
      <hr />
      <!-- 运动记录按钮 -->
      <button class="add-record-btn" @click="showModal = true">➕ 记录运动</button>
    </div>

    <div class="card" v-for="p in posts">
      <div class="image"></div>
      <div class="info">
        <div class="date">
          <i class="fa fa-clock"></i>
          发布于 {{ new Date(p.create).toLocaleDateString('sv-SE') }}
        </div>
        <a :href="base + p.href">
          <div class="title">{{ p.title }}</div>
        </a>
        <div class="content" v-html="p.excerpt"></div>
        <div class="tags">
          <a v-for="t in p.tags" :href="`${base}tags/?q=${t}`">
            <i class="fa fa-tag"></i>
            {{ t }}
          </a>
        </div>
      </div>
    </div>

    <!-- 弹出层：添加运动记录 -->
    <div v-if="showModal" class="modal-overlay">
      <div class="modal">
        <h2>📅 记录运动数据</h2>
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

        <button @click="saveWorkout">✅ 保存</button>
        <button @click="showModal = false">❌ 取消</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { type PostData } from '../posts.data'
import { useData } from 'vitepress'
import { ref } from 'vue'

const base = useData().site.value.base
const { posts } = defineProps<{ posts: PostData[] }>()

// 控制弹窗显示
const showModal = ref(false)
const startTime = ref('')
const endTime = ref('')
const exerciseType = ref('🏃‍♂️ 跑步')

// 生成 `.md` 记录
const saveWorkout = async () => {
  if (!startTime.value || !endTime.value || !exerciseType.value) {
    alert("请填写所有字段！");
    return;
  }

  // 生成 `.md` 内容
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

  // 生成唯一文件名（基于当前时间）
  const fileName = `${new Date().toISOString().replace(/[:.-]/g, "_")}.md`;

  try {
    const response = await fetch('http://127.0.0.1:8000/saveMission', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ fileName, content: mdContent })
    });

    const result = await response.json();

    if (response.ok) {
      alert("运动记录已成功保存！");
    } else {
      alert("保存失败: " + result.detail);
    }
  } catch (error) {
    alert("请求失败，请检查网络连接。");
  }

  showModal.value = false;
};

// 计算运动时长
const calculateDuration = () => {
  const start = new Date(startTime.value)
  const end = new Date(endTime.value)
  return Math.round((end.getTime() - start.getTime()) / (1000 * 60)) || 0
}
</script>

<style lang="scss">
.bloglist {
  max-width: 800px;
  margin: auto;

  .section {
    padding-top: 24px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .add-record-btn {
    background: #007bff;
    color: white;
    border: none;
    padding: 10px;
    border-radius: 5px;
    cursor: pointer;
    font-size: 14px;
  }

  .add-record-btn:hover {
    background: #0056b3;
  }

  .card {
    color: var(--color-gray);
    margin: 20px 0;
    padding: 24px;
    border-radius: 10px;
    box-shadow: 0 1px 20px -6px rgba(0, 0, 0, 0.5);
    transition: box-shadow 0.3s ease;

    &:hover {
      box-shadow: 0 5px 10px 5px rgb(0, 0, 0, 0.2);
    }
  }

  .title {
    color: #333;
    font-size: 24px;
    margin: 20px 0;
    transition: color 0.2s ease-out;

    &:hover {
      color: var(--color-accent);
    }
  }

  .tags a {
    margin-right: 8px;
    color: var(--color-gray);
    transition: color 0.2s ease-out;

    &:hover {
      color: var(--color-accent);
    }
  }
}

/* 弹出框样式 */
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
