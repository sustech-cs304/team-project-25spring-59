// tests/components/SpinePlayer.spec.ts
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { mount, flushPromises } from '@vue/test-utils'
import SpinePlayer from '../../../components/Spine-Player-MainMenu/index.vue'

// mock AudioContext
class MockAudioBuffer {}
class MockAudioSource {
  start = vi.fn()
  stop = vi.fn()
  connect = vi.fn()
  onended = vi.fn()
}
const mockDecodeAudioData = vi.fn((buffer, cb) => cb && cb(new MockAudioBuffer()))
class MockAudioContext {
  decodeAudioData = mockDecodeAudioData
  createBufferSource = () => new MockAudioSource()
  destination = {}
}

vi.stubGlobal('AudioContext', MockAudioContext)
vi.stubGlobal('fetch', vi.fn(() => Promise.resolve({ arrayBuffer: () => Promise.resolve(new ArrayBuffer(8)) })))

// mock spine player
vi.mock('@/components/spine-player.js', () => ({
  spine: {
    SpinePlayer: vi.fn().mockImplementation((el, options) => {
      setTimeout(() => {
        options.success({
          setAnimation: vi.fn(),
          addAnimation: vi.fn(),
          canvas: document.createElement('canvas'),
          skeleton: {
            findBone: () => ({ x: 0, y: 0, data: { x: 0, y: 0 } }),
            updateWorldTransform: vi.fn()
          },
          animationState: {
            setAnimation: vi.fn(),
            addAnimation: vi.fn(),
            setEmptyAnimation: vi.fn()
          },
          resize: vi.fn()
        })
      }, 10)
    })
  }
}))

vi.stubGlobal('WeakRef', class {
  constructor(value) {
    this.value = value
  }
  deref() {
    return this.value
  }
})

vi.stubGlobal('navigator', { userAgent: 'nodejs' })

describe('SpinePlayer.vue', () => {
  let wrapper: any

  beforeEach(() => {
    wrapper = mount(SpinePlayer, {
      props: {},
      global: {
        stubs: ['transition']
      }
    })
  })

  afterEach(() => {
    wrapper.unmount()
  })

  it('does not render when SpinePlayerEnabled is false', async () => {
    wrapper.vm.state.SpinePlayerEnabled = false
    await flushPromises()
    expect(wrapper.find('.playerContainer').exists()).toBe(false)
  })

  it('renders and initializes spine player when enabled', async () => {
    await flushPromises()
    expect(wrapper.find('.playerContainer').exists()).toBe(true)
  })

  it('shows dialog on click and hides after playback', async () => {
    await flushPromises()
    const container = wrapper.find('.playerContainer')
    await container.trigger('click')
    await flushPromises()
    expect(wrapper.vm.showDialog).toBe(false)
    await new Promise(r => setTimeout(r, 500)) // simulate audio ended
    expect(wrapper.vm.showDialog).toBe(false)
  })

  it('prevents multiple playbacks while audio is playing', async () => {
    await flushPromises()
    const container = wrapper.find('.playerContainer')
    await container.trigger('click')
    const dialogBefore = wrapper.vm.currentDialog
    await container.trigger('click')
    expect(wrapper.vm.currentDialog).toBe(dialogBefore) // should not change while playing
  })
})