import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import DropdownMenu from '../../../TrainMission/Navbar/Dropdown-Menu.vue'

// @ts-ignore
vi.mock('../../../TrainMission/Navbar/Music-Control.vue', () => ({
  default: {
    template: '<div class="mock-music-control">MusicControl</div>'
  }
}))
//@ts-ignore
vi.mock('../../../TrainMission/Navbar/Search-Button.vue', () => ({
  default: {
    template: '<div class="mock-search-button">SearchButton</div>'
  }
}))

//@ts-ignore
vi.mock('../../../TrainMission/Navbar/ToggleSwitch.vue', () => ({
  default: {
    template: '<div class="mock-toggle-switch">ToggleSwitch</div>'
  }
}))

describe('DropdownMenu.vue', () => {
  it('should render properly', () => {
    const wrapper = mount(DropdownMenu)
    expect(wrapper.exists()).toBe(true)
    expect(wrapper.find('.dropdown-menu').exists()).toBe(true)
  })

  it('should contain child components', () => {
    const wrapper = mount(DropdownMenu)
    expect(wrapper.find('.mock-music-control').exists()).toBe(true)
    expect(wrapper.find('.mock-search-button').exists()).toBe(true)
    expect(wrapper.find('.mock-toggle-switch').exists()).toBe(true)
  })

  it('should apply showmenu=true style when attribute is set', async () => {
    const wrapper = mount(DropdownMenu, {
      attrs: {
        showmenu: 'true'
      }
    })
    expect(wrapper.attributes('showmenu')).toBe('true')
    expect(wrapper.classes()).toContain('dropdown-menu')
  })

  it('should apply showmenu=false style when attribute is set', async () => {
    const wrapper = mount(DropdownMenu, {
      attrs: {
        showmenu: 'false'
      }
    })
    expect(wrapper.attributes('showmenu')).toBe('false')
  })

  it('matches snapshot', () => {
    const wrapper = mount(DropdownMenu)
    expect(wrapper.html()).toMatchSnapshot()
  })
})
