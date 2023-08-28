/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020-2023
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
import { AttachmentsMixin } from '@/mixins/AttachmentsMixin'
import { Attachment } from '@/models/Attachment'

Vue.use(Vuetify)

describe('AttachmentsMixin', () => {
  const localVue = createLocalVue()
  const vuetify = new Vuetify()

  const wrapper: any = mount(AttachmentsMixin, {
    localVue,
    vuetify,
    propsData: {},
    template: '<div />'
  })

  describe('#filename', () => {
    it('should should return a very simple filename', () => {
      const attachment = Attachment.createFromObject({
        id: '1',
        url: 'https://foo.pdf',
        label: 'Manual',
        isUpload: false,
        createdAt: null
      })
      const filename = wrapper.vm.filename(attachment)
      const expectedFilename = 'foo.pdf'
      expect(filename).toEqual(expectedFilename)
    })
    it('should should return unkown filename of there is no url', () => {
      const attachment = Attachment.createFromObject({
        id: '1',
        url: '',
        label: 'Manual',
        isUpload: false,
        createdAt: null
      })
      const filename = wrapper.vm.filename(attachment)
      const expectedFilename = 'unknown filename'
      expect(filename).toEqual(expectedFilename)
    })
    it('should should be able to handle longer paths to a file', () => {
      const attachment = Attachment.createFromObject({
        id: '1',
        url: 'https://server/very/fancy/images/abc.jpeg',
        label: 'Manual',
        isUpload: false,
        createdAt: null
      })
      const filename = wrapper.vm.filename(attachment)
      const expectedFilename = 'abc.jpeg'
      expect(filename).toEqual(expectedFilename)
    })
    it('should should be able to handle cases with as / at the end', () => {
      const attachment = Attachment.createFromObject({
        id: '1',
        url: 'https://server/very/fancy/images/abc.jpeg/',
        label: 'Manual',
        isUpload: false,
        createdAt: null
      })
      const filename = wrapper.vm.filename(attachment)
      const expectedFilename = 'abc.jpeg'
      expect(filename).toEqual(expectedFilename)
    })
  })
})
