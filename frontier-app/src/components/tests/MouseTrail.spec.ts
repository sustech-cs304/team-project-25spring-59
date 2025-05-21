import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { render } from '@testing-library/vue'
import MouseTrail from '../MouseTrail.vue'

// let rafSpy: ReturnType<typeof vi.spyOn>
let rafSpy: any
let addEventSpy: ReturnType<typeof vi.spyOn>
import flushPromises from 'flush-promises'



beforeEach(() => {
  // 1. Mock canvas.getContext，防止 JSDOM 报错
  vi.spyOn(HTMLCanvasElement.prototype, 'getContext').mockImplementation(() => {
    return {
      clearRect: vi.fn(),
      beginPath: vi.fn(),
      moveTo: vi.fn(),
      lineTo: vi.fn(),
      stroke: vi.fn(),
      arc: vi.fn(),
      fill: vi.fn(),
      closePath: vi.fn(),
      createLinearGradient: () => ({ addColorStop: vi.fn() }),
      createRadialGradient: () => ({ addColorStop: vi.fn() }),
      fillStyle: '',
      strokeStyle: '',
      globalAlpha: 1,
      lineWidth: 1,
      save: vi.fn(),
      restore: vi.fn(),
      translate: vi.fn(),
      rotate: vi.fn()
    } as unknown as CanvasRenderingContext2D
  })

  // 2. 保存 requestAnimationFrame spy 引用（全局变量）
  rafSpy = vi.spyOn(window, 'requestAnimationFrame').mockImplementation((cb) => {
    return setTimeout(cb, 16) as unknown as number
  })

  // 3. 保存 addEventListener spy 引用（全局变量）
  addEventSpy = vi.spyOn(window, 'addEventListener')
})

afterEach(() => {
  vi.restoreAllMocks()
})

describe('MouseTrail.vue', () => {
  it('应成功渲染 canvas 元素', () => {
    render(MouseTrail)
    const canvas = document.querySelector('canvas')
    expect(canvas).not.toBeNull()
    expect(canvas?.id).toBe('mouse-trail')
  })

  it('应绑定 mousemove 和 mousedown 事件', async () => {
    render(MouseTrail)
    await flushPromises() // 等待 onMounted 中异步逻辑执行

  })

  it('应启动动画帧', () => {
    render(MouseTrail)
    expect(rafSpy).toHaveBeenCalled()
  })
})
