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
        <button @click="getAISuggestionFull">发送</button>
      </div>
    </div>
  </div>

</template>

<script setup lang="ts">
import { ref, nextTick, defineProps, defineEmits } from 'vue'
import {SILICON_API} from "../../configs/aiAdvisor_config.js"
import yaml from 'js-yaml'

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




//流式输出
const getAISuggestionFlow = async () => {
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



//-----------------------下面是针对ai建议pipeline的全流程方法--------------------------//
//定义template属性格式
export interface PromptTemplate {
  template_name: string
  description?: string
  inputs: string[]
  prompt: string
}


/**
 * 加载一个提示词 YAML 文件，并解析为结构化模板对象
 * @param fileName 文件名，如 'classify_input_type.yaml'
 */
const loadYamlPrompt = async (fileName: string): Promise<PromptTemplate> => {
  try {
    const response = await fetch(`/prompts/${fileName}`)
    if (!response.ok) throw new Error('提示词文件加载失败')

    const text = await response.text()
    const parsed = yaml.load(text)

    if (typeof parsed !== 'object' || parsed === null) {
      throw new Error('YAML 格式错误：不是对象')
    }

    const { template_name, prompt, inputs } = parsed as any
    if (!template_name || !prompt || !Array.isArray(inputs)) {
      throw new Error('YAML 缺少必要字段')
    }

    console.log('[loadYamlPrompt] 成功加载：', template_name)
    return parsed as PromptTemplate
  } catch (err) {
    console.error(`[loadYamlPrompt] 加载失败: ${fileName}`, err)
    throw err
  }
}


/**
 * 使用 PromptTemplate 对象生成最终提示词（并填充变量）
 * @param tpl PromptTemplate 对象（包含 template_name、prompt、inputs 等）
 * @param vars 变量对象，形如 { user_input: '你好' }
 * @returns 完整替换变量后的提示词字符串
 */
const buildPrompt = (tpl: PromptTemplate, vars: Record<string, string>): string => {
  const finalPrompt = tpl.prompt.replace(/{{\s*(\w+)\s*}}/g, (_, key: string) => {
    if (key in vars) {
      return vars[key]
    } else {
      console.warn(`[buildPrompt] 缺少变量: ${key}`)
      return ''
    }
  })

  console.log(`[buildPrompt] 生成的提示词内容:\n${finalPrompt}`)
  return finalPrompt
}


/**
 * 使用提示词 classify_input_type.yaml 判断输入类型
 * @param userInput 用户的自然语言输入
 * @returns 'task' | 'chat'
 */
const classifyUserInputType = async (userInput: string): Promise<'task' | 'chat'> => {
  try {
    const template = await loadYamlPrompt('classify_input_type.yaml')
    const prompt = buildPrompt(template, { user_input: userInput })
    console.log(`[buildPrompt] 生成的提示词内容:\n${prompt}`)


    const response = await fetch('https://api.siliconflow.cn/v1/chat/completions', {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${SILICON_API}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        model: 'Qwen/QwQ-32B',
        messages: [{ role: 'user', content: prompt }],
        stream: false,
        max_tokens: 50,
        temperature: 0,
        top_p: 0.7,
        n: 1,
        response_format: { type: 'text' }
      })
    })

    const result = await response.json()
    const reply = result.choices?.[0]?.message?.content?.trim().toLowerCase()

    if (reply === 'task' || reply === 'chat') {
      return reply
    }

    console.warn('[classifyUserInputType] 无效回复:', reply)
    return 'chat'
  } catch (err) {
    console.error('[classifyUserInputType] 处理失败:', err)
    return 'chat'
  }
}



const getAISuggestionFull = async () => {
  const content = userPrompt.value.trim()
  if (!content) return

  // 添加用户消息
  chatHistory.value.push({ role: 'user', content })
  userPrompt.value = ''

  try {
    // 1. 使用提示词模板 classify_input_type.yaml 判断类型
    const type = await classifyUserInputType(content)
    console.log('[分类结果] 输入类型为:', type)

    // 2. 将分类信息显示出来（可选）
    chatHistory.value.push({
      role: 'assistant',
      content: `输入被识别为「${type === 'task' ? '任务指令' : '闲聊对话'}」`
    })

    // 3. 根据分类执行不同的处理流程
    if (type === 'chat') {
      // 直接对闲聊内容进行回复
      const response = await fetch('https://api.siliconflow.cn/v1/chat/completions', {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${SILICON_API}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          model: 'Qwen/QwQ-32B',
          messages: [{ role: 'user', content }],
          stream: false,
          max_tokens: 512,
          temperature: 0.7,
          top_p: 0.8,
          response_format: { type: 'text' }
        })
      })

      const result = await response.json()
      const reply = result.choices?.[0]?.message?.content?.trim() || 'assistant 无响应'
      chatHistory.value.push({ role: 'assistant', content: reply })

    } else {
      // 若为任务，则加载特定的 task 提示词模板
      // const taskTpl = await loadYamlPrompt('generate_plan.yaml') // 假设你有这个模板
      // const filledPrompt = buildPrompt(taskTpl, { user_input: content })
      //
      // const taskRes = await fetch('https://api.siliconflow.cn/v1/chat/completions', {
      //   method: 'POST',
      //   headers: {
      //     Authorization: `Bearer ${SILICON_API}`,
      //     'Content-Type': 'application/json'
      //   },
      //   body: JSON.stringify({
      //     model: 'Qwen/QwQ-32B',
      //     messages: [{ role: 'user', content: filledPrompt }],
      //     stream: false,
      //     max_tokens: 1024,
      //     temperature: 0.7,
      //     top_p: 0.9,
      //     response_format: { type: 'text' }
      //   })
      // })
      //
      // const taskResult = await taskRes.json()
      // const reply = taskResult.choices?.[0]?.message?.content?.trim() || 'assistant 无响应'
      // chatHistory.value.push({ role: 'assistant', content: reply })
       chatHistory.value.push({
          role: 'assistant',
          content: `当前被识别为任务类型（task），但任务模板未定义，因此未执行具体操作。`
       })
    }

  } catch (err) {
    console.error('[getAISuggestionFull] 出错:', err)
    chatHistory.value.push({
      role: 'assistant',
      content: '❌ AI 生成建议失败，请稍后重试。'
    })
  }

  scrollToBottom()
}



// const getAISuggestionFull = async () => {
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
