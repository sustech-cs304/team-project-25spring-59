<template>
  <div class="ai-float-sidebar animate__animated animate__fadeInRight" v-if="visible">
    <div class="ai-panel">
      <div class="ai-header">
        <h3>AI 建议</h3>
        <button @click="$emit('close')">关闭</button>
      </div>
      <div class="ai-content" ref="chatContainer">
        <div
          v-for="(msg, index) in chatHistory"
          :key="index"
          class="chat-message"
          :class="msg.role"
        >
          <img
            class="avatar"
            :src="msg.role === 'user' ? userAvatar : aiAvatar"
            alt="avatar"
          />
          <div class="bubble">{{ msg.content }}</div>
        </div>
      </div>
      <div class="ai-input">
        <input
          type="text"
          v-model="userPrompt"
          placeholder="请输入问题或请求"
          @keyup.enter="getAISuggestion"
        />
        <button @click="getAISuggestion">发送</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, nextTick, defineProps, defineEmits } from 'vue'

interface Message {
  role: 'user' | 'assistant'
  content: string
}

const props = defineProps({
  visible: Boolean,
})
const emit = defineEmits(['close'])

const userAvatar = '/avatar-user.jpg'
const aiAvatar = '/avatar-ai.jpg'

const userPrompt = ref('')
const chatHistory = ref<Message[]>([])
const chatContainer = ref<HTMLElement | null>(null)

const scrollToBottom = () => {
  nextTick(() => {
    if (chatContainer.value) {
      chatContainer.value.scrollTop = chatContainer.value.scrollHeight
    }
  })
}

const getAISuggestion = async () => {
  const content = userPrompt.value.trim()
  if (!content) return

  chatHistory.value.push({ role: 'user', content })
  userPrompt.value = ''

  await new Promise(resolve => setTimeout(resolve, 500))

  chatHistory.value.push({
    role: 'assistant',
    content: `收到：${content}`
  })

  scrollToBottom()
}
</script>

<style scoped lang="scss">
@import "animate.css";

.ai-float-sidebar {
  position: fixed;
  top: 80px;
  right: 0;
  width: 600px;
  height: calc(100vh - 80px);
  background: white;
  box-shadow: -4px 0 12px rgba(0, 0, 0, 0.1);
  z-index: 2000;
  display: flex;
  flex-direction: column;
}

.ai-panel {
  display: flex;
  flex-direction: column;
  height: 100%;
  padding: 1rem;
}

.ai-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #ddd;
  padding-bottom: 0.5rem;

  h3 {
    margin: 0;
    font-size: 1.2rem;
  }

  button {
    background: none;
    border: none;
    color: #888;
    cursor: pointer;
    font-size: 0.9rem;
  }
}

.ai-content {
  flex: 1;
  overflow-y: auto;
  margin: 1rem 0;
  .placeholder {
    color: #999;
    font-style: italic;
  }
}

.ai-input {
  display: flex;
  gap: 0.5rem;
  input {
    flex: 1;
    padding: 0.5rem;
    border: 1px solid #ddd;
    border-radius: 6px;
  }
  button {
    padding: 0.5rem 1rem;
    background-color: #1976d2;
    color: #fff;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    &:hover {
      background-color: #125ca1;
    }
  }
}

.chat-message {
  display: flex;
  align-items: flex-start;
  margin-bottom: 1rem;

  &.user {
    flex-direction: row-reverse;
    .bubble {
      background-color: #1976d2;
      color: white;
      border-top-right-radius: 0;
    }
  }
  &.assistant {
    .bubble {
      background-color: #f0f0f0;
      border-top-left-radius: 0;
    }
  }
  .avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    object-fit: cover;
    margin: 0 0.75rem;
  }
  .bubble {
    max-width: 75%;
    padding: 0.75rem 1rem;
    border-radius: 1rem;
    font-size: 0.95rem;
    line-height: 1.4;
    word-break: break-word;
    background-color: #eee;
  }
}
</style>
