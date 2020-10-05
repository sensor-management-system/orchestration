import Vue from 'vue'
import Vuetify from 'vuetify'

import { mount, createLocalVue } from '@vue/test-utils'

// @ts-ignore
import DevicePropertyHierarchySelect from '@/components/DevicePropertyHierarchySelect.vue'
import Device from '@/models/Device'
import { DeviceProperty } from '@/models/DeviceProperty'

Vue.use(Vuetify)

describe('DevicePropertyHierarchySelect', () => {
  let wrapper: any
  let device1: Device
  let device2: Device
  let prop1: DeviceProperty
  let prop2: DeviceProperty
  let prop3: DeviceProperty

  beforeEach(() => {
    const localVue = createLocalVue()
    const vuetify = new Vuetify()

    device1 = new Device()
    device1.shortName = 'Device 1'

    prop1 = new DeviceProperty()
    prop1.propertyName = 'hPa'
    prop1.propertyUri = 'foo/bar'

    prop2 = new DeviceProperty()
    prop2.propertyName = 'm'
    prop2.propertyUri = 'foo/bar'

    device1.properties.push(prop1)
    device1.properties.push(prop2)

    device2 = new Device()
    device2.shortName = 'Device 2'

    prop3 = new DeviceProperty()
    prop3.propertyName = 'degree Celsius'
    prop3.propertyUri = 'foo/degcelsius'

    device2.properties.push(prop3)

    const devices = [device1, device2]

    wrapper = mount(DevicePropertyHierarchySelect, {
      localVue,
      vuetify,
      propsData: {
        devices
      }
    })
  })

  it('should return the properties of a device when a device is selected', () => {
    // select the first device
    wrapper.vm.selectDevice(device1)
    expect(wrapper.vm.propertiesOfDevice).toHaveLength(2)
    expect(wrapper.vm.propertiesOfDevice).toContain(prop1)
    expect(wrapper.vm.propertiesOfDevice).toContain(prop2)
  })

  it('should trigger an input event with a null value when a device is unselected', () => {
    // select the first device
    wrapper.vm.selectDevice(device1)
    // unset the device
    wrapper.vm.selectDevice()

    expect(wrapper.emitted().input).toBeTruthy()
    expect(wrapper.emitted().input.length).toBe(1)
    expect(wrapper.emitted().input[0]).toEqual([null])
  })

  it('should trigger an input event with a property when a property is selected', () => {
    // select the first device
    wrapper.vm.selectDevice(device1)
    // select the first property
    wrapper.vm.selectProperty(prop1)

    expect(wrapper.emitted().input).toBeTruthy()
    expect(wrapper.emitted().input.length).toBe(1)
    expect(wrapper.emitted().input[0]).toEqual([prop1])
  })

  it('should trigger an input event with a null value when a property is unselected', () => {
    // select the first device
    wrapper.vm.selectDevice(device1)
    // select the first property
    wrapper.vm.selectProperty(prop1)
    // unset the property
    wrapper.vm.selectProperty()

    expect(wrapper.emitted().input).toBeTruthy()
    expect(wrapper.emitted().input.length).toBe(2)
    expect(wrapper.emitted().input[1]).toEqual([null])
  })

  it('should trigger an input event with a property when a device with just one property is selected', () => {
    // select the second device
    wrapper.vm.selectDevice(device2)

    expect(wrapper.emitted().input).toBeTruthy()
    expect(wrapper.emitted().input.length).toBe(1)
    expect(wrapper.emitted().input[0]).toEqual([prop3])
  })
})
