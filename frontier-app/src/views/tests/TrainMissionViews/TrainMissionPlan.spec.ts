/// <reference types="vitest" />
import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import WeeklyPlanView from '../../TrainMissionViews/TrainMissionPlan.vue' // 修改为你的路径

describe('WeeklyPlanView.vue', () => {
  it('应成功渲染背景层和组件', () => {
    const wrapper = mount(WeeklyPlanView, {
      global: {
        stubs: {
          Header: {
            template: '<div class="mock-header">HeaderStub</div>'
          },
          Weekly_Plan: {
            template: '<div class="mock-weekly-plan">WeeklyPlanStub</div>'
          }
        }
      }
    })

    // 检查背景层元素是否存在
    expect(wrapper.find('.background-color-layer').exists()).toBe(true)
    expect(wrapper.find('.background-image-layer').exists()).toBe(true)

    // 检查 Header 和 Weekly_Plan 是否被 stub 渲染
    expect(wrapper.find('.mock-header').exists()).toBe(true)
    expect(wrapper.find('.mock-weekly-plan').exists()).toBe(true)
  })
})
