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
import Vuex, { Store } from 'vuex'
import { DateTime } from 'luxon'

import { mount, createLocalVue } from '@vue/test-utils'

// @ts-ignore
import ConfigurationsSelectedItem from '@/components/ConfigurationsSelectedItem.vue'
// @ts-ignore
import ConfigurationsSelectedItemUnmountForm from '@/components/ConfigurationsSelectedItemUnmountForm.vue'

import { Contact } from '@/models/Contact'
import { Device } from '@/models/Device'
import { DeviceMountAction } from '@/models/DeviceMountAction'

import { DeviceNode } from '@/viewmodels/DeviceNode'
import { ConfigurationsTreeNode } from '@/viewmodels/ConfigurationsTreeNode'

const contact = new Contact()
contact.email = 'aa@bb.cc'
const date = DateTime.utc(2020, 2, 3, 0, 0, 0, 0)

const selectedDate = DateTime.utc(2020, 1, 1, 12, 0, 0)

Vue.use(Vuetify)

describe('ConfigurationsSelectedItem', () => {
  const createWrapper = (node: ConfigurationsTreeNode) => {
    const localVue = createLocalVue()
    localVue.use(Vuex)
    const vuetify = new Vuetify()

    const store = new Store({
      getters: {
        'oidc/userEMail': () => contact.email
      }
    })

    return mount(ConfigurationsSelectedItem, {
      localVue,
      vuetify,
      store,
      propsData: {
        value: node,
        selectedDate
      },
      data () {
        return {}
      }
    })
  }

  it('should return the description of a given device', () => {
    const device = new Device()
    device.id = '1'
    device.description = 'foo bar baz'

    const wrapper: any = createWrapper(new DeviceNode(DeviceMountAction.createFromObject({
      id: '',
      device,
      parentPlatform: null,
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0,
      contact,
      date,
      description: 'Device mount'
    })))
    expect(wrapper.vm.description).toEqual(device.description)
  })
  it('should trigger an input event when the remove button is clicked', async () => {
    const device = new Device()
    device.id = '1'
    device.description = 'foo bar baz'

    const node = new DeviceNode(DeviceMountAction.createFromObject({
      id: '',
      device,
      parentPlatform: null,
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0,
      contact,
      date,
      description: 'Device mount'
    }))

    const wrapper: any = createWrapper(node)
    await wrapper.get('.unmount-expansion-panel').trigger('click')
    const unmountForms = wrapper.findAllComponents(ConfigurationsSelectedItemUnmountForm)
    expect(unmountForms).toHaveLength(1)
    const unmountForm = unmountForms.at(0)
    expect(unmountForm.exists()).toBeTruthy()
    await unmountForm.setData({
      contact,
      description: 'dummy description'
    })
    expect(unmountForm.vm.$data.description).toEqual('dummy description')

    await wrapper.get('button[data-role="remove-node"]').trigger('click')
    expect(wrapper.emitted().remove).toBeTruthy()
    expect(wrapper.emitted().remove.length).toBe(1)
    const emitted = wrapper.emitted().remove[0]
    expect(emitted.length).toEqual(3)
    // we only test here the node, as the contact & description come from sub components
    expect(emitted[0]).toEqual(node)
    expect(emitted[2]).toEqual('dummy description')
    expect(emitted[1]).toEqual(contact)
  })

  describe('#isMountedOnSelctedDate', () => {
    it('should return true for the very same instance', () => {
      const device = new Device()
      device.id = '1'
      device.description = 'foo bar baz'

      const node = new DeviceNode(DeviceMountAction.createFromObject({
        id: '',
        device,
        parentPlatform: null,
        offsetX: 0,
        offsetY: 0,
        offsetZ: 0,
        contact,
        date: selectedDate,
        description: 'Device mount'
      }))

      const wrapper: any = createWrapper(node)

      expect(wrapper.vm.isMountedOnSelectedDate).toEqual(true)
    })
    it('should return false for a different date', () => {
      const device = new Device()
      device.id = '1'
      device.description = 'foo bar baz'

      const node = new DeviceNode(DeviceMountAction.createFromObject({
        id: '',
        device,
        parentPlatform: null,
        offsetX: 0,
        offsetY: 0,
        offsetZ: 0,
        contact,
        date: DateTime.utc(2021, 1, 1, 12, 0, 0),
        description: 'Device mount'
      }))

      const wrapper: any = createWrapper(node)

      expect(wrapper.vm.isMountedOnSelectedDate).toEqual(false)
    })
    it('should return true for the an instance with the same datetime', () => {
      const device = new Device()
      device.id = '1'
      device.description = 'foo bar baz'

      const node = new DeviceNode(DeviceMountAction.createFromObject({
        id: '',
        device,
        parentPlatform: null,
        offsetX: 0,
        offsetY: 0,
        offsetZ: 0,
        contact,
        date: DateTime.utc(2020, 1, 1, 12, 0, 0),
        description: 'Device mount'
      }))

      const wrapper: any = createWrapper(node)

      expect(wrapper.vm.isMountedOnSelectedDate).toEqual(true)
    })
  })
})
