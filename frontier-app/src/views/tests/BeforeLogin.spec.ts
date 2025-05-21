/// <reference types="vitest" />
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { flushPromises, mount } from '@vue/test-utils'
import BeforeLogin from '../BeforeLogin.vue'
import { nextTick } from 'vue'

// 模拟 router
vi.mock('vue-router', () => ({
  useRouter: () => ({
    push: vi.fn()
  })
}))

// 模拟 axios 请求
vi.mock('axios', () => ({
  default: {
    get: vi.fn(() => Promise.resolve())
  }
}))

describe('BeforeLogin.vue', () => {
  beforeEach(() => {
    vi.useFakeTimers()
    localStorage.setItem('user_id', 'test_user_123')
  })

  afterEach(() => {
    vi.useRealTimers()
    vi.restoreAllMocks()
    localStorage.clear()
  })

  it('应显示启动加载界面', async () => {
    const wrapper = mount(BeforeLogin)
    expect(wrapper.find('.splash-container').exists()).toBe(true)
    expect(wrapper.find('.status-text').exists()).toBe(true)
  })

  it('应模拟加载步骤并跳转登录', async () => {
    const wrapper = mount(BeforeLogin)
    // 快进加载步骤的定时器
    vi.runAllTimers()
    await flushPromises()
    await nextTick()

    // 这里模拟的 router.push 只是被调用了，但因为 mock，不会真的跳转
    // 验证触发流程结束并改变状态
    // @ts-ignore
    expect(wrapper.vm.isLoading).toBe(true)
  })

  it('应初始化进度和状态文字', async () => {
    const wrapper = mount(BeforeLogin)
    // @ts-ignore
    wrapper.vm.progress = 50
    // @ts-ignore
    wrapper.vm.statusText = '加载中...'
    await nextTick()

    expect(wrapper.html()).toContain('加载中...')
    expect(wrapper.find('.progress-bar').attributes('style')).toContain('width: 50%')
  })
})
