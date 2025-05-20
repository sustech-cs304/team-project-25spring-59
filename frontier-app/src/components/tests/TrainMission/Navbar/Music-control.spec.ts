import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import MusicControl from '../../../TrainMission/Navbar/Music-Control.vue'

describe('MusicControl.vue', () => {
  let mockAudio: HTMLAudioElement

  beforeEach(() => {
    // 创建一个假的 audio 元素并挂载到 DOM
    mockAudio = document.createElement('audio')
    mockAudio.id = 'background-music'
    mockAudio.volume = 1
    mockAudio.pause = vi.fn()
    mockAudio.play = vi.fn().mockResolvedValue(undefined)
    document.body.appendChild(mockAudio)
  })

  afterEach(() => {
    document.body.innerHTML = '' // 清理 DOM
  })

  it('renders the music icon', () => {
    const wrapper = mount(MusicControl)
    const icon = wrapper.find('i')
    expect(icon.exists()).toBe(true)
    expect(icon.classes()).toContain('iconfont')
    expect(icon.classes()).toContain('icon-stop') // 初始状态是暂停图标
  })

  it('toggles play and pause on click', async () => {
    const wrapper = mount(MusicControl)
    const icon = wrapper.find('.music-control')

    // 初始状态：暂停
    expect(mockAudio.pause).toHaveBeenCalled() // onMounted 中执行
    expect(mockAudio.play).not.toHaveBeenCalled()

    // 点击一次：播放
    await icon.trigger('click')
    expect(mockAudio.play).toHaveBeenCalled()
    expect(wrapper.find('i').classes()).toContain('icon-continue')

    // 点击两次：暂停
    await icon.trigger('click')
    expect(mockAudio.pause).toHaveBeenCalledTimes(2) // onMounted + 点击
    expect(wrapper.find('i').classes()).toContain('icon-stop')
  })
})
