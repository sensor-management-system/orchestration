import Vue from 'vue'
import Vuetify from 'vuetify'

import { mount, createLocalVue } from '@vue/test-utils'

// @ts-ignore
import DevicePropertyForm from '../components/DevicePropertyForm.vue'
import { DeviceProperty } from '~/models/DeviceProperty'

Vue.use(Vuetify)

describe('DevicePropertyForm', () => {
  let wrapper: any

  /*
   * setup
   */

  beforeEach(() => {
    const localVue = createLocalVue()
    const vuetify = new Vuetify()

    wrapper = mount(DevicePropertyForm, {
      localVue,
      vuetify,
      propsData: {
        value: DeviceProperty.createFromObject({
          label: 'test',
          compartmentUri: 'http://foo/compartment/1',
          compartmentName: 'bar',
          unitUri: 'http://foo/unit/1',
          unitName: 'mm',
          samplingMediaUri: 'http://foo/samplingMedia/1',
          samplingMediaName: 'water',
          propertyUri: 'http://foo/property/1',
          propertyName: 'foo.bar',
          measuringRange: {
            min: 10,
            max: 1000
          },
          accuracy: 0.1,
          failureValue: 0.01
        })
      }
    })
  })

  /*
   * initial state
   */

  it('should be a Vue instance', () => {
    expect(wrapper.isVueInstance()).toBeTruthy()
  })

  it('should trigger an input event on change', () => {
    wrapper.get('input[type="text"]').setValue('foo')
    expect(wrapper.emitted('input')).toBeTruthy()
  })
})
