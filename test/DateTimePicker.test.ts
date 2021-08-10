/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020
 * - Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
 * - Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
 * - Tobias Kuhnert (UFZ, tobias.kuhnert@ufz.de)
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
import { DateTime } from 'luxon'

import { mount } from '@vue/test-utils'

// @ts-ignore
import DateTimePicker from '@/components/DateTimePicker'

Vue.use(Vuetify)

const factory = (options = {}) => {
  const vuetify = new Vuetify()
  return mount(DateTimePicker, {
    vuetify,
    ...options
  })
}

describe('DatetimePicker.vue', () => {
  let wrapper: any

  it('renders a vue instance', () => {
    wrapper = factory({
      propsData: {
        label: 'Testlabel',
        value: null
      }
    })

    expect(wrapper).toBeTruthy()
  })

  it('textfield displays the correct label', () => {
    wrapper = factory({
      propsData: {
        label: 'Testlabel',
        value: null
      }
    })

    const textfieldLabel = wrapper.find('.v-text-field__slot > label')

    expect(textfieldLabel.text()).toBe('Testlabel')
  })

  it('textfield displays nothing when value is null', () => {
    wrapper = factory({
      propsData: {
        label: 'Testlabel',
        value: null
      }
    })
    expect(wrapper.find('input[type="text"]').element.value).toBe('')
  })

  it('textfield displays the correct date and time passed as DateTime-Object', () => {
    const testDateTime = DateTime.fromISO('2021-01-20T20:12:00.000Z', { zone: 'UTC' })

    wrapper = factory({
      propsData: {
        label: 'Display date and time',
        value: testDateTime
      }
    })

    expect(wrapper.find('input[type="text"]').element.value).toBe('2021-01-20 20:12')
  })

  it('textfield displays the correct date passed as DateTime-Object', () => {
    const testDateTime = DateTime.fromISO('2021-01-20T20:12:00.000Z', { zone: 'UTC' })

    wrapper = factory({
      propsData: {
        label: 'Display date and time',
        value: testDateTime,
        'use-date': true
      }
    })

    expect(wrapper.find('input[type="text"]').element.value).toBe('2021-01-20')
  })

  it('textfield displays the correct time passed as DateTime-Object', () => {
    const testDateTime = DateTime.fromISO('2021-01-20T20:12:00.000Z', { zone: 'UTC' })

    wrapper = factory({
      propsData: {
        label: 'Display date and time',
        value: testDateTime,
        'use-time': true
      }
    })

    expect(wrapper.find('input[type="text"]').element.value).toBe('20:12')
  })

  it('displays correct error message for datetime format, when textfield contains value with wrong format', () => {
    wrapper = factory({
      propsData: {
        label: 'Testlabel',
        value: null
      }
    })
    const validationMessage = wrapper.vm.textInputRules[0]('2021-05-01')

    expect(validationMessage).toBe('Please use the format: yyyy-MM-dd HH:mm')
  })

  it('displays correct error message for date format, when textfield contains value with wrong format', () => {
    wrapper = factory({
      propsData: {
        label: 'Testlabel',
        value: null,
        'use-date': true
      }
    })

    const validationMessage = wrapper.vm.textInputRules[0]('2021-05-011')

    expect(validationMessage).toBe('Please use the format: yyyy-MM-dd')
  })

  it('displays correct error message for time format, when textfield contains value with wrong format', () => {
    wrapper = factory({
      propsData: {
        label: 'Testlabel',
        value: null,
        'use-time': true
      }
    })
    const validationMessage = wrapper.vm.textInputRules[0]('2021-05-01')

    expect(validationMessage).toBe('Please use the format: HH:mm')
  })

  it('uses datetime when use-date and use-datime are both WRONGLY passed as props', () => {
    wrapper = factory({
      propsData: {
        label: 'Testlabel',
        value: null,
        'use-time': true,
        'use-date': true
      }
    })

    expect(wrapper.vm.isDatetimeUsed).toBeTruthy()
    expect(wrapper.vm.usesDate).toBeFalsy()
    expect(wrapper.vm.usesTime).toBeFalsy()
  })

  it('emits correct dateTime object when textInput is updated', async () => {
    const expectedDateTime = DateTime.fromFormat('2020-05-01 12:12', 'yyyy-MM-dd HH:mm', { zone: 'UTC' })

    wrapper = factory({
      propsData: {
        label: 'Testlabel',
        value: null
      }
    })

    wrapper.vm.updateByTextfield('2020-05-01 12:12')
    expect(wrapper.emitted('input')).toBeTruthy()
    await wrapper.vm.$nextTick()
    expect(wrapper.emitted().input[0]).toEqual([expectedDateTime])
  })

  it('emits correct dateTime object when updated by date picker when value was null', async () => {
    const expectedDate = '2020-05-01'
    const expectedTime = DateTime.now().setZone('UTC').toFormat('HH:mm')

    wrapper = factory({
      propsData: {
        label: 'Testlabel',
        value: null
      }
    })

    wrapper.vm.initDateAndTimePickerValues()

    wrapper.vm.setDatePickerValue('2020-05-01')
    wrapper.vm.applyPickerValue()
    expect(wrapper.emitted('input')).toBeTruthy()
    await wrapper.vm.$nextTick()

    const emittedObject = wrapper.emitted().input[0][0]
    const actualDate = emittedObject.toFormat('yyyy-MM-dd')
    const actualTime = emittedObject.toFormat('HH:mm')

    expect(actualDate).toEqual(expectedDate)
    expect(actualTime).toEqual(expectedTime)
  })

  it('emits correct dateTime object when updated by date picker when value was passed', async () => {
    const testDateTime = DateTime.fromISO('2021-01-20T20:12:00.000Z', { zone: 'UTC' })
    const expectedDateTime = DateTime.fromFormat('2020-05-01 20:12', 'yyyy-MM-dd HH:mm', { zone: 'UTC' })

    wrapper = factory({
      propsData: {
        label: 'Testlabel',
        value: testDateTime
      }
    })

    wrapper.vm.initDateAndTimePickerValues()

    wrapper.vm.setDatePickerValue('2020-05-01')
    wrapper.vm.applyPickerValue()
    expect(wrapper.emitted('input')).toBeTruthy()
    await wrapper.vm.$nextTick()
    expect(wrapper.emitted().input[0]).toEqual([expectedDateTime])
  })

  it('emits null when updated by date picker and the date is not valid', async () => {
    wrapper = factory({
      propsData: {
        label: 'Testlabel',
        value: null
      }
    })

    wrapper.vm.initDateAndTimePickerValues()

    wrapper.vm.setDatePickerValue('2020-05-88')
    wrapper.vm.applyPickerValue()
    expect(wrapper.emitted('input')).toBeTruthy()
    await wrapper.vm.$nextTick()
    expect(wrapper.emitted().input[0]).toEqual([null])
  })

  it('emits correct dateTime object when updated by time picker when value was null', async () => {
    const expectedTime = '12:13'

    wrapper = factory({
      propsData: {
        label: 'Testlabel',
        value: null
      }
    })

    wrapper.vm.initDateAndTimePickerValues()

    wrapper.vm.setTimePickerValue(expectedTime)
    wrapper.vm.applyPickerValue()
    expect(wrapper.emitted('input')).toBeTruthy()
    await wrapper.vm.$nextTick()

    const actual = wrapper.emitted().input[0][0]
    expect(actual.hour + ':' + actual.minute).toBe(expectedTime)
  })

  it('emits correct dateTime object when updated by time picker when value was passed', async () => {
    const testDateTime = DateTime.fromISO('2021-01-20T20:12:00.000Z', { zone: 'UTC' })
    const expectedTime = '12:13'

    wrapper = factory({
      propsData: {
        label: 'Testlabel',
        value: testDateTime
      }
    })

    wrapper.vm.initDateAndTimePickerValues()

    wrapper.vm.setTimePickerValue(expectedTime)
    wrapper.vm.applyPickerValue()
    expect(wrapper.emitted('input')).toBeTruthy()
    await wrapper.vm.$nextTick()

    const actual = wrapper.emitted().input[0][0]
    expect(actual.hour + ':' + actual.minute).toBe(expectedTime)
  })

  it('emits null when updated by time picker and the time is not valid', async () => {
    const invalidTime = '12:88'

    wrapper = factory({
      propsData: {
        label: 'Testlabel',
        value: null
      }
    })

    wrapper.vm.initDateAndTimePickerValues()

    wrapper.vm.setTimePickerValue(invalidTime)
    wrapper.vm.applyPickerValue()

    expect(wrapper.emitted('input')).toBeTruthy()

    await wrapper.vm.$nextTick()
    expect(wrapper.emitted().input[0]).toEqual([null])
  })

  it('setTextInputByValue sets textInput to empty string when null is passed', () => {
    wrapper = factory({
      propsData: {
        label: 'Testlabel',
        value: null
      }
    })

    wrapper.vm.setTextInputByValue(null)
    expect(wrapper.vm.textInput).toBe('')
  })

  it('sets the correct values when picker is closed', () => {
    wrapper = factory({
      propsData: {
        label: 'Testlabel',
        value: null
      }
    })

    wrapper.vm.activeTab = 1
    wrapper.vm.display = true

    wrapper.vm.closePicker()

    expect(wrapper.vm.activeTab).toBe(0)
    expect(wrapper.vm.dialog).toBe(false)
  })

  it('includes the provided rules', () => {
    const testRuleNameRequired = (v:any) => !!v || 'Name is required'

    wrapper = factory({
      propsData: {
        label: 'Testlabel',
        value: null,
        rules: [
          testRuleNameRequired
        ]
      }
    })

    expect(wrapper.vm.textInputRules).toContain(testRuleNameRequired)
  })

  it('picker initializes correct when value was null', () => {
    // Fix to avoid following warning--------------------------
    // console.warn
    //   [Vuetify] Unable to locate target [data-app]
    const app = document.createElement('div')
    app.setAttribute('data-app', 'true')
    document.body.append(app)
    // --------------------------------------------------------

    const expectedDate = new Date().toISOString().substr(0, 10)
    const expectedTime = DateTime.now().setZone('UTC').toFormat('HH:mm')
    wrapper = factory({
      propsData: {
        label: 'Testlabel',
        value: null
      }
    })

    wrapper.vm.initPicker()

    expect(wrapper.vm.dialog).toBeTruthy()
    expect(wrapper.vm.datePickerValue).toBe(expectedDate)
    expect(wrapper.vm.timePickerValue).toBe(expectedTime)
  })

  it('picker initializes correct when value was passed', () => {
    // Fix to avoid following warning--------------------------
    // console.warn
    //   [Vuetify] Unable to locate target [data-app]
    const app = document.createElement('div')
    app.setAttribute('data-app', 'true')
    document.body.append(app)
    // --------------------------------------------------------

    const testDateTime = DateTime.fromISO('2021-01-20T20:12:00.000Z', { zone: 'UTC' })

    const expectedDate = '2021-01-20'
    const expectedTime = '20:12'
    wrapper = factory({
      propsData: {
        label: 'Testlabel',
        value: testDateTime
      }
    })

    wrapper.vm.initPicker()

    expect(wrapper.vm.dialog).toBeTruthy()
    expect(wrapper.vm.datePickerValue).toBe(expectedDate)
    expect(wrapper.vm.timePickerValue).toBe(expectedTime)
  })

  it('resetPicker sets the correct values', () => {
    // Fix to avoid following warning--------------------------
    // console.warn
    //   [Vuetify] Unable to locate target [data-app]
    const app = document.createElement('div')
    app.setAttribute('data-app', 'true')
    document.body.append(app)
    // --------------------------------------------------------

    wrapper = factory({
      propsData: {
        label: 'Testlabel',
        value: null
      }
    })

    wrapper.vm.dialog = true
    wrapper.vm.datePickerValue = '2021-05-05'
    wrapper.vm.timePickerValue = '10:10'
    wrapper.vm.activeTab = 1

    expect(wrapper.vm.dialog).toBeTruthy()
    expect(wrapper.vm.datePickerValue).toBe('2021-05-05')
    expect(wrapper.vm.timePickerValue).toBe('10:10')
    expect(wrapper.vm.activeTab).toBe(1)

    wrapper.vm.resetPicker()

    expect(wrapper.vm.dialog).toBeFalsy()
    expect(wrapper.vm.datePickerValue).toBe('')
    expect(wrapper.vm.timePickerValue).toBe('')
    expect(wrapper.vm.activeTab).toBe(0)
  })

  it('emits correct dateTime object when using use-date and updated by date picker when value was null', async () => {
    const expectedDateTime = DateTime.fromFormat('2020-05-01 00:00', 'yyyy-MM-dd HH:mm', { zone: 'UTC' })

    wrapper = factory({
      propsData: {
        label: 'Testlabel',
        value: null,
        'use-date': true
      }
    })

    wrapper.vm.initDateAndTimePickerValues()

    wrapper.vm.setDatePickerValue('2020-05-01')
    wrapper.vm.applyPickerValue()
    expect(wrapper.emitted('input')).toBeTruthy()
    await wrapper.vm.$nextTick()
    expect(wrapper.emitted().input[0]).toEqual([expectedDateTime])
  })

  it('emits correct dateTime object when using use-time and updated by time picker when value was null', async () => {
    const expectedTime = '12:13'

    wrapper = factory({
      propsData: {
        label: 'Testlabel',
        value: null,
        'use-time': true
      }
    })

    wrapper.vm.initDateAndTimePickerValues()

    wrapper.vm.setTimePickerValue(expectedTime)
    wrapper.vm.applyPickerValue()
    expect(wrapper.emitted('input')).toBeTruthy()
    await wrapper.vm.$nextTick()

    const actual = wrapper.emitted().input[0][0]
    expect(actual.hour + ':' + actual.minute).toBe(expectedTime)
  })
})
