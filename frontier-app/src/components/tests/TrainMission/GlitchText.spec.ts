import { render } from '@testing-library/vue'
import { describe, it, expect } from 'vitest'
import GlitchText from '../../TrainMission/GlitchText.vue'

describe('GlitchText.vue', () => {
  it('应该正确渲染文本和 data-text 属性', () => {
    const testText = '测试文本'
    const { getByText } = render(GlitchText, {
      props: {
        text: testText
      }
    })

    const el = getByText(testText)

    // 核心断言
    expect(el).toBeTruthy()
    expect(el.classList.contains('glitch')).toBe(true)
    expect(el.getAttribute('data-text')).toBe(testText)
  })
})
