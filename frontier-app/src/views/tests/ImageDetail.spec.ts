/// <reference types="vitest" />
import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import ImageDetail from '../ImageDetail.vue'

// mock vue-router
const pushMock = vi.fn()
vi.mock('vue-router', () => ({
  useRoute: () => ({ params: { id: '3' } }),
  useRouter: () => ({ push: pushMock })
}))

describe('ImageDetail.vue', () => {
  it('应正确渲染图片与描述文字', () => {
    const wrapper = mount(ImageDetail, {
      global: {
        stubs: {
          'el-button': {
            template: '<button><slot /></button>'
          }
        }
      }
    })

    const img = wrapper.find('img')
    expect(img.attributes('src')).toContain('03.jpg')
    expect(wrapper.text()).toContain('编号为 3 的图片')
  })

  it('点击按钮应导航回 /carousel', async () => {
    const wrapper = mount(ImageDetail, {
      global: {
        stubs: {
          'el-button': {
            template: '<button @click="$emit(\'click\')"><slot /></button>'
          }
        }
      }
    })

    const button = wrapper.find('button')
    await button.trigger('click')

    expect(pushMock).toHaveBeenCalledWith('/carousel')
  })
})
