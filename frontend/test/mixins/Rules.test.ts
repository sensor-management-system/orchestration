/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2022
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
import { Rules } from '@/mixins/Rules'

Vue.use(Vuetify)

describe('Rules', () => {
  const localVue = createLocalVue()
  const vuetify = new Vuetify()

  const wrapper: any = mount(Rules, {
    localVue,
    vuetify,
    propsData: {},
    template: '<div />'
  })

  describe('#required', () => {
    it('should should return an error if a string value is empty', () => {
      expect(wrapper.vm.rules.required('')).not.toBe(true)
    })
    it('should should return an error if a string consists of whitespace only', () => {
      expect(wrapper.vm.rules.required('                   ')).not.toBe(true)
    })
    it('should should return an error if a value is undefined', () => {
      expect(wrapper.vm.rules.required(undefined)).not.toBe(true)
    })
    it('should should return an error if a value is null', () => {
      expect(wrapper.vm.rules.required(null)).not.toBe(true)
    })
    it('should should return true if a string is not empty', () => {
      expect(wrapper.vm.rules.required('abc')).toBe(true)
    })
    it('should should return true if a value is numeric', () => {
      expect(wrapper.vm.rules.required('0')).toBe(true)
      expect(wrapper.vm.rules.required('1')).toBe(true)
    })
    it('should should return true if a value is an object', () => {
      expect(wrapper.vm.rules.required({})).toBe(true)
      expect(wrapper.vm.rules.required([])).toBe(true)
    })
  })
  describe('#numeric', () => {
    it('should should return an error if a value is not numeric', () => {
      expect(wrapper.vm.rules.numeric('')).not.toBe(true)
      expect(wrapper.vm.rules.numeric('abc')).not.toBe(true)
      expect(wrapper.vm.rules.numeric({})).not.toBe(true)
    })
    it('should should return true if a value is numeric', () => {
      expect(wrapper.vm.rules.numeric(0)).toBe(true)
      expect(wrapper.vm.rules.numeric(1)).toBe(true)
    })
  })
  describe('#validUrl', () => {
    it('should should return an error if a value does not begin with http(s):// or ftp://', () => {
      expect(wrapper.vm.rules.validUrl('www.abc.de')).not.toBe(true)
      expect(wrapper.vm.rules.validUrl('//abc.de')).not.toBe(true)
    })
    it('should should return true if a value begins with http(s):// or ftp://', () => {
      expect(wrapper.vm.rules.validUrl('http://www.abc.de')).toBe(true)
      expect(wrapper.vm.rules.validUrl('https://www.abc.de')).toBe(true)
      expect(wrapper.vm.rules.validUrl('ftp://abc.de')).toBe(true)
    })
  })
})
