
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { render, fireEvent } from '@testing-library/vue'
import FooterMenu from '../FooterMenu.vue'
import { useRouter } from 'vue-router'

// ✅ mock vue-router push 方法
vi.mock('vue-router', () => {
  return {
    useRouter: vi.fn()
  }
})
/// <reference types="vitest" />
describe('FooterMenu.vue', () => {
  let pushMock: ReturnType<typeof vi.fn>

  beforeEach(() => {
    pushMock = vi.fn()
    ;(useRouter as unknown as vi.Mock).mockReturnValue({ push: pushMock })

    // 设置用户 ID 以测试 handleTrainMissionClick
    localStorage.setItem('user_id', 'test_user_123')
  })

  afterEach(() => {
    vi.restoreAllMocks()
    localStorage.clear()
  })

  it('应渲染所有菜单项名称', () => {
    const { getByText } = render(FooterMenu)

    const labels = [
      '训练任务',
      '健身排课',
      '积分排行',
      '社交分享',
      '在线挑战',
      '个人中心',
      'Button7',
      'Button8'
    ]

    for (const label of labels) {
      expect(getByText(label)).toBeTruthy()
    }
  })

  it('应渲染所有菜单图标', () => {
    const { container } = render(FooterMenu)
    const icons = container.querySelectorAll('img.menu-icon')
    expect(icons.length).toBe(8)
  })

  it('应更新并显示当前时间', async () => {
      const { findByText } = render(FooterMenu)

      const now = new Date().toLocaleTimeString()
      const partialMatch = now.slice(0, 5)

      const timeNode = await findByText((content) => content.includes(partialMatch))
      expect(timeNode).toBeTruthy()
    })


  it('点击训练任务应调用 handleTrainMissionClick 并跳转', async () => {
    const { getByText } = render(FooterMenu)

    const trainMission = getByText('训练任务')
    await fireEvent.click(trainMission)

    expect(pushMock).toHaveBeenCalledWith('/trainMission')
  })

  it('点击其他菜单项应调用 router.push 对应路径', async () => {
    const { getByText } = render(FooterMenu)

    const gym = getByText('健身排课')
    await fireEvent.click(gym)
    expect(pushMock).toHaveBeenCalledWith('/gym')

    const leaderboard = getByText('积分排行')
    await fireEvent.click(leaderboard)
    expect(pushMock).toHaveBeenCalledWith('/leaderboard')

    const personal = getByText('个人中心')
    await fireEvent.click(personal)
    expect(pushMock).toHaveBeenCalledWith('/personal')
  })
})
