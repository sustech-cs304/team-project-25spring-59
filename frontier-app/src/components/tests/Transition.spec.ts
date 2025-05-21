// tests/unit/views/Transition.spec.ts
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render } from '@testing-library/vue'
import Transition from '../Transition.vue'
import { createRouter, createWebHistory } from 'vue-router'
import { nextTick } from 'vue'

// 创建一个 mock 路由器
const router = createRouter({
  history: createWebHistory(),
  routes: [{ path: '/', component: { template: '<div>首页</div>' } }]
})

describe('Transition.vue', () => {
  beforeEach(() => {
    vi.useFakeTimers() // 模拟定时器
  })

  it('初始渲染成功，包含进度条与图片', () => {
    const { getByAltText, getByText } = render(Transition, {
      global: { plugins: [router] }
    })

    expect(getByAltText('Loading...')).toBeTruthy()
    expect(getByText('0%')).toBeTruthy()
  })

  it('模拟进度条变化和图片轮播', async () => {
    const { getByText, getByAltText } = render(Transition, {
      global: { plugins: [router] }
    })

    vi.advanceTimersByTime(750) // 模拟 750ms -> progress 应该为 30%
    await nextTick()

    expect(getByText('10%')).toBeTruthy()
    expect(getByAltText('Loading...')).toBeTruthy()
  })

  it('2.5 秒后自动跳转', async () => {
    const pushSpy = vi.spyOn(router, 'push')
    render(Transition, { global: { plugins: [router] } })

    vi.advanceTimersByTime(2500)
    await nextTick()

    expect(pushSpy).toHaveBeenCalledWith('/')
  })
})
