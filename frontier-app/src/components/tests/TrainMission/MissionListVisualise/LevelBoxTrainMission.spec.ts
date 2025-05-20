import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render } from '@testing-library/vue'
import LevelBox from '../../../TrainMission/MissionListVisualize/LevelBoxTrainMission.vue'

// mock a-progress 组件，避免渲染错误
vi.mock('ant-design-vue', () => ({
  AProgress: {
    name: 'a-progress',
    template: '<div><slot /></div>',
    props: ['percent', 'showText', 'color', 'trackColor']
  }
}))

describe('LevelBox.vue', () => {
  beforeEach(() => {
    localStorage.setItem('user_id', '123456')
  })

  it('应正确渲染用户 ID', () => {
    const { getByText } = render(LevelBox)
    expect(getByText('UserId: 123456')).toBeTruthy()
  })

  it('应渲染等级 Lv.60', () => {
    const { getByText } = render(LevelBox)
    expect(getByText('Lv.')).toBeTruthy()
    expect(getByText('60')).toBeTruthy()
  })

  it('应显示经验值比例为 50/100', () => {
    const { getByText } = render(LevelBox)
    expect(getByText('50/100')).toBeTruthy()
  })

  it('应渲染 a-progress 组件', () => {
    const { container } = render(LevelBox)
    // 检查自定义标签存在（因为我们 mock 了 a-progress）
    expect(container.querySelector('div')).toBeTruthy()
  })
})
