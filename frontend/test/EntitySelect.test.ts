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
