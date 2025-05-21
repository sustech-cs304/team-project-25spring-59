/// <reference types="vitest" />
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount, flushPromises } from '@vue/test-utils'
import AITrainerAssistant from '../../TrainMissionViews/aitrainer.vue'

describe('AITrainerAssistant.vue', () => {
  beforeEach(() => {
    localStorage.setItem('user_id', '123') // mock user_id
  })

  it('应渲染组件并展示输入框', () => {
    const wrapper = mount(AITrainerAssistant, {
      props: {
        visible: true
      }
    })

    expect(wrapper.find('.ai-float-sidebar').exists()).toBe(true)
    expect(wrapper.find('input[type="text"]').exists()).toBe(true)
    expect(wrapper.find('button').text()).toContain('关闭')
  })
    
  it('点击关闭按钮应触发 close 事件', async () => {
    const wrapper = mount(AITrainerAssistant, {
      props: {
        visible: true
      }
    })

    await wrapper.find('.ai-header button').trigger('click')

    expect(wrapper.emitted('close')).toBeTruthy()
  })

  it('加载中状态时应显示动画气泡', async () => {
    const wrapper = mount(AITrainerAssistant, {
      props: {
        visible: true
      }
    })

    // 设置加载状态
    wrapper.vm.isLoading = true
    await flushPromises()

    expect(wrapper.find('.loading-placeholder').exists()).toBe(true)
    expect(wrapper.find('.loading-dot').text()).toContain('阿罗娜正在思考中')
  })
})
