import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { mount, flushPromises } from '@vue/test-utils'
import HomePage from '../Carousel.vue'

vi.mock('vue-router', () => ({
  useRouter: () => ({ push: vi.fn() })
}))
vi.mock('pixi.js', () => ({
  Application: vi.fn().mockImplementation(() => ({
    view: document.createElement('canvas'),
    stage: { addChild: vi.fn() }
  })),
  Assets: {
    load: vi.fn().mockResolvedValue({ spineData: {} })
  }
}))
vi.mock('pixi-spine', () => ({
  Spine: vi.fn().mockImplementation(() => ({
    state: { hasAnimation: () => true, setAnimation: vi.fn() },
    scale: { set: vi.fn() },
    autoUpdate: true, x: 0, y: 0
  }))
}))
vi.mock('@pixi/sound', () => ({
  sound: { add: vi.fn(), play: vi.fn() }
}))

beforeEach(() => {
  document.body.innerHTML = '<div id="background"></div>'
  vi.stubGlobal('HTMLMediaElement', class {
    play = vi.fn()
    pause = vi.fn()
    onended = null
  })
})

afterEach(() => {
  document.body.innerHTML = ''
  vi.restoreAllMocks()
})

describe('HomePage.vue', () => {
  it('应渲染背景容器', async () => {
    const wrapper = mount(HomePage, {
      global: {
        stubs: {
          'router-view': true,
          'a-progress': true
        }
      }
    })
    await flushPromises()
    expect(wrapper.find('#background').exists()).toBe(true)
  })

  it('点击右上角感叹号应弹出关于弹窗', async () => {
    const wrapper = mount(HomePage, {
      global: {
        stubs: {
          'router-view': true,
          'a-progress': true
        }
      }
    })

    await wrapper.find('.alert-box').trigger('click')
    expect(wrapper.find('.modal-content').exists()).toBe(true)
  })
})
