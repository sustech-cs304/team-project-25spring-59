/// <reference types="vitest" />
vi.mock('echarts', () => {
  return {
    init: vi.fn(() => ({
      setOption: vi.fn(),
      resize: vi.fn()
    }))
  }
})

import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import DynamicBar from '../../TrainMission/Charts/TimeBar.vue'

describe('DynamicBar.vue', () => {
  it('应挂载并渲染 chart 容器', () => {
    const wrapper = mount(DynamicBar)

    const chartContainer = wrapper.find('#chart-dynamic-bar')
    expect(chartContainer.exists()).toBe(true)
  })
})
