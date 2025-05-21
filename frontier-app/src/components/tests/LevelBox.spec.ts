import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render } from '@testing-library/vue'
import LevelBox from '../LevelBox.vue'

// 👇 mock ant-design-vue 的 <a-progress>
vi.mock('ant-design-vue', () => {
  return {
    AProgress: {
      name: 'AProgress',
      props: ['percent', 'showText', 'color', 'trackColor'],
      template: '<div data-testid="progress">{{ percent }}</div>'
    }
  }
})

describe('LevelBox.vue', () => {
  beforeEach(() => {
    // 模拟 localStorage.user_id
    localStorage.setItem('user_id', 'test_user_123')
  })

  it('应渲染用户 ID 和等级', () => {
    const { getByText } = render(LevelBox)

    expect(getByText('Lv.')).toBeTruthy()
    expect(getByText('60')).toBeTruthy()
    expect(getByText('UserId: test_user_123')).toBeTruthy()
  })

  it('应显示当前经验值文本', () => {
    const { getByText } = render(LevelBox)

    expect(getByText('50/100')).toBeTruthy()
  })

  it('应在经验值满时显示 MAX 并改变颜色', async () => {
    // mock 经验值逻辑，模拟 MAX 状态
    vi.mocked(Object, true) // 避免 globalRef 报错

    const { getByText } = render(LevelBox, {
      global: {
        mocks: {
          exp: 100,
          nextExp: 100
        }
      }
    })

    expect(getByText('MAX')).toBeTruthy()
  })
})
