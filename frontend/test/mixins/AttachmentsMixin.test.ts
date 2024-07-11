/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2023
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
        description: 'The manual',
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
        description: 'One manual',
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
        description: 'Some manual',
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
        description: '',
        isUpload: false,
        createdAt: null
      })
      const filename = wrapper.vm.filename(attachment)
      const expectedFilename = 'abc.jpeg'
      expect(filename).toEqual(expectedFilename)
    })
  })
})
