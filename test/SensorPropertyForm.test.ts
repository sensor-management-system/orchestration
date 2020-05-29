import Vue from 'vue'
import Vuetify from 'vuetify'

import { mount, createLocalVue } from '@vue/test-utils'
import { WrapperArray } from '@vue/test-utils/types'

// @ts-ignore
import SensorPropertyForm from '@/components/SensorPropertyForm.vue'
import { SensorProperty } from '@/models/SensorProperty'

// see https://github.com/vuejs/vue-test-utils/issues/960
function withWrapperArray (wrapperArray: WrapperArray<Vue>): Record<string, Function> {
  return {
    childSelectorHasText: (
      selector: string,
      str: string
    ): WrapperArray<Vue> => wrapperArray
      .filter(i => i.find(selector).text().match(str)),

    hasText: (str: string): WrapperArray<Vue> => wrapperArray
      .filter(i => i.text().match(str))
  }
}

Vue.use(Vuetify)

describe('SensorPropertyForm', () => {
  let wrapper: any

  /*
   * setup
   */

  beforeEach(() => {
    const localVue = createLocalVue()
    const vuetify = new Vuetify()

    wrapper = mount(SensorPropertyForm, {
      localVue,
      vuetify,
      propsData: {
        value: SensorProperty.createFromObject({
          compartment: 'test',
          label: 'test',
          samplingMedia: 'water',
          unit: 'mm',
          variable: 'foo.bar',
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
