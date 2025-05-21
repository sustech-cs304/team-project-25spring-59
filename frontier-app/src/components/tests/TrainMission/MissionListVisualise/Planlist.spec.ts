/// <reference types="vitest" />
import { render, fireEvent, waitFor } from '@testing-library/vue'
import PlanList from '../../../TrainMission/MissionListVisualize/Planlist.vue'
import { describe, it, vi, expect, beforeEach } from 'vitest'

// mock axios
vi.mock('axios')
import axios from 'axios'
const mockedAxios = axios as unknown as {
  post: ReturnType<typeof vi.fn>
}

beforeEach(() => {
  vi.stubGlobal('localStorage', {
    getItem: vi.fn(() => '123'),
    setItem: vi.fn(),
    removeItem: vi.fn()
  })

  mockedAxios.post = vi.fn()
})

describe('PlanList.vue', () => {
  it('应正确渲染标题和用户 ID', async () => {
    mockedAxios.post.mockResolvedValue({ data: { records: [] } })

    const { getByText } = render(PlanList)

    await waitFor(() => {
      expect(getByText('运动计划列表')).toBeTruthy()
      expect(getByText(/用户ID：123/)).toBeTruthy()
    })
  })

  it('点击 Add Record 应显示弹窗', async () => {
    mockedAxios.post.mockResolvedValue({ data: { records: [] } })

    const { getByText, queryByText } = render(PlanList)

    const addBtn = getByText('Add Record')
    await fireEvent.click(addBtn)

    expect(queryByText('新建训练记录')).toBeTruthy()
  })

  it('点击 Delete Record 时未选择应提示警告', async () => {
    // @ts-ignore
    global.alert = vi.fn()
    mockedAxios.post.mockResolvedValue({ data: { records: [] } })

    const { getByText } = render(PlanList)
    const deleteBtn = getByText('Delete Record')
    await fireEvent.click(deleteBtn)

    // @ts-ignore
    expect(global.alert).toHaveBeenCalledWith('请先选择要删除的训练记录')
  })

  it('应发起网络请求加载记录', async () => {
    mockedAxios.post.mockResolvedValue({
      data: {
        records: [
          {
            id: 1,
            activity_type: '跑步',
            duration_minutes: 30,
            calories: 100,
            average_heart_rate: 90,
            start_time: '2025-05-01T10:00:00Z',
            end_time: '2025-05-01T10:30:00Z',
            is_completed: true
          }
        ]
      }
    })

    const { getByText } = render(PlanList)

    await waitFor(() => {
      expect(getByText('✅ 已完成记录')).toBeTruthy()
    })
  })
})
