import { describe, it, expect } from 'vitest'
import { render, fireEvent } from '@testing-library/vue'
import SpecDisplay from '../../TrainMission/Specification.vue'

describe('SpecDisplay.vue', () => {
  it('应渲染默认记录数据', () => {
    const { getByText } = render(SpecDisplay)

    expect(getByText('当前记录：周一 跑步')).toBeTruthy()
    expect(getByText('2025-04-20 | 有氧')).toBeTruthy()
    expect(getByText('128 bpm')).toBeTruthy()
    expect(getByText('8.2 km/h')).toBeTruthy()
    expect(getByText('320 kcal')).toBeTruthy()
    expect(getByText('已运动时间：25 分钟 / 总时长：40 分钟')).toBeTruthy()
  })

  it('应支持下拉选择切换记录', async () => {
    const { getByRole, getByText } = render(SpecDisplay)

    const select = getByRole('combobox') as HTMLSelectElement
    expect(select.value).toBe('1') // 默认值

    // 模拟选择记录 2
    await fireEvent.update(select, '2')

    expect(getByText('当前记录：周三 骑行')).toBeTruthy()
    expect(getByText('2025-04-17 | 耐力')).toBeTruthy()
    expect(getByText('112 bpm')).toBeTruthy()
    expect(getByText('16.5 km/h')).toBeTruthy()
    expect(getByText('410 kcal')).toBeTruthy()
    expect(getByText('已运动时间：30 分钟 / 总时长：60 分钟')).toBeTruthy()
  })
})
