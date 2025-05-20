// ❗ 必须放在顶部才能生效
vi.mock('chart.js/auto', () => {
  const ChartMock = vi.fn()
  return { default: ChartMock }
})

import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render } from '@testing-library/vue'
import PieChart from '../PieChart.vue'
import Chart from 'chart.js/auto'

// 转换类型，才能访问 mock.calls
const ChartMock = Chart as unknown as ReturnType<typeof vi.fn>

describe('PieChart.vue', () => {
  const mockChartData = {
    labels: ['A', 'B'],
    datasets: [{
      label: '测试图表',
      data: [60, 40],
      backgroundColor: ['#ff6384', '#36a2eb']
    }]
  }

  beforeEach(() => {
    ChartMock.mockClear()
  })

  it('成功渲染 canvas 元素', () => {
    const { getByTestId } = render(PieChart, {
      props: { chartData: mockChartData }
    })

    expect(getByTestId('chart-canvas')).toBeTruthy()
  })

  it('初始化 Chart.js 并使用传入数据', () => {
    render(PieChart, {
      props: { chartData: mockChartData }
    })

    expect(ChartMock).toHaveBeenCalledTimes(1)

    const chartCall = ChartMock.mock.calls[0][1]
    expect(chartCall.type).toBe('pie')
    expect(chartCall.data).toEqual(mockChartData)
  })
})
