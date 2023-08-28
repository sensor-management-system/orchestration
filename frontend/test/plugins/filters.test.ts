/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020 - 2023
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

import '@/plugins/filters'

Vue.use(Vuetify)

describe('orDefault', () => {
  it('should return the string if the string is not empty', () => {
    const localVue = createLocalVue()
    /* eslint-disable */
    const customComponent = Vue.component('CustomComponent', {
      data () {
        return {
          testValue: 'no such empty'
        }
      },
      template: '<div>{{ testValue | orDefault }}</div>'
    })
    /* eslint-enable */

    const wrapper = mount(customComponent, {
      localVue
    })
    expect(wrapper.html()).toBe('<div>no such empty</div>')
  })
  it('should return the default for an empty string', () => {
    const localVue = createLocalVue()
    /* eslint-disable */
    const customComponent = Vue.component('CustomComponent', {
      data () {
        return {
          testValue: ''
        }
      },
      template: "<div>{{ testValue | orDefault('such empty') }}</div>"
    })
    /* eslint-enable */

    const wrapper = mount(customComponent, {
      localVue
    })
    expect(wrapper.html()).toBe('<div>such empty</div>')
  })
  it('should return the numeric value for numerics', () => {
    const localVue = createLocalVue()
    /* eslint-disable */
    const customComponent = Vue.component('CustomComponent', {
      data () {
        return {
          testValue: 0
        }
      },
      template: '<div>{{ testValue | orDefault }}</div>'
    })
    /* eslint-enable */

    const wrapper = mount(customComponent, {
      localVue
    })
    expect(wrapper.html()).toBe('<div>0</div>')
  })
  it('should return the default for NaN', () => {
    const localVue = createLocalVue()
    /* eslint-disable */
    const customComponent = Vue.component('CustomComponent', {
      data () {
        return {
          testValue: NaN
        }
      },
      template: "<div>{{ testValue | orDefault('such empty') }}</div>"
    })
    /* eslint-enable */

    const wrapper = mount(customComponent, {
      localVue
    })
    expect(wrapper.html()).toBe('<div>such empty</div>')
  })
  it('should return the default for undefined values', () => {
    const localVue = createLocalVue()
    /* eslint-disable */
    const customComponent = Vue.component('CustomComponent', {
      data () {
        return {
          testValue: undefined
        }
      },
      template: "<div>{{ testValue | orDefault('such empty') }}</div>"
    })
    /* eslint-enable */

    const wrapper = mount(customComponent, {
      localVue
    })
    expect(wrapper.html()).toBe('<div>such empty</div>')
  })
  it('should return the default for null values', () => {
    const localVue = createLocalVue()
    /* eslint-disable */
    const customComponent = Vue.component('CustomComponent', {
      data () {
        return {
          testValue: null
        }
      },
      template: "<div>{{ testValue | orDefault('such empty') }}</div>"
    })
    /* eslint-enable */

    const wrapper = mount(customComponent, {
      localVue
    })
    expect(wrapper.html()).toBe('<div>such empty</div>')
  })
})
