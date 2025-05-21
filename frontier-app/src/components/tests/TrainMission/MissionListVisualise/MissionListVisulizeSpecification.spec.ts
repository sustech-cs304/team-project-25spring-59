/// <reference types="vitest" />
import { render, fireEvent } from '@testing-library/vue'
import RecordDisplay from '../../../TrainMission/MissionListVisualize/Specification.vue' // 替换为你实际的路径
import { describe, it, expect } from 'vitest'

describe('RecordDisplay.vue', () => {
  it('应显示默认的第一条记录信息', async () => {
    const { getByText } = render(RecordDisplay)

    // 检查顶部信息
    expect(getByText('当前记录：周一 跑步')).toBeTruthy()
    expect(getByText('2025-04-20 | 有氧')).toBeTruthy()

    // 检查数值区域
    expect(getByText('128 bpm')).toBeTruthy()
    expect(getByText('8.2 km/h')).toBeTruthy()
    expect(getByText('320 kcal')).toBeTruthy()

    // 检查进度条说明文字
    expect(getByText('已运动时间：25 分钟 / 总时长：40 分钟')).toBeTruthy()
  })

  it('应切换下拉框后更新数据显示', async () => {
    const { getByText, getByDisplayValue } = render(RecordDisplay)

    // 选择下拉项（切换到 "周三 骑行"）
    const select = getByDisplayValue('周一 跑步') as HTMLSelectElement
    await fireEvent.update(select, '2') // id 为 2 的项

    // 检查是否切换成功
    expect(getByText('当前记录：周三 骑行')).toBeTruthy()
    expect(getByText('2025-04-17 | 耐力')).toBeTruthy()
    expect(getByText('112 bpm')).toBeTruthy()
    expect(getByText('16.5 km/h')).toBeTruthy()
    expect(getByText('410 kcal')).toBeTruthy()
    expect(getByText('已运动时间：30 分钟 / 总时长：60 分钟')).toBeTruthy()
  })

  it('应正确渲染所有下拉选项', () => {
    const { getByDisplayValue, getByText } = render(RecordDisplay)
    expect(getByDisplayValue('周一 跑步')).toBeTruthy()
    expect(getByText('周三 骑行')).toBeTruthy()
  })
})
