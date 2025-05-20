import { describe, it, expect } from 'vitest'
import { render } from '@testing-library/vue'
import NavHeader from '../../TrainMission/Header.vue'

describe('NavHeader.vue', () => {
  const basePath = '/mockBase/'

  it('应渲染 logo 图标', () => {
    const { container } = render(NavHeader, {
      props: { base: basePath }
    })
    const logo = container.querySelector('.logo img')
    expect(logo).toBeTruthy()
    expect(logo?.getAttribute('src')).toMatch(/^data:image\/svg\+xml/)
  })

  it('应渲染全部导航链接，并正确拼接 base', () => {
    const { getByText } = render(NavHeader, {
      props: { base: basePath }
    })

    const links = [
      { name: '首页', url: 'TrainMission' },
      { name: '运动界面', url: 'TrainMission/Specification' },
      { name: '任务列表', url: 'TrainMission/Plans' },
      { name: '训练数据', url: 'TrainMission/Dashboard' },
      { name: '返回大厅', url: 'carousel' }
    ]

    for (const link of links) {
      const linkEl = getByText(link.name)
      expect(linkEl).toBeTruthy()
      expect(linkEl.getAttribute('href')).toBe(basePath + link.url)
    }
  })
})
