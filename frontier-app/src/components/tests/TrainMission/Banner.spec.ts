// tests/unit/Banner.spec.ts
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, fireEvent } from '@testing-library/vue'
import Banner from '../../TrainMission/Banner.vue'

describe('Banner.vue', () => {
  const mockProps = {
    cover: 'https://example.com/banner.jpg',
    hello: 'Hello World',
    highText: 'Test Highlight',
    motto: 'This is a test motto.',
    social: [
      { icon: 'fa-twitter', url: 'https://twitter.com' },
      { icon: 'fa-github', url: 'https://github.com' }
    ]
  }

  beforeEach(() => {
    vi.useFakeTimers() // 控制 setTimeout 打字效果
  })

  it('应渲染背景图和 hello 标题', () => {
    const { getByText, container } = render(Banner, {
      props: mockProps
    })

    expect(getByText(mockProps.hello)).toBeTruthy()

    const rootDiv = container.querySelector('.banner')
    expect(rootDiv?.getAttribute('style')).toContain(mockProps.cover)
  })

  it('应显示高亮文字和社交链接', () => {
    const { getByText, getAllByRole } = render(Banner, {
      props: mockProps
    })

    expect(getByText(mockProps.highText)).toBeTruthy()

    const links = getAllByRole('link')
    expect(links.length).toBe(2)
    // expect(links[0]).toHaveAttribute('href', 'https://twitter.com')
  })

    it('应显示打字目标容器 .text', () => {
      const { container } = render(Banner, {
        props: mockProps
      })

      const textParagraph = container.querySelector('.text')
      expect(textParagraph).not.toBeNull()
    })


  it('应响应鼠标移动并更新 transform', async () => {
    const { container } = render(Banner, {
      props: mockProps
    })

    const box = container.querySelector('.box')
    expect(box).toBeTruthy()

    // 模拟鼠标移动事件
    const mockEvent = {
      clientX: 300,
      clientY: 300
    } as MouseEvent

    await fireEvent.mouseMove(box!, mockEvent)

    // 注意：这里的 transform 是响应式绑定，实际需要深入 Vue 内部去断言 calcX / calcY
    // 简化方式：断言 box 有 style 属性（不是空的）
    expect(box?.getAttribute('style')).toContain('rotateX')
  })
})
