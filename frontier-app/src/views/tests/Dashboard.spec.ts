import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount, flushPromises } from '@vue/test-utils'
import Dashboard from '../Dashboard.vue'
import axios from 'axios'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

// ✅ Mock 子组件（图表）
vi.mock('../../components/LineChart.vue', () => ({
  default: { template: '<div class="line-chart" />' }
}))
vi.mock('../../components/PieChart.vue', () => ({
  default: { template: '<div class="pie-chart" />' }
}))

// ✅ Mock axios
vi.mock('axios')
const mockedAxios = axios as unknown as {
  post: ReturnType<typeof vi.fn>
}

describe('Dashboard.vue', () => {
  beforeEach(() => {
    mockedAxios.post = vi.fn().mockResolvedValue({
      data: {
        total_minutes: 100,
        estimated_calories: 800,
        '2025-05-01': 30,
        '2025-05-02': 40
      }
    })
  })

  it('应挂载并渲染标题', async () => {
    const wrapper = mount(Dashboard, {
      global: {
        plugins: [ElementPlus]
      }
    })
    await flushPromises()
    expect(wrapper.text()).toContain('📊 训练数据仪表板')
  })

  it('点击刷新按钮应调用 fetchTrainingData', async () => {
    const wrapper = mount(Dashboard, {
      global: {
        plugins: [ElementPlus]
      }
    })
    await flushPromises()
    const btn = wrapper.find('button')
    expect(btn.exists()).toBe(true)
    await btn.trigger('click')
    expect(mockedAxios.post).toHaveBeenCalled()
  })

  it('应包含图表组件', async () => {
    const wrapper = mount(Dashboard, {
      global: {
        plugins: [ElementPlus]
      }
    })
    await flushPromises()
    expect(wrapper.find('.line-chart').exists()).toBe(true)
    expect(wrapper.find('.pie-chart').exists()).toBe(true)
  })

  it('应显示训练记录表格', async () => {
    const wrapper = mount(Dashboard, {
      global: {
        plugins: [ElementPlus]
      }
    })
    await flushPromises()
    expect(wrapper.find('table').exists()).toBe(true)
  })
})
