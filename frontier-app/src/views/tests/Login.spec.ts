/// <reference types="vitest" />
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount, flushPromises } from '@vue/test-utils'
import Login from '../Login.vue'
import axios from 'axios'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

// ✅ mock router
vi.mock('vue-router', () => ({
  useRouter: () => ({
    push: vi.fn()
  })
}))

// ✅ mock axios
vi.mock('axios')
const mockedAxios = axios as unknown as {
  post: ReturnType<typeof vi.fn>
}

// ✅ mock Element Plus Message
vi.mock('element-plus', async (importOriginal) => {
  const original = await importOriginal()
  return {
    // @ts-ignore
    ...original,
    ElMessage: {
      success: vi.fn(),
      error: vi.fn()
    }
  }
})

describe('Login.vue', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    localStorage.clear()
  })

  it('初始时应显示点击提示', () => {
    const wrapper = mount(Login, {
      global: {
        stubs: { MouseTrail: true },
        plugins: [ElementPlus]
      }
    })
    expect(wrapper.find('.login-button-text').exists()).toBe(true)
    expect(wrapper.find('.login-card').exists()).toBe(false)
  })

  it('点击后应显示登录表单', async () => {
    const wrapper = mount(Login, {
      global: {
        stubs: { MouseTrail: true },
        plugins: [ElementPlus]
      }
    })
    await wrapper.trigger('click')
    expect(wrapper.find('.login-card').exists()).toBe(true)
  })


})
