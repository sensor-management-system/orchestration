/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020-2022
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
