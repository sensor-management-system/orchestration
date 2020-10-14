import Vue from 'vue'
import Vuetify from 'vuetify'

import { mount, createLocalVue } from '@vue/test-utils'

// @ts-ignore
import DevicePropertyForm from '../components/DevicePropertyForm.vue'

import { DeviceProperty } from '~/models/DeviceProperty'
import { Compartment } from '~/models/Compartment'
import { SamplingMedia } from '~/models/SamplingMedia'
import { Property } from '~/models/Property'
import { Unit } from '~/models/Unit'

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
          id: null,
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
        }),
        compartments: [
          Compartment.createWithData('1', 'bar', 'http://foo/compartment/1'),
          Compartment.createWithData('2', 'foo', 'http://foo/compartment/2')
        ] as Compartment[],
        samplingMedias: [
          SamplingMedia.createWithData('1', 'water', 'http://foo/samplingMedia/1'),
          SamplingMedia.createWithData('2', 'media2', 'http://foo/samplingMedia/2')
        ] as SamplingMedia[],
        properties: [
          Property.createWithData('1', 'foo.bar', 'http://foo/property/1'),
          Property.createWithData('2', 'property2', 'http://foo/property/2')
        ] as Property[],
        units: [
          Unit.createWithData('1', 'mm', 'http://foo/unit/1'),
          Unit.createWithData('2', 's', 'http://foo/unit/2')
        ] as Unit[]
      }
    })
  })

  /*
   * initial state
   */

  it('should be a Vue instance', () => {
    expect(wrapper.vm).toBeTruthy()
  })

  it('should trigger an input event on change', async () => {
    const inputField = wrapper.get('input[type="text"]')
    inputField.setValue('foo')
    // and because of the v-combobox, we need to trigger the
    // update as well (so send enter)
    inputField.trigger('keydown.enter')
    // and we have to wait until the action is done
    // and btw, we need to make the lambda function for the
    // it call async
    await wrapper.vm.$nextTick()
    expect(wrapper.emitted('input')).toBeTruthy()
  })
})
