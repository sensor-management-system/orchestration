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

// @ts-ignore
import EntitySelect from '@/components/EntitySelect.vue'
import { Contact } from '@/models/Contact'

Vue.use(Vuetify)

describe('EntitySelect', () => {
  let wrapper: any

  /*
   * setup
   */

  beforeEach(() => {
    const localVue = createLocalVue()
    const vuetify = new Vuetify()

    wrapper = mount(EntitySelect, {
      localVue,
      vuetify,
      propsData: {
        value: [Contact.createWithIdEMailAndNames('1', 'p1@mail.org', 'Per', 'son 1', 'stuff/per/son1')],
        fetchFunction: () => new Promise((resolve) => {
          resolve([
            Contact.createWithIdEMailAndNames('1', 'p1@mail.org', 'Per', 'son 1', 'stuff/per/son1'),
            Contact.createWithIdEMailAndNames('2', 'p2@mail.org', 'Pers', 'On 2', 'stuff/pers/On2')
          ])
        }),
        color: 'red',
        label: 'Add a contact'
      },
      data () {
        return {
          elements: [
            Contact.createWithIdEMailAndNames('1', 'p1@mail.org', 'Per', 'son 1', 'stuff/per/son1'),
            Contact.createWithIdEMailAndNames('2', 'p2@mail.org', 'Pers', 'On 2', 'stuff/pers/On2')]
        }
      }
    })
  })

  /*
   * initial state
   */

  it('should be a Vue instance', () => {
    expect(wrapper.vm).toBeTruthy()
  })

  it('should render one chip', () => {
    expect(wrapper.findAllComponents({ name: 'v-chip' })).toHaveLength(1)
  })

  /*
   * removing
   */

  it('should trigger an update event when a contact is removed', () => {
    wrapper.vm.remove('1')
    expect(wrapper.emitted('input')).toBeTruthy()
  })

  it('should trigger an event with a contact array with a length decreased by 1 when a contact is removed', () => {
    wrapper.vm.remove('1')
    expect(wrapper.emitted('input')[0][0]).toHaveLength(0)
  })

  /*
   * adding
   */

  it('should trigger an update event when a contact is added', () => {
    wrapper.vm.add('2')
    expect(wrapper.emitted('input')).toBeTruthy()
  })

  it('should trigger an event with a contact array with a length increased by 1 when a contact is added', () => {
    wrapper.vm.add('2')
    expect(wrapper.emitted('input')[0][0]).toHaveLength(2)
  })
})
