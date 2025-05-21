import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import TaskPanel from '../../../TrainMission/Plans/TaskPanel.vue'

describe('TaskPanel.vue', () => {
  const mockProps = {
    title: '今日任务',
    tasks: ['跑步 3km', '俯卧撑 30 次', '阅读 20 分钟'],
    panelStyle: {
      top: '100px',
      left: '200px',
      backgroundColor: 'rgba(255, 255, 255, 0.8)'
    }
  }

  it('renders title correctly', () => {
    const wrapper = mount(TaskPanel, {
      props: mockProps
    })

    const titleEl = wrapper.find('.panel-title')
    expect(titleEl.exists()).toBe(true)
    expect(titleEl.text()).toBe('今日任务')
  })

  it('renders tasks list correctly', () => {
    const wrapper = mount(TaskPanel, {
      props: mockProps
    })

    const items = wrapper.findAll('ul > li')
    expect(items.length).toBe(mockProps.tasks.length)
    expect(items[0].text()).toBe('跑步 3km')
    expect(items[1].text()).toBe('俯卧撑 30 次')
    expect(items[2].text()).toBe('阅读 20 分钟')
  })

  it('applies panelStyle correctly', () => {
    const wrapper = mount(TaskPanel, {
      props: mockProps
    })

    const panel = wrapper.find('.task-panel')
    const style = panel.attributes('style')

    expect(style).toContain('top: 100px')
    expect(style).toContain('left: 200px')
    expect(style).toContain('background-color: rgba(255, 255, 255, 0.8)')
  })
})
