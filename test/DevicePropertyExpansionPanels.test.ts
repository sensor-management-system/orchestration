import Vue from 'vue'
import Vuetify from 'vuetify'

import { mount, createLocalVue } from '@vue/test-utils'

// @ts-ignore
import DevicePropertyExpansionPanels from '@/components/DevicePropertyExpansionPanels.vue'
import { DeviceProperty } from '@/models/DeviceProperty'

import Compartment from '~/models/Compartment'
import SamplingMedia from '~/models/SamplingMedia'
import Property from '~/models/Property'
import Unit from '~/models/Unit'

Vue.use(Vuetify)

describe('DevicePropertyExpansionPanels', () => {
  let wrapper: any

  /*
   * setup
   */

  beforeEach(() => {
    const localVue = createLocalVue()
    const vuetify = new Vuetify()
    // disable "[Vuetify] Unable to locate target [data-app]" warnings:
    document.body.setAttribute('data-app', 'true')

    wrapper = mount(DevicePropertyExpansionPanels, {
      localVue,
      vuetify,
      propsData: {
        value: [
          DeviceProperty.createFromObject({
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
        ] as DeviceProperty[],
        compartments: [
          Compartment.createWithData('1', 'bar', 'http://foo/compartment/1'),
          Compartment.createWithData('2', 'compartment2', 'http://foo/compartment/2')
        ],
        samplingMedias: [
          SamplingMedia.createWithData('1', 'water', 'http://foo/samplingMedia/1'),
          SamplingMedia.createWithData('2', 'media2', 'http://foo/samplingMedia/2')
        ],
        properties: [
          Property.createWithData('1', 'foo.bar', 'http://foo/property/1'),
          Property.createWithData('2', 'property2', 'http://foo/property/2')
        ],
        units: [
          Unit.createWithData('1', 'mm', 'http://foo/unit/1'),
          Unit.createWithData('2', 's', 'http://foo/unit/2')
        ]
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
   * adding
   */

  it('should trigger an input event when add button is clicked', async () => {
    await wrapper.get('button[data-role="add-property"]').trigger('click')
    expect(wrapper.emitted('input')).toBeTruthy()
  })

  it('should trigger an input event with a device property array length increased by 1 when the add button is clicked', async () => {
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

  it('should trigger an input event with a device property array length decreased by 1 when the delete menu item is clicked', async () => {
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

  it('should trigger an input event with a device property array length increased by 1 when the copy menu item is clicked', async () => {
    await wrapper.get('[data-role="property-menu"]').trigger('click')
    await wrapper.get('[data-role="copy-property"]').trigger('click')
    expect(wrapper.emitted('input')[0][0]).toHaveLength(2)
  })
})
