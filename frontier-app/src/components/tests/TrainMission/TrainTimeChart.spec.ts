/// <reference types="vitest" />
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { flushPromises, mount } from '@vue/test-utils'
import RollArcLine from '../../TrainMission/Charts/TrainTimeChart.vue'


// ✅ mock echarts 防止真实渲染及 DOM 错误
vi.mock('echarts', () => {
  return {
    init: vi.fn(() => ({
      setOption: vi.fn(),
      resize: vi.fn(),
      dispatchAction: vi.fn(),
    })),
    graphic: {
      LinearGradient: vi.fn()
    }
  }
})

// ✅ mock fetch 请求
global.fetch = vi.fn(() =>
  Promise.resolve({
    json: () =>
      Promise.resolve({
        '2025-05-01': {
          duration_minutes: 30,
          calories: 300,
          avg_heart_rate: 100,
          max_heart_rate: 120,
        },
        '2025-05-02': {
          duration_minutes: 40,
          calories: 350,
          avg_heart_rate: 110,
          max_heart_rate: 130,
        },
      })
  })
) as unknown as typeof fetch

describe('RollArcLine.vue', () => {
  beforeEach(() => {
    localStorage.setItem('user_id', '123')
  })

  afterEach(() => {
    localStorage.clear()
    vi.restoreAllMocks()
  })

  it('应成功挂载并调用图表渲染', async () => {
    const wrapper = mount(RollArcLine)
    await flushPromises()

    const chartDom = wrapper.find('#chart-rollArc')
    expect(chartDom.exists()).toBe(true)
  })

  it('应响应月份选择并重新加载数据', async () => {
    const wrapper = mount(RollArcLine)
    await flushPromises()

    const vm = wrapper.vm as any
    const spy = vi.spyOn(vm, 'generateChartDataForMonth')

    await vm.handleMonthChange('2025-04')
    expect(spy).toHaveBeenCalledWith('2025-04')
  })

  it('应格式化 tooltip 内容', async () => {
    const wrapper = mount(RollArcLine)
    await flushPromises()

    const vm = wrapper.vm as any
    const tooltip = vm.option.tooltip.formatter([
      {
        name: '5月1日',
        marker: '*',
        seriesName: '运动时长（分钟）',
        value: 30,
        dataIndex: 0,
      },
    ])

    expect(tooltip).toContain('5月1日')
    expect(tooltip).toContain('运动时长')
    expect(tooltip).toContain('30')
  })
})
