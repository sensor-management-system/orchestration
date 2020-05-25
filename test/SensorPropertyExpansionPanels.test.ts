import Vue from 'vue'
import Vuetify from 'vuetify'

import { mount, createLocalVue } from '@vue/test-utils'
import { WrapperArray } from '@vue/test-utils/types'

// @ts-ignore
import SensorPropertyExpansionPanels from '@/components/SensorPropertyExpansionPanels.vue'
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

describe('SensorPropertyExpansionPanels', () => {
  let wrapper: any

  /*
   * setup
   */

  beforeEach(() => {
    const localVue = createLocalVue()
    const vuetify = new Vuetify()
    // disable "[Vuetify] Unable to locate target [data-app]" warnings:
    document.body.setAttribute('data-app', 'true')

    wrapper = mount(SensorPropertyExpansionPanels, {
      localVue,
      vuetify,
      propsData: {
        value: [
          SensorProperty.createFromObject({
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
        ] as SensorProperty[]
      }
    })
  })

  /*
   * initial state
   */

  it('should be a Vue instance', () => {
    expect(wrapper.isVueInstance()).toBeTruthy()
  })

  /*
   * adding
   */

  it('should trigger an input event when add button is clicked', async () => {
    await wrapper.get('button[data-role="add-property"]').trigger('click')
    expect(wrapper.emitted('input')).toBeTruthy()
  })

  it('should trigger an input event with a sensor property array length increased by 1 when the add button is clicked', async () => {
    await wrapper.get('[data-role="add-property"]').trigger('click')
    expect(wrapper.emitted('input')[0][0]).toHaveLength(2)
  })

  /*
   * removing
   */

  it('should trigger an input event when delete menu item is clicked', async () => {
    await wrapper.get('[data-role="property-menu"]').trigger('click')
    await wrapper.get('[data-role="delete-property"]').trigger('click')
    expect(wrapper.emitted('input')).toBeTruthy()
  })

  it('should trigger an input event with a sensor property array length decreased by 1 when the delete menu item is clicked', async () => {
    await wrapper.get('[data-role="property-menu"]').trigger('click')
    await wrapper.get('[data-role="delete-property"]').trigger('click')
    expect(wrapper.emitted('input')[0][0]).toHaveLength(0)
  })

  /*
   * copying
   */

  it('should trigger an input event when copy menu item is clicked', async () => {
    await wrapper.get('[data-role="property-menu"]').trigger('click')
    await wrapper.get('[data-role="copy-property"]').trigger('click')
    expect(wrapper.emitted('input')).toBeTruthy()
  })

  it('should trigger an input event with a sensor property array length increased by 1 when the copy menu item is clicked', async () => {
    await wrapper.get('[data-role="property-menu"]').trigger('click')
    await wrapper.get('[data-role="copy-property"]').trigger('click')
    expect(wrapper.emitted('input')[0][0]).toHaveLength(2)
  })
})
