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
import Vuex from 'vuex'
import Vuetify from 'vuetify'

import { mount, createLocalVue } from '@vue/test-utils'

// @ts-ignore
import DevicePropertyForm from '@/components/DevicePropertyForm.vue'

import { DeviceProperty } from '@/models/DeviceProperty'
import { Compartment } from '@/models/Compartment'
import { SamplingMedia } from '@/models/SamplingMedia'
import { Property } from '@/models/Property'
import { Unit } from '@/models/Unit'
import { MeasuredQuantityUnit } from '@/models/MeasuredQuantityUnit'
import { AggregationType } from '@/models/AggregationType'

Vue.use(Vuetify)

describe('DevicePropertyForm', () => {
  let wrapper: any

  /*
   * setup
   */

  beforeEach(() => {
    const localVue = createLocalVue()
    localVue.use(Vuex)
    const vuetify = new Vuetify()

    const vocabulary = {
      namespaced: true,
      state: {
        // The dialogs to submit new entries use the vocabulary state.
        globalProvenances: []
      },
      mutations: {
      },
      actions: {
        loadGlobalProvenances: () => {}
      }
    }
    const store = new Vuex.Store({
      modules: { vocabulary }
    })

    wrapper = mount(DevicePropertyForm, {
      localVue,
      vuetify,
      store,
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
          accuracyUnitUri: 'http://foo/unit/2',
          accuracyUnitName: 'cm',
          failureValue: 0.01,
          resolution: 0.001,
          resolutionUnitUri: 'http://foo/unit/1',
          resolutionUnitName: 'mm',
          aggregationTypeUri: 'http://foo/aggregationtypes/1',
          aggregationTypeName: 'Average',
          description: 'test description'
        }),
        compartments: [
          Compartment.createWithData('1', 'bar', 'http://foo/compartment/1', 'foo'),
          Compartment.createWithData('2', 'foo', 'http://foo/compartment/2', 'bar')
        ] as Compartment[],
        samplingMedias: [
          SamplingMedia.createWithData('1', 'water', 'http://foo/samplingMedia/1', 'foo', '5'),
          SamplingMedia.createWithData('2', 'media2', 'http://foo/samplingMedia/2', 'bar', '2')
        ] as SamplingMedia[],
        properties: [
          Property.createWithData('1', 'foo.bar', 'http://foo/property/1', 'foo', '8'),
          Property.createWithData('2', 'property2', 'http://foo/property/2', 'bar', '3')
        ] as Property[],
        units: [
          Unit.createWithData('1', 'mm', 'http://foo/unit/1', 'foo'),
          Unit.createWithData('2', 's', 'http://foo/unit/2', 'bar')
        ] as Unit[],
        measuredQuantityUnits: [
          MeasuredQuantityUnit.createWithData('1', 'mm', 'http://foo/measuredquantityunits/1', 'foo', '0.01', '10', '1', '1'),
          MeasuredQuantityUnit.createWithData('2', 's', 'http://foo/measuredquantityunits/2', 'bar', '0.001', '60', '2', '1')
        ] as MeasuredQuantityUnit[],
        aggregationTypes: [
          AggregationType.createFromObject({
            uri: 'https://foo/aggregationtypes/1',
            name: 'Average',
            id: '1',
            provenance: '',
            provenanceUri: '',
            category: '',
            definition: '',
            globalProvenanceId: '1',
            note: ''
          }),
          AggregationType.createFromObject({
            uri: 'https://foo/aggregationtypes/2',
            name: 'Mode',
            id: '2',
            provenance: '',
            provenanceUri: '',
            category: '',
            definition: '',
            globalProvenanceId: '1',
            note: ''
          })
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

  it('checks if an URI ends with an id', () => {
    const uri1 = '/foo/bar/42/'
    const uri2 = '/foo/bar/23'

    expect(wrapper.vm.checkUriEndsWithId(uri1, '42')).toBeTruthy()
    expect(wrapper.vm.checkUriEndsWithId(uri1, '43')).toBeFalsy()
    expect(wrapper.vm.checkUriEndsWithId(uri2, '23')).toBeTruthy()
  })
})
