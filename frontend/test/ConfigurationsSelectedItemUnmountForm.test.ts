/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2021
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */

import Vue from 'vue'
import Vuetify from 'vuetify'

import { mount, createLocalVue } from '@vue/test-utils'

// @ts-ignore
import ConfigurationsSelectedItemUnmountForm from '@/components/ConfigurationsSelectedItemUnmountForm.vue'

import { Contact } from '@/models/Contact'

const contact = new Contact()
contact.email = 'aa@bb.cc'

Vue.use(Vuetify)

describe('ConfigurationsSelectedItemUnmountForm', () => {
  const createWrapper = () => {
    const localVue = createLocalVue()
    const vuetify = new Vuetify()

    return mount(ConfigurationsSelectedItemUnmountForm, {
      localVue,
      vuetify,
      propsData: {
        readonly: false,
        contacts: [contact],
        currentUserMail: 'aa@bb.cc'
      },
      data () {
        return {
          contact,
          description: 'unmount description'
        }
      },
      mocks: {
        $auth: {
          user: {
            email: 'aa@bb.cc'
          }
        }
      }
    })
  }

  it('should trigger an add event when the button is clicked', async () => {
    const wrapper: any = createWrapper()

    await wrapper.get('button[data-role="remove-node"]').trigger('click')
    expect(wrapper.emitted('unmount')).toBeTruthy()
    expect(wrapper.emitted('unmount').length).toBe(1)
    const addPayload = wrapper.emitted('unmount')[0]
    expect(addPayload.length).toEqual(1)
    const addPayloadContent = addPayload[0]
    expect(addPayloadContent.contact).toEqual(contact)
    expect(addPayloadContent.description).toEqual('unmount description')
  })
})
