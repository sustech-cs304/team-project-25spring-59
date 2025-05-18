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
import {SILICON_API} from "../../configs/aiAdvisor_config.js"

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

// const getAISuggestion = async () => {
//   const content = userPrompt.value.trim()
//   if (!content) return
//
//   // 显示用户输入
//   chatHistory.value.push({ role: 'user', content })
//   userPrompt.value = ''
//
//   try {
//     const response = await fetch('https://api.siliconflow.cn/v1/chat/completions', {
//       method: 'POST',
//       headers: {
//         Authorization: `Bearer ${SILICON_API}`,
//         'Content-Type': 'application/json'
//       },
//       body: JSON.stringify({
//         model: 'Qwen/QwQ-32B',
//         messages: [
//           { role: 'user', content }
//         ],
//         stream: false,
//         max_tokens: 512,
//         enable_thinking: false,
//         thinking_budget: 4096,
//         min_p: 0.05,
//         stop: null,
//         temperature: 0.7,
//         top_p: 0.7,
//         top_k: 50,
//         frequency_penalty: 0.5,
//         n: 1,
//         response_format: { type: 'text' },
//         tools: [
//           {
//             type: 'function',
//             function: {
//               description: '',
//               name: '',
//               parameters: {},
//               strict: false
//             }
//           }
//         ]
//       })
//     })
//
//     const result = await response.json()
//
//     // 获取 AI 回复内容（确保格式匹配）
//     const replyText = result.choices?.[0]?.message?.content || 'AI 无响应'
//
//     chatHistory.value.push({
//       role: 'assistant',
//       content: replyText
//     })
//   } catch (error) {
//     console.error('AI 接口调用失败:', error)
//     chatHistory.value.push({
//       role: 'assistant',
//       content: '获取建议失败，请稍后重试。'
//     })
//   }
//
//   scrollToBottom()
// }


//流式输出
const getAISuggestion = async () => {
  const content = userPrompt.value.trim()
  if (!content) return

  chatHistory.value.push({ role: 'user', content })
  userPrompt.value = ''

  // 插入 assistant 占位消息
  chatHistory.value.push({ role: 'assistant', content: '' })
  scrollToBottom()

  const assistantIndex = chatHistory.value.length - 1

  try {
    const response = await fetch('https://api.siliconflow.cn/v1/chat/completions', {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${SILICON_API}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        model: 'Qwen/QwQ-32B',
        messages: [{ role: 'user', content }],
        stream: true,
        max_tokens: 512,
        enable_thinking: false,
        thinking_budget: 4096,
        min_p: 0.05,
        stop: null,
        temperature: 0.7,
        top_p: 0.7,
        top_k: 50,
        frequency_penalty: 0.5,
        n: 1,
        response_format: { type: 'text' },
        tools: [{
          type: 'function',
          function: { description: '', name: '', parameters: {}, strict: false }
        }]
      })
    })

    if (!response.body) throw new Error('No response body')

    const reader = response.body.getReader()
    const decoder = new TextDecoder('utf-8')

    while (true) {
      const { done, value } = await reader.read()
      if (done) break
      const chunk = decoder.decode(value, { stream: true })

      for (const line of chunk.split('\n')) {
        const trimmed = line.trim()
        if (!trimmed || trimmed === 'data: [DONE]') continue

        let jsonLine = trimmed
        if (jsonLine.startsWith('data:')) jsonLine = jsonLine.slice(5).trim()

        try {
          const parsed = JSON.parse(jsonLine)
          const delta = parsed.choices?.[0]?.delta?.content
          if (delta) {
            chatHistory.value[assistantIndex].content += delta
            scrollToBottom()
          }
        } catch (e) {
          console.warn('JSON 解析失败:', jsonLine)
        }
      }
    }

  } catch (err) {
    console.error('流式请求失败:', err)
    chatHistory.value[assistantIndex].content += '\n[获取失败]'
  }

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
