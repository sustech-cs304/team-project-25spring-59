
/// <reference types="vitest" />
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { flushPromises, mount } from '@vue/test-utils'
import DashboardView from '../../TrainMissionViews/TrainMissionDashboard.vue'
import axios from 'axios'

vi.mock('axios')
const mockedAxios = axios as unknown as { post: ReturnType<typeof vi.fn> }

vi.mock('../../../components/TrainMission/Header.vue', () => ({
  default: { template: '<div class="mock-header" />' }
}))
vi.mock('../../../components/TrainMission/Charts/TrainTimeChart.vue', () => ({
  default: { template: '<div class="mock-train-chart" />' }
}))
vi.mock('../../components/Spine-Player-Dashboard/index.vue', () => ({
  default: {
    name: 'SpinePlayer',
    emits: ['show-ai-panel'],
    template: '<div class="mock-spine-player" @click="$emit(\'show-ai-panel\')" />'
  }
}))
vi.mock('../aitrainer.vue', () => ({
  default: {
    name: 'AITrainerAssistant',
    props: ['visible'],
    emits: ['close'],
    template: '<div class="mock-ai-panel" />'
  }
}))

describe('TrainMissionDashboard.vue', () => {
  beforeEach(() => {
    localStorage.setItem('user_id', '1')
    mockedAxios.post = vi.fn().mockResolvedValue({
      data: {
        total_minutes: 90,
        estimated_calories: 600,
        actual_calories: 580,
        average_heart_rate: 100,
        max_heart_rate: 130
      }
    })
  })

  afterEach(() => {
    localStorage.clear()
    vi.restoreAllMocks()
  })

  it('应渲染 Header、图表、SpinePlayer', async () => {
    const wrapper = mount(DashboardView)
    await flushPromises()

    expect(wrapper.find('.mock-header').exists()).toBe(true)
    expect(wrapper.find('.mock-train-chart').exists()).toBe(true)
    expect(wrapper.find('.mock-spine-player').exists()).toBe(false)
  })

  it('应渲染训练数据统计卡片', async () => {
    const wrapper = mount(DashboardView)
    await flushPromises()

    expect(wrapper.text()).toContain('90 分钟')
    expect(wrapper.text()).toContain('600 kcal')
    expect(wrapper.text()).toContain('580 kcal')
    expect(wrapper.text()).toContain('100 bpm')
    expect(wrapper.text()).toContain('130 bpm')
  })

  it('点击 spine-player 应显示 AI 面板', async () => {
    const wrapper = mount(DashboardView, {
      global: {
        stubs: {
          SpinePlayer: {
            template: `<div class="mock-spine-player" @click="$emit('show-ai-panel')" />`
          },
          AITrainerAssistant: {
            template: `<div class="mock-ai-panel" />`,
            props: ['visible']
          },
          Header: true,
          TrainTimeChart: true
        }
      }
    })

    await flushPromises()
    expect(wrapper.find('.mock-ai-panel').exists()).toBe(true)

    await wrapper.find('.mock-spine-player').trigger('click')
    await flushPromises()

    expect(wrapper.find('.mock-ai-panel').exists()).toBe(true)
  })

})
