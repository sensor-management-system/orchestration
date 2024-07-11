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
