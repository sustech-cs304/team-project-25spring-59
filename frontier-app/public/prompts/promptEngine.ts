import yaml from 'js-yaml'
import {SILICON_API} from "../../src/configs/aiAdvisor_config.js"
import {ref} from "vue";

//-----------------------下面是针对ai建议pipeline的全流程方法--------------------------//
interface Message {
  role: 'user' | 'assistant'
  content: string
}

const userPrompt = ref('')
const chatHistory = ref<Message[]>([])

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
export async function loadYamlPrompt(fileName: string): Promise<PromptTemplate> {
  try {
    const file = await import(`../prompts/${fileName}?raw`)
    const parsed = yaml.load(file.default)

    if (typeof parsed !== 'object' || parsed === null) {
      throw new Error('YAML 格式错误：不是对象')
    }

    const { template_name, prompt, inputs } = parsed as any
    if (!template_name || !prompt || !Array.isArray(inputs)) {
      throw new Error('YAML 中缺少 template_name、prompt 或 inputs 字段')
    }

    return parsed as PromptTemplate
  } catch (err) {
    console.error(`[loadYamlPrompt] 加载提示词失败: ${fileName}`, err)
    throw err
  }
}

/**
 * 使用 PromptTemplate 对象生成最终提示词（并填充变量）
 * @param tpl PromptTemplate 对象（包含 template_name、prompt、inputs 等）
 * @param vars 变量对象，形如 { user_input: '你好' }
 * @returns 完整替换变量后的提示词字符串
 */
export function buildPrompt(tpl: PromptTemplate, vars: Record<string, string>): string {
  const finalPrompt = tpl.prompt.replace(/{{\s*(\w+)\s*}}/g, (_, key: string) => {
    if (key in vars) {
      return vars[key]
    } else {
      console.warn(`[buildPrompt] 缺少变量: ${key}`)
      return ''
    }
  })
  //打印最终生成的提示词内容
  console.log(`[buildPrompt] 生成的提示词内容:\n${finalPrompt}`)
  return finalPrompt
}



/**
 * 使用提示词 classify_input_type.yaml 判断输入类型
 * @param userInput 用户的自然语言输入
 * @returns 'task' | 'chat'
 */
export async function classifyUserInputType(userInput: string): Promise<'task' | 'chat'> {
  try {
    // 1. 加载 YAML 模板
    const template: PromptTemplate = await loadYamlPrompt('classify_input_type.yaml')

    // 2. 填充模板变量
    const prompt = buildPrompt(template, { user_input: userInput })

    // 3. 调用 AI API（非流式）
    const response = await fetch('https://api.siliconflow.cn/v1/chat/completions', {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${SILICON_API}`,
        'Content-Type': 'application/json',
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
      }),
    })

    const result = await response.json()
    const reply = result.choices?.[0]?.message?.content?.trim().toLowerCase()

    if (reply === 'task' || reply === 'chat') {
      return reply
    }

    console.warn('[classifyUserInputType] 无效回复:', reply)
    return 'chat' // 默认降级为 chat

  } catch (err) {
    console.error('[classifyUserInputType] 处理失败:', err)
    return 'chat' // 错误时默认返回
  }
}
