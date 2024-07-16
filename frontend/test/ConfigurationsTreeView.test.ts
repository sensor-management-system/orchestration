/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
import Vue from 'vue'
import Vuetify from 'vuetify'

import { mount, createLocalVue } from '@vue/test-utils'

import { DateTime } from 'luxon'

// @ts-ignore
import ConfigurationsTreeView from '@/components/ConfigurationsTreeView.vue'

import { Contact } from '@/models/Contact'
import { Device } from '@/models/Device'
import { DeviceMountAction } from '@/models/DeviceMountAction'
import { Platform } from '@/models/Platform'
import { PlatformMountAction } from '@/models/PlatformMountAction'

import { DeviceNode } from '@/viewmodels/DeviceNode'
import { PlatformNode } from '@/viewmodels/PlatformNode'
import { ConfigurationsTreeNode } from '@/viewmodels/ConfigurationsTreeNode'
import { ConfigurationsTree } from '@/viewmodels/ConfigurationsTree'

import { shortenMiddle } from '@/utils/stringHelpers'

Vue.use(Vuetify)

const contact = new Contact()
const date = DateTime.utc(2020, 2, 3, 0, 0, 0, 0)

describe('ConfigurationsTreeView', () => {
  const createWrapper = (tree: ConfigurationsTree, value: ConfigurationsTreeNode | null = null) => {
    const localVue = createLocalVue()
    // register the used filter explicitly
    localVue.filter('shortenMiddle', shortenMiddle)
    const vuetify = new Vuetify()

    return mount(ConfigurationsTreeView, {
      localVue,
      vuetify,
      propsData: {
        value,
        tree
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
    const node = new PlatformNode(PlatformMountAction.createFromObject({
      id: '',
      platform,
      parentPlatform: null,
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0,
      epsgCode: '',
      x: null,
      y: null,
      z: null,
      elevationDatumName: '',
      elevationDatumUri: '',
      beginContact: contact,
      endContact: null,
      beginDate: date,
      endDate: null,
      beginDescription: 'Platform mount',
      endDescription: '',
      label: ''
    }))
    node.getTree().push(new DeviceNode(DeviceMountAction.createFromObject({
      id: '',
      device,
      parentPlatform: platform,
      parentDevice: null,
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0,
      epsgCode: '',
      x: null,
      y: null,
      z: null,
      elevationDatumName: '',
      elevationDatumUri: '',
      beginContact: contact,
      endContact: null,
      beginDate: date,
      endDate: null,
      beginDescription: 'Device mount',
      endDescription: '',
      label: ''
    })))

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
    const node = new PlatformNode(PlatformMountAction.createFromObject({
      id: '',
      platform,
      parentPlatform: null,
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0,
      epsgCode: '',
      x: null,
      y: null,
      z: null,
      elevationDatumName: '',
      elevationDatumUri: '',
      beginContact: contact,
      endContact: null,
      beginDate: date,
      endDate: null,
      beginDescription: 'Platform mount',
      endDescription: '',
      label: ''
    }))
    node.getTree().push(new DeviceNode(DeviceMountAction.createFromObject({
      id: '',
      device,
      parentPlatform: platform,
      parentDevice: null,
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0,
      epsgCode: '',
      x: null,
      y: null,
      z: null,
      elevationDatumName: '',
      elevationDatumUri: '',
      beginContact: contact,
      endContact: null,
      beginDate: date,
      endDate: null,
      beginDescription: 'Device mount',
      endDescription: '',
      label: ''
    })))

    const tree = ConfigurationsTree.fromArray([node])

    const wrapper: any = createWrapper(tree, node as ConfigurationsTreeNode)
    // the used v-treeview requires an array of node ids
    expect(wrapper.vm.selectedNodeSingletonList).toHaveLength(1)
    expect(wrapper.vm.selectedNodeSingletonList[0]).toEqual(node)
  })

  it('should trigger an input event when a node is selected', () => {
    const platform = new Platform()
    platform.id = '1'
    platform.shortName = 'a platform'
    const device = new Device()
    device.id = '1'
    device.shortName = 'a sensor'
    const node = new PlatformNode(PlatformMountAction.createFromObject({
      id: '',
      platform,
      parentPlatform: null,
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0,
      epsgCode: '',
      x: null,
      y: null,
      z: null,
      elevationDatumName: '',
      elevationDatumUri: '',
      beginContact: contact,
      endContact: null,
      beginDate: date,
      endDate: null,
      beginDescription: 'Platform mount',
      endDescription: '',
      label: ''
    }))
    node.getTree().push(new DeviceNode(DeviceMountAction.createFromObject({
      id: '',
      device,
      parentPlatform: platform,
      parentDevice: null,
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0,
      epsgCode: '',
      x: null,
      y: null,
      z: null,
      elevationDatumName: '',
      elevationDatumUri: '',
      beginContact: contact,
      endContact: null,
      beginDate: date,
      endDate: null,
      beginDescription: 'Device mount',
      endDescription: '',
      label: ''
    })))

    const tree = ConfigurationsTree.fromArray([node])

    const wrapper: any = createWrapper(tree)
    // the used v-treeview requires an array of node ids
    wrapper.vm.selectedNodeSingletonList = [node]

    expect(wrapper.emitted().input).toBeTruthy()
    expect(wrapper.emitted().input.length).toBe(1)
    expect(wrapper.emitted().input[0]).toEqual([node])
  })
})
