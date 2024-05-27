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
import StringSelect from '@/components/StringSelect.vue'

Vue.use(Vuetify)

describe('StringSelect', () => {
  let wrapper: any

  /*
   * setup
   */

  beforeEach(() => {
    const localVue = createLocalVue()
    const vuetify = new Vuetify()

    wrapper = mount(StringSelect, {
      localVue,
      vuetify,
      propsData: {
        value: ['A'],
        items: ['A', 'B'],
        color: 'red',
        label: 'Add a string'
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

  it('should trigger an update event when a string-item is removed', () => {
    wrapper.vm.remove('A')
    expect(wrapper.emitted('input')).toBeTruthy()
  })

  it('should trigger an event with a string array with a length decreased by 1 when a string-item is removed', () => {
    wrapper.vm.remove('A')
    expect(wrapper.emitted('input')[0][0]).toHaveLength(0)
  })

  /*
   * adding
   */

  it('should trigger an update event when a string-item is added', () => {
    wrapper.vm.add('B')
    expect(wrapper.emitted('input')).toBeTruthy()
  })

  it('should trigger an event with a string array with a length increased by 1 when a string-item is added', () => {
    wrapper.vm.add('B')
    expect(wrapper.emitted('input')[0][0]).toHaveLength(2)
  })
})
