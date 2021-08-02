/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020-2021
 * - Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
 * - Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for
 *   Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * Parts of this program were developed within the context of the
 * following publicly funded projects or measures:
 * - Helmholtz Earth and Environment DataHub
 *   (https://www.helmholtz.de/en/research/earth_and_environment/initiatives/#h51095)
 *
 * Licensed under the HEESIL, Version 1.0 or - as soon they will be
 * approved by the "Community" - subsequent versions of the HEESIL
 * (the "Licence").
 *
 * You may not use this work except in compliance with the Licence.
 *
 * You may obtain a copy of the Licence at:
 * https://gitext.gfz-potsdam.de/software/heesil
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the Licence is distributed on an "AS IS" basis,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
 * implied. See the Licence for the specific language governing
 * permissions and limitations under the Licence.
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

Vue.use(Vuetify)

const contact = new Contact()
const date = DateTime.utc(2020, 2, 3, 0, 0, 0, 0)

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
    const node = new PlatformNode(PlatformMountAction.createFromObject({
      id: '',
      platform,
      parentPlatform: null,
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0,
      contact,
      date,
      description: 'Platform mount'
    }))
    node.getTree().push(new DeviceNode(DeviceMountAction.createFromObject({
      id: '',
      device,
      parentPlatform: platform,
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0,
      contact,
      date,
      description: 'Device mount'
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
      contact,
      date,
      description: 'Platform mount'
    }))
    node.getTree().push(new DeviceNode(DeviceMountAction.createFromObject({
      id: '',
      device,
      parentPlatform: platform,
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0,
      contact,
      date,
      description: 'Device mount'
    })))

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
    const node = new PlatformNode(PlatformMountAction.createFromObject({
      id: '',
      platform,
      parentPlatform: null,
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0,
      contact,
      date,
      description: 'Platform mount'
    }))
    node.getTree().push(new DeviceNode(DeviceMountAction.createFromObject({
      id: '',
      device,
      parentPlatform: platform,
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0,
      contact,
      date,
      description: 'Device mount'
    })))

    const tree = ConfigurationsTree.fromArray([node])

    const wrapper: any = createWrapper(tree)
    // the used v-treeview requires an array of node ids
    wrapper.vm.selectedNodeSingletonList = [node.id]

    expect(wrapper.emitted().select).toBeTruthy()
    expect(wrapper.emitted().select.length).toBe(1)
    expect(wrapper.emitted().select[0]).toEqual([node])
  })
})
