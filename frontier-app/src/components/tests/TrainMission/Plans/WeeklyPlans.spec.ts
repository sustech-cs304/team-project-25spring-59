import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount, flushPromises } from '@vue/test-utils'
import WeeklyPlan from '../../../TrainMission/Plans/Weekly_Plan.vue'
import dayjs from 'dayjs'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

// ✅ Mock TaskPanel
vi.mock('@/components/TrainMission/Plans/TaskPanel.vue', () => ({
  default: {
    name: 'TaskPanel',
    props: ['title', 'tasks', 'panelStyle'],
    template: `<div class="mock-task-panel">{{ title }}</div>`
  }
}))

// ✅ mock localStorage
vi.stubGlobal('localStorage', {
  getItem: vi.fn(() => 'user123')
})

describe('WeeklyPlan.vue', () => {
  let wrapper: any

  beforeEach(async () => {
    // ✅ mock axios 动态导入（局部 spy）
    const axios = await vi.importActual<typeof import('axios')>('axios')
    vi.spyOn(axios.default, 'post').mockImplementation(() =>
      Promise.resolve({
        data: {
          training_items: ['**深蹲 30 次**', '**俯卧撑 20 次**']
        }
      })
    )

    wrapper = mount(WeeklyPlan, {
      global: {
        plugins: [ElementPlus]
      }
    })

    await flushPromises()
  })

  it('renders current date range', () => {
    const today = dayjs()
    const expected = `${today.startOf('week').add(1, 'day').format('YYYY年M月D日')} - ${today.endOf('week').add(1, 'day').format('M月D日')}`
    expect(wrapper.find('.date-range').text()).toBe(expected)
  })

  it('renders 7 TaskPanels', () => {
    const taskPanels = wrapper.findAllComponents({ name: 'TaskPanel' })
    expect(taskPanels.length).toBe(7)
  })

  it('calls axios.post 7 times', async () => {
    const axios = await vi.importActual<typeof import('axios')>('axios')
    expect((axios.default.post as any).mock.calls.length).toBe(7)
    expect(wrapper.vm.weekTasks[0].tasks[0]).toBe('深蹲 30 次')
  })

  it('clicking nextWeek updates date', async () => {
    const initialDate = wrapper.vm.currentDate.format('YYYY-MM-DD')
    await wrapper.findAll('button')[1].trigger('click') // 下一周
    await flushPromises()
    const updatedDate = wrapper.vm.currentDate.format('YYYY-MM-DD')
    expect(updatedDate).not.toBe(initialDate)
  })

  it('clicking prevWeek updates date', async () => {
    const initialDate = wrapper.vm.currentDate.format('YYYY-MM-DD')
    await wrapper.findAll('button')[0].trigger('click') // 上一周
    await flushPromises()
    const updatedDate = wrapper.vm.currentDate.format('YYYY-MM-DD')
    expect(updatedDate).not.toBe(initialDate)
  })
})
