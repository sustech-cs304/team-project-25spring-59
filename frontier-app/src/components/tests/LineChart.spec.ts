// tests/unit/components/LineChart.spec.ts
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { render } from '@testing-library/vue'
import LineChart from '../LineChart.vue'
import Chart from 'chart.js/auto'

// Mock Chart.js 构造函数
vi.mock('chart.js/auto', () => {
  return {
    default: vi.fn()
  }
})

// 用类型断言拿到 mock 实例
const ChartMock = Chart as unknown as ReturnType<typeof vi.fn>

describe('LineChart.vue', () => {
  const mockChartData = {
    labels: ['Jan', 'Feb', 'Mar'],
    datasets: [
      {
        label: '销售额',
        data: [100, 200, 300],
        borderColor: 'blue'
      }
    ]
  }

  beforeEach(() => {
    ChartMock.mockClear()
  })

  it('应渲染 canvas 元素', () => {
    const { container } = render(LineChart, {
      props: { chartData: mockChartData }
    })

    const canvas = container.querySelector('canvas')
    expect(canvas).toBeTruthy()
  })

  it('应使用 props 初始化 Chart 实例', () => {
    render(LineChart, {
      props: { chartData: mockChartData }
    })

    expect(ChartMock).toHaveBeenCalledTimes(1)

    const config = ChartMock.mock.calls[0][1]
    expect(config.type).toBe('line')
    expect(config.data).toEqual(mockChartData)
  })
})
