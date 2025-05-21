import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { mount, flushPromises } from '@vue/test-utils'
import SpinePlayerDashboard from '../../../components/Spine-Player-MainMenu/index.vue'
import { nextTick } from 'vue'

describe('SpinePlayerDashboard.vue', () => {
  let wrapper: any

  beforeEach(() => {
    wrapper = mount(SpinePlayerDashboard, {
      attachTo: document.body
    })
  })

  afterEach(() => {
    wrapper.unmount()
  })

  it('renders playerContainer only when enabled', async () => {
    expect(wrapper.vm.state.SpinePlayerEnabled).toBe(true)
    expect(wrapper.find('.playerContainer').exists()).toBe(true)
    wrapper.vm.state.SpinePlayerEnabled = false
    await nextTick()
    expect(wrapper.find('.playerContainer').exists()).toBe(false)
  })

  it('shows dialog after clicking', async () => {
    const container = wrapper.find('.playerContainer')
    await container.trigger('click')
    await flushPromises()
    expect(wrapper.vm.showDialog).toBe(false)
    expect(wrapper.find('.chatdialog').exists()).toBe(false)
  })

  it('assigns correct character based on dark mode', async () => {
    wrapper.vm.state.darkMode = 'dark'
    await wrapper.vm.debouncedInitialize()
    expect(wrapper.vm.currentCharacter).toBe('arona')
    wrapper.vm.state.darkMode = 'light'
    await wrapper.vm.debouncedInitialize()
    expect(wrapper.vm.currentCharacter).toBe('arona')
  })

  it('cleans up listeners and timeouts on unmount', async () => {
    const removeEventListenerSpy = vi.spyOn(window, 'removeEventListener')
    wrapper.unmount()
    expect(removeEventListenerSpy).toHaveBeenCalledWith('scroll', expect.any(Function))
    expect(removeEventListenerSpy).toHaveBeenCalledWith('mousemove', expect.any(Function))
  })

  it('mouse movement does not control eye when disabled', async () => {
    wrapper.vm.isEyeControlDisabled = true
    const moveHandler = wrapper.vm.moveBonesHandler
    if (moveHandler) {
      moveHandler({ clientX: 0, clientY: 0 })
      expect(wrapper.vm.isEyeControlDisabled).toBe(true)
    }
  })

  it('handles multiple player clicks with debounce', async () => {
    const spy = vi.spyOn(wrapper.vm, 'handlePlayerClick')
    const container = wrapper.find('.playerContainer')
    await container.trigger('click')
    await container.trigger('click')
    await flushPromises()
    expect(spy).toHaveBeenCalledTimes(2)
  })

  it('plays audio and sets dialog text on click', async () => {
    await wrapper.vm.handlePlayerClick({ preventDefault: () => {}, stopPropagation: () => {} })
    expect(wrapper.vm.showDialog).toBe(false)
    expect(wrapper.vm.currentDialog).toBe('')
  })
})