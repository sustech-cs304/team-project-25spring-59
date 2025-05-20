/// <reference types="vitest" />
import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import TrainMissionLevel from '../../TrainMissionViews/TrainMissionSpecification.vue' // 替换为你的真实路径

describe('TrainMissionLevel.vue', () => {
  it('应正确渲染背景层和组件结构', () => {
    const wrapper = mount(TrainMissionLevel, {
      global: {
        stubs: {
          Header: { template: '<div class="stub-header" />' },
          LevelBox: { template: '<div class="stub-levelbox" />' },
          Specification: { template: '<div class="stub-specification" />' }
        }
      }
    })

    // 检查背景图层是否存在
    expect(wrapper.find('.background-color-layer').exists()).toBe(true)
    expect(wrapper.find('.background-image-layer').exists()).toBe(true)

    // 检查 Header、LevelBox、Specification 组件是否渲染
    expect(wrapper.find('.stub-header').exists()).toBe(true)
    expect(wrapper.find('.stub-levelbox').exists()).toBe(true)
    expect(wrapper.find('.stub-specification').exists()).toBe(true)

    // 检查主体容器存在
    expect(wrapper.find('.train-mission-main').exists()).toBe(true)
  })
})
