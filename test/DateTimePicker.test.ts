import Vue from 'vue'

import { mount } from '@vue/test-utils'

// @ts-ignore
import DateTimePicker from '@/components/DateTimePicker'
import { DateTime } from 'luxon'
import Vuetify from 'vuetify'

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

  it('displays correct error message for datetime format, when textfield contains value with wrong format', async () => {
    wrapper = factory({
      propsData: {
        label: 'Testlabel',
        value: null
      }
    })

    const textFieldInput = wrapper.find('input[type="text"]')

    await textFieldInput.setValue('2021-05-01')

    expect(wrapper.find('input[type="text"]').element.value).toBe('2021-05-01')

    const validationMessage = wrapper.find('div.v-messages__message')

    expect(validationMessage.text()).toBe('Please use the format: yyyy-MM-dd HH:mm')
  })

  it('displays correct error message for date format, when textfield contains value with wrong format', async () => {
    wrapper = factory({
      propsData: {
        label: 'Testlabel',
        value: null,
        'use-date': true
      }
    })

    const textFieldInput = wrapper.find('input[type="text"]')

    await textFieldInput.setValue('2021-05-011')

    expect(wrapper.find('input[type="text"]').element.value).toBe('2021-05-011')

    const validationMessage = wrapper.find('div.v-messages__message')

    expect(validationMessage.text()).toBe('Please use the format: yyyy-MM-dd')
  })

  it('displays correct error message for time format, when textfield contains value with wrong format', async () => {
    wrapper = factory({
      propsData: {
        label: 'Testlabel',
        value: null,
        'use-time': true
      }
    })

    const textFieldInput = wrapper.find('input[type="text"]')

    await textFieldInput.setValue('2021-05-01')

    expect(wrapper.find('input[type="text"]').element.value).toBe('2021-05-01')

    const validationMessage = wrapper.find('div.v-messages__message')

    expect(validationMessage.text()).toBe('Please use the format: HH:mm')
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
    const expectedDateTime = DateTime.fromFormat('2020-05-01 00:00', 'yyyy-MM-dd HH:mm', { zone: 'UTC' })

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
    expect(wrapper.emitted().input[0]).toEqual([expectedDateTime])
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
    const expectedTime = '00:00'
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

  it('getPickerValue returns empty string when neither date, time nor datetime are true', () => {
    wrapper = factory({
      propsData: {
        label: 'Testlabel',
        value: null,
        'use-time': true
      }
    })

    wrapper.vm.isUseDatetime = false
    wrapper.vm.isUseTime = false
    wrapper.vm.isUseDateTime = false

    expect(wrapper.vm.getPickerValue()).toBe('')
  })
})
