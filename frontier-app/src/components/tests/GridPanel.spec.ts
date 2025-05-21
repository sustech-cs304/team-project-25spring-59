// tests/unit/components/GridDisplay.spec.ts
import { describe, it, expect } from 'vitest'
import { render } from '@testing-library/vue'
import GridComponent from '../GridPanel.vue'
import '@testing-library/jest-dom'

describe('GridComponent.vue', () => {
  it('应正确渲染 4 个图片项', () => {
    const { container, getAllByRole, getAllByText } = render(GridComponent)

    // 验证 grid-item 数量
    const items = container.querySelectorAll('.grid-item')
    expect(items.length).toBe(4)

    // 验证所有图片渲染
    const images = getAllByRole('img')
    expect(images.length).toBe(4)

    // 验证每个标题是否出现
    expect(getAllByText(/图片说明/).length).toBe(4)

    // 验证图片 src 和 alt 存在（不做精确路径测试）
    images.forEach((img, index) => {
      expect(img).toHaveAttribute('src')
      expect(img).toHaveAttribute('alt', `图片说明 ${index + 1}`)
    })
  })
})
