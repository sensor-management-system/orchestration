import Vue from 'vue'
import Vuetify from 'vuetify'

import { mount, createLocalVue } from '@vue/test-utils'

// @ts-ignore
import ConfigurationsSelectedItem from '@/components/ConfigurationsSelectedItem.vue'
import Device from '@/models/Device'
import Platform from '@/models/Platform'
import { DeviceNode } from '@/models/DeviceNode'
import { PlatformNode } from '@/models/PlatformNode'
import { ConfigurationsTreeNode } from '@/models/ConfigurationsTreeNode'

Vue.use(Vuetify)

describe('ConfigurationsSelectedItem', () => {
  const createWrapper = (node: ConfigurationsTreeNode) => {
    const localVue = createLocalVue()
    const vuetify = new Vuetify()

    return mount(ConfigurationsSelectedItem, {
      localVue,
      vuetify,
      propsData: {
        value: node
      }
    })
  }

  it('should test if the given device node is a device or platform', () => {
    const device = new Device()
    device.id = '1'

    const wrapper: any = createWrapper(new DeviceNode(device))
    expect(wrapper.vm.isPlatform).toBeFalsy()
    expect(wrapper.vm.isDevice).toBeTruthy()
  })

  it('should test if the given platform node is a device or platform', () => {
    const platform = new Platform()
    platform.id = '1'

    const wrapper: any = createWrapper(new PlatformNode(platform))
    expect(wrapper.vm.isPlatform).toBeTruthy()
    expect(wrapper.vm.isDevice).toBeFalsy()
  })

  it('should return the description of a given device', () => {
    const device = new Device()
    device.id = '1'
    device.description = 'foo bar baz'

    const wrapper: any = createWrapper(new DeviceNode(device))
    expect(wrapper.vm.description).toEqual(device.description)
  })

  it('should trigger an input event when the remove button is clicked', async () => {
    const device = new Device()
    device.id = '1'
    device.description = 'foo bar baz'

    const node = new DeviceNode(device)

    const wrapper: any = createWrapper(node)
    await wrapper.get('button[data-role="remove-node"]').trigger('click')
    expect(wrapper.emitted().remove).toBeTruthy()
    expect(wrapper.emitted().remove.length).toBe(1)
    expect(wrapper.emitted().remove[0]).toEqual([node])
  })
})
