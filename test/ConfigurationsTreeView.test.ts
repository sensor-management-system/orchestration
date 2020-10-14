import Vue from 'vue'
import Vuetify from 'vuetify'

import { mount, createLocalVue } from '@vue/test-utils'

// @ts-ignore
import ConfigurationsTreeView from '@/components/ConfigurationsTreeView.vue'
import { Device } from '@/models/Device'
import { Platform } from '@/models/Platform'
import { DeviceNode } from '@/models/DeviceNode'
import { PlatformNode } from '@/models/PlatformNode'
import { ConfigurationsTreeNode } from '@/models/ConfigurationsTreeNode'
import { ConfigurationsTree } from '@/models/ConfigurationsTree'

Vue.use(Vuetify)

describe('ConfigurationsTreeView', () => {
  const createWrapper = (value: ConfigurationsTree, selected: ConfigurationsTreeNode|null = null) => {
    const localVue = createLocalVue()
    const vuetify = new Vuetify()

    return mount(ConfigurationsTreeView, {
      localVue,
      vuetify,
      propsData: {
        value,
        selected
      }
    })
  }

  it('should return an empty array when no node is selected', () => {
    const platform = new Platform()
    platform.id = '1'
    platform.shortName = 'a platform'
    const device = new Device()
    device.id = '1'
    device.shortName = 'a sensor'
    const node = new PlatformNode(platform)
    node.getTree().push(new DeviceNode(device))

    const tree = ConfigurationsTree.fromArray([node])

    const wrapper: any = createWrapper(tree)
    // the used v-treeview requires an array of node ids
    expect(wrapper.vm.selectedNodeSingletonList).toHaveLength(0)
  })

  it('should return an array with one node id when a node is selected', () => {
    const platform = new Platform()
    platform.id = '1'
    platform.shortName = 'a platform'
    const device = new Device()
    device.id = '1'
    device.shortName = 'a sensor'
    const node = new PlatformNode(platform)
    node.getTree().push(new DeviceNode(device))

    const tree = ConfigurationsTree.fromArray([node])

    const wrapper: any = createWrapper(tree, node as ConfigurationsTreeNode)
    // the used v-treeview requires an array of node ids
    expect(wrapper.vm.selectedNodeSingletonList).toHaveLength(1)
    expect(wrapper.vm.selectedNodeSingletonList[0]).toEqual(node.id)
  })

  it('should trigger a select event when a node is selected', () => {
    const platform = new Platform()
    platform.id = '1'
    platform.shortName = 'a platform'
    const device = new Device()
    device.id = '1'
    device.shortName = 'a sensor'
    const node = new PlatformNode(platform)
    node.getTree().push(new DeviceNode(device))

    const tree = ConfigurationsTree.fromArray([node])

    const wrapper: any = createWrapper(tree)
    // the used v-treeview requires an array of node ids
    wrapper.vm.selectedNodeSingletonList = [node.id]

    expect(wrapper.emitted().select).toBeTruthy()
    expect(wrapper.emitted().select.length).toBe(1)
    expect(wrapper.emitted().select[0]).toEqual([node])
  })
})
