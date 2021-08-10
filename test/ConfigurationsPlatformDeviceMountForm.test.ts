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

import { mount, createLocalVue } from '@vue/test-utils'

// @ts-ignore
import ConfigurationsPlatformDeviceMountForm from '@/components/ConfigurationsPlatformDeviceMountForm.vue'

import { Contact } from '@/models/Contact'

const contact = new Contact()
contact.email = 'aa@bb.cc'

Vue.use(Vuetify)

describe('ConfigurationsPlatformDeviceMountForm', () => {
  const createWrapper = () => {
    const localVue = createLocalVue()
    localVue.use(Vuex)
    const vuetify = new Vuetify()

    const store = new Store({
      getters: {
        'oidc/userEMail': () => contact.email
      }
    })

    return mount(ConfigurationsPlatformDeviceMountForm, {
      localVue,
      vuetify,
      store,
      propsData: {
        dataRoleBtn: 'add-device',
        readonly: false,
        contacts: [contact]
      },
      data () {
        return {
          offsetX: 1,
          offsetY: 2,
          offsetZ: 3,
          contact,
          description: 'mount description'
        }
      }
    })
  }

  it('should trigger an add event when the button is clicked', async () => {
    const wrapper: any = createWrapper()

    await wrapper.get('button[data-role="add-device"]').trigger('click')
    expect(wrapper.emitted('add')).toBeTruthy()
    expect(wrapper.emitted('add').length).toBe(1)
    const addPayload = wrapper.emitted('add')[0]
    expect(addPayload.length).toEqual(1)
    const addPayloadContent = addPayload[0]
    expect(addPayloadContent.offsetX).toEqual(1)
    expect(addPayloadContent.offsetY).toEqual(2)
    expect(addPayloadContent.offsetZ).toEqual(3)
    expect(addPayloadContent.contact).toEqual(contact)
    expect(addPayloadContent.description).toEqual('mount description')
  })
})
