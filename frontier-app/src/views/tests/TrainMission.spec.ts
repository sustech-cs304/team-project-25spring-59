/// <reference types="vitest" />
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { flushPromises, mount } from '@vue/test-utils'
import MainPage from '../TrainMission.vue'

// ✅ Mock 子组件
vi.mock('../../components/TrainMission/Banner.vue', () => ({
  default: {
    name: 'Banner',
    template: '<div class="mock-banner" />',
    props: ['cover', 'hello', 'highText', 'motto', 'social']
  }
}))

vi.mock('../../components/TrainMission/Header.vue', () => ({
  default: {
    name: 'Header',
    template: '<div class="mock-header" />',
    props: ['base']
  }
}))

vi.mock('../../components/TrainMission/MissionListVisualize/Planlist.vue', () => ({
  default: {
    name: 'PlanList',
    template: '<div class="mock-planlist" />'
  }
}))

vi.mock('../../components/Spine-Player-MainMenu/index.vue', () => ({
  default: {
    name: 'SpinePlayer',
    template: '<div class="mock-spine-player" />'
  }
}))

describe('MainTrainMissionPage.vue', () => {
  beforeEach(() => {
    vi.restoreAllMocks()
  })

  it('应挂载并包含背景图层', () => {
    const wrapper = mount(MainPage)
    expect(wrapper.find('.background-color-layer').exists()).toBe(true)
    expect(wrapper.find('.background-image-layer').exists()).toBe(true)
  })

  it('应渲染 Header、Banner、PlanList 和 SpinePlayer 组件', async () => {
    const wrapper = mount(MainPage)
    await flushPromises()

    expect(wrapper.find('.mock-header').exists()).toBe(true)
    expect(wrapper.find('.mock-banner').exists()).toBe(true)
    expect(wrapper.find('.mock-planlist').exists()).toBe(true)
    expect(wrapper.find('.mock-spine-player').exists()).toBe(true)
  })

  it('应在挂载时设置 routeBase', async () => {
    const wrapper = mount(MainPage)
    await flushPromises()

    const vm = wrapper.vm as any
    expect(vm.routeBase).toBe(window.location.origin + '/')
  })
})
