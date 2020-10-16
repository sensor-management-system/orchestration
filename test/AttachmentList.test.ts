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
import AttachmentList from '@/components/AttachmentList.vue'
import { Attachment } from '@/models/Attachment'

Vue.use(Vuetify)

describe('AttachmentList', () => {
  let wrapper: any

  /*
   * setup
   */

  beforeEach(() => {
    const localVue = createLocalVue()
    const vuetify = new Vuetify()
    // disable "[Vuetify] Unable to locate target [data-app]" warnings:
    document.body.setAttribute('data-app', 'true')

    wrapper = mount(AttachmentList, {
      localVue,
      vuetify,
      propsData: {
        value: [
          Attachment.createFromObject({
            id: '1',
            url: 'https://foo.pdf',
            label: 'Manual'
          }),
          Attachment.createFromObject({
            id: '2',
            url: 'https://bar.png',
            label: 'Product Image'
          })
        ] as Attachment[]
      }
    })
  })

  /*
   * initial state
   */

  it('should be a Vue instance', () => {
    expect(wrapper.vm).toBeTruthy()
  })

  /*
   * add by URL
   */

  it('should trigger an input event when add button is clicked', async () => {
    await wrapper.get('input[type="radio"][value="url"]').trigger('click')
    wrapper.get('input[type="url"]').setValue('https://foo.bar/document.docx')
    await wrapper.get('button[data-role="add-attachment"]').trigger('click')
    expect(wrapper.emitted('input')).toBeTruthy()
  })

  it('must not trigger an input event when the url is empty and the add button is clicked', async () => {
    await wrapper.get('input[type="radio"][value="url"]').trigger('click')
    wrapper.get('input[type="url"]').setValue('')
    await wrapper.get('button[data-role="add-attachment"]').trigger('click')
    expect(wrapper.emitted('input')).toBeFalsy()
  })

  it('should trigger an input event with a attachment array length increased by 1 when the add button is clicked', async () => {
    await wrapper.get('input[type="radio"][value="url"]').trigger('click')
    wrapper.get('input[type="url"]').setValue('https://foo.bar/document.docx')
    await wrapper.get('button[data-role="add-attachment"]').trigger('click')
    expect(wrapper.emitted('input')[0][0]).toHaveLength(3)
  })

  /*
   * removing
   */

  it('should trigger an input event when delete button is clicked', async () => {
    await wrapper.get('[data-role="delete-attachment"]').trigger('click')
    expect(wrapper.emitted('input')).toBeTruthy()
  })

  it('should trigger an input event with a fields array length decreased by 1 when the delete buttom is clicked', async () => {
    await wrapper.get('[data-role="delete-attachment"]').trigger('click')
    expect(wrapper.emitted('input')[0][0]).toHaveLength(1)
  })
})
