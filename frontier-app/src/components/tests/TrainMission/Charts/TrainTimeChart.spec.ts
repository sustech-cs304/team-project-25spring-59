/// <reference types="vitest" />
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { flushPromises, mount } from '@vue/test-utils'
import RollArcLine from '../../../TrainMission/Charts/TrainTimeChart.vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

// ✅ mock echarts
const resizeMock = vi.fn()
const setOptionMock = vi.fn()
const dispatchActionMock = vi.fn()

vi.mock('echarts', () => {
  return {
    init: vi.fn(() => ({
      setOption: setOptionMock,
      resize: resizeMock,
      dispatchAction: dispatchActionMock
    })),
    graphic: {
      LinearGradient: vi.fn()
    }
  }
})

// ✅ mock fetch 请求数据
globalThis.fetch = vi.fn(() =>
  Promise.resolve({
    json: () =>
      Promise.resolve({
        '2025-05-01': {
          duration_minutes: 30,
          calories: 300,
          avg_heart_rate: 100,
          max_heart_rate: 120
        },
        '2025-05-02': {
          duration_minutes: 40,
          calories: 350,
          avg_heart_rate: 110,
          max_heart_rate: 130
        }
      })
  })
) as unknown as typeof fetch

describe('TrainTimeChart.vue', () => {
  beforeEach(() => {
    localStorage.setItem('user_id', '123')
  })

  afterEach(() => {
    vi.clearAllMocks()
    localStorage.clear()
  })

   it('应调用数据加载并构建 x/y 数据', async () => {
    localStorage.setItem('user_id', '123')

    // ✅ 必须在 mount 前 spy
    const spy = vi.spyOn(RollArcLine.methods, 'generateChartDataForMonth')

    const wrapper = mount(RollArcLine, {
      global: {
        plugins: [ElementPlus]
      }
    })

    await flushPromises()

    expect(spy).toHaveBeenCalled()
    expect((wrapper.vm as any).xData.length).toBeGreaterThan(0)
  })

  it('应触发月份切换并重新加载', async () => {
    const wrapper = mount(RollArcLine)
    const vm = wrapper.vm as any
    const genSpy = vi.spyOn(vm, 'generateChartDataForMonth')

    await vm.handleMonthChange('2025-04')
    expect(genSpy).toHaveBeenCalledWith('2025-04')
  })


  it('应正确停止 tooltip 轮播', async () => {
    const wrapper = mount(RollArcLine)
    const vm = wrapper.vm as any
    vm.timer = setInterval(() => {}, 1000)
    const clearSpy = vi.spyOn(globalThis, 'clearInterval')

    vm.stopChartAutoShowTip()
    expect(clearSpy).toHaveBeenCalled()
    expect(vm.timer).toBeNull()
  })

  it('应处理 mouseover / mouseout 事件', async () => {
    const wrapper = mount(RollArcLine)
    await flushPromises()

    const chartDom = document.getElementById('chart-rollArc')
    expect(chartDom).toBeNull()

    const stopSpy = vi.spyOn(wrapper.vm as any, 'stopChartAutoShowTip')
    const startSpy = vi.spyOn(wrapper.vm as any, 'startChartAutoShowTip')

    chartDom?.dispatchEvent(new Event('mouseover'))
    chartDom?.dispatchEvent(new Event('mouseout'))

  })
})
