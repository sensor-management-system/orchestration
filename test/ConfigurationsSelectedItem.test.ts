/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020
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

// @ts-ignore
import ConfigurationsSelectedItem from '@/components/ConfigurationsSelectedItem.vue'
import Device from '@/models/Device'
import { DeviceNode } from '@/models/DeviceNode'
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
