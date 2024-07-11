/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */

import Vue from 'vue'
import Vuex from 'vuex'
import Vuetify from 'vuetify'

import { createLocalVue, mount } from '@vue/test-utils'

import { DateTime } from 'luxon'
// @ts-ignore
import DynamicLocationActionDateForm from '@/components/configurations/dynamicLocation/DynamicLocationActionDateForm'
import { DynamicLocationAction } from '@/models/DynamicLocationAction'
import { Configuration } from '@/models/Configuration'
import { Visibility } from '@/models/Visibility'
import { Device } from '@/models/Device'
import { DeviceProperty } from '@/models/DeviceProperty'

type PresetData = {
  configuration?: Configuration
}

Vue.use(Vuetify)

const testConfig1 = Configuration.createFromObject({
  startDate: DateTime.fromISO('2020-08-04T00:00:00.000Z', { zone: 'UTC' }),
  endDate: DateTime.fromISO('2020-08-12T23:59:00.000Z', { zone: 'UTC' }),
  label: 'HYDREX_2020_Inland_Elbe',
  id: '1',
  persistentIdentifier: '',
  description: '',
  project: '',
  campaign: '',
  status: '',
  archived: false,
  contacts: [],
  createdAt: null,
  updatedAt: null,
  updateDescription: '',
  createdBy: null,
  updatedBy: null,
  createdByUserId: null,
  visibility: Visibility.Internal,
  siteId: '',
  platformMountActions: [],
  deviceMountActions: [],
  parameters: [],
  images: [],
  permissionGroup: null,
  keywords: []
})

const factory = (options = {}, presetData: PresetData = {}) => {
  const localVue = createLocalVue()
  localVue.use(Vuex)

  const vuetify = new Vuetify()

  const device1 = new Device()
  device1.id = '1'
  device1.shortName = 'GPS'
  const prop1 = new DeviceProperty()
  prop1.id = '1'
  prop1.propertyName = 'GPS position, latitude'
  device1.properties = [prop1]

  const configurations = {
    namespaced: true,
    state: {
      configuration: presetData.configuration
    },
    getters: {
      locationActionTimepointsExceptPassedIdAndType: () => () => [
        {
          timepoint: DateTime.fromISO('2020-08-12T23:59:00.000Z', { zone: 'UTC' }),
          type: 'configuration_static_location_end',
          id: '2',
          text: '2020-08-12 23:59 - Static location end - End'
        },
        {
          timepoint: DateTime.fromISO('2020-08-12T00:00:00.000Z', { zone: 'UTC' }),
          type: 'configuration_static_location_begin',
          id: '2',
          text: '2020-08-12 00:00 - Static location begin - End'
        },
        {
          timepoint: DateTime.fromISO('2020-08-04T23:59:00.000Z', { zone: 'UTC' }),
          type: 'configuration_static_location_end',
          id: '1',
          text: '2020-08-04 23:59 - Static location end - Start'
        },
        {
          timepoint: DateTime.fromISO('2020-08-04T00:00:00.000Z', { zone: 'UTC' }),
          type: 'configuration_static_location_begin',
          id: '1',
          text: '2020-08-04 00:00 - Static location begin - Start'
        }
      ],
      earliestEndDateOfRelatedDeviceOfDynamicAction: () => () => null,
      activeDevicesWithPropertiesForDate: () => () => [
        device1
      ]
    },
    actions: {},
    mutations: {}

  }
  const store = new Vuex.Store({ modules: { configurations } })
  return mount(DynamicLocationActionDateForm, {
    localVue,
    vuetify,
    store,
    ...options
  })
}

describe('DynamicLocationActionDateForm', () => {
  let wrapper: any

  it('renders a vue instance', () => {
    wrapper = factory({
      propsData: {
        value: new DynamicLocationAction()
      }
    })

    expect(wrapper).toBeTruthy()
  })

  it('shows validation error, if the begin date of the dynamic location action is not in the range of the configuration dates', async () => {
    const action = new DynamicLocationAction()
    const expectedDate = DateTime.fromISO('2023-06-14T09:00:00.000Z', { zone: 'UTC' })
    action.beginDate = expectedDate

    wrapper = factory(
      {
        propsData: {
          value: action
        }
      },
      {
        configuration: testConfig1
      }
    )
    // make sure date is correctly set
    expect(wrapper.vm.value.beginDate).toBe(expectedDate)

    const datePickers = wrapper.findAllComponents({ name: 'DateTimePicker' })

    expect(datePickers).toHaveLength(2)

    expect(wrapper.vm.validateForm()).toBe(false)

    await wrapper.vm.$nextTick()

    expect(datePickers.at(0).find('.v-messages__message').text()).toBe('Date must be in the range of 2020-08-04 00:00 -- 2020-08-12 23:59 (dates of configuration)')
    expect(datePickers.at(1).find('.v-messages__message').exists()).toBe(false)
  })

  it('shows validation error, if the start and end date of the dynamic location action is not in the range of the configuration dates', async () => {
    const action = new DynamicLocationAction()
    const expectedBeginDate = DateTime.fromISO('2023-06-14T09:00:00.000Z', { zone: 'UTC' })
    const expectedEndDate = DateTime.fromISO('2023-06-15T09:00:00.000Z', { zone: 'UTC' })
    action.beginDate = expectedBeginDate
    action.endDate = expectedEndDate

    wrapper = factory(
      {
        propsData: {
          value: action
        }
      },
      {
        configuration: testConfig1
      }
    )
    // make sure date is correctly set
    expect(wrapper.vm.value.beginDate).toBe(expectedBeginDate)
    expect(wrapper.vm.value.endDate).toBe(expectedEndDate)

    const datePickers = wrapper.findAllComponents({ name: 'DateTimePicker' })

    expect(datePickers).toHaveLength(2)

    expect(wrapper.vm.validateForm()).toBe(false)

    await wrapper.vm.$nextTick()

    expect(datePickers.at(0).find('.v-messages__message').text()).toBe('Date must be in the range of 2020-08-04 00:00 -- 2020-08-12 23:59 (dates of configuration)')
    expect(datePickers.at(1).find('.v-messages__message').text()).toBe('Date must be in the range of 2020-08-04 00:00 -- 2020-08-12 23:59 (dates of configuration)')
  })

  it('shows validation error, when begin and end date conflict with existing actions', async () => {
    const action = new DynamicLocationAction()
    const expectedBeginDate = DateTime.fromISO('2020-08-04T00:00:00.000Z', { zone: 'UTC' })
    const expectedEndDate = DateTime.fromISO('2020-08-12T23:59:00.000Z', { zone: 'UTC' })
    action.beginDate = expectedBeginDate
    action.endDate = expectedEndDate

    wrapper = factory(
      {
        propsData: {
          value: action
        }
      },
      {
        configuration: testConfig1
      }
    )
    // make sure date is correctly set
    expect(wrapper.vm.value.beginDate).toBe(expectedBeginDate)
    expect(wrapper.vm.value.endDate).toBe(expectedEndDate)

    const datePickers = wrapper.findAllComponents({ name: 'DateTimePicker' })

    expect(datePickers).toHaveLength(2)

    expect(wrapper.vm.validateForm()).toBe(false)

    await wrapper.vm.$nextTick()

    expect(datePickers.at(0).find('.v-messages__message').text()).toBe('Must be before 2020-08-04 00:00 or after 2020-08-04 23:59 (of existing location action)')
    expect(datePickers.at(1).find('.v-messages__message').text()).toBe('End date must be before 2020-08-04 23:59 (next action)')
  })

  it('should be valid, if start and end are in range of configuration and do not conflict with existing actions', () => {
    const action = new DynamicLocationAction()
    const expectedBeginDate = DateTime.fromISO('2020-08-05T00:00:00.000Z', { zone: 'UTC' })
    const expectedEndDate = DateTime.fromISO('2020-08-11T23:59:00.000Z', { zone: 'UTC' })
    action.beginDate = expectedBeginDate
    action.endDate = expectedEndDate

    wrapper = factory(
      {
        propsData: {
          value: action
        }
      },
      {
        configuration: testConfig1
      }
    )
    // make sure date is correctly set
    expect(wrapper.vm.value.beginDate).toBe(expectedBeginDate)
    expect(wrapper.vm.value.endDate).toBe(expectedEndDate)

    expect(wrapper.vm.validateForm()).toBe(true)
  })
})
