import Device from '@/models/Device'
import { DeviceConfigurationAttributes } from '@/models/DeviceConfigurationAttributes'
import { DeviceProperty } from '@/models/DeviceProperty'

describe('DeviceConfigurationAttributes', () => {
  it('should create a DeviceConfigurationAttributes object', () => {
    const device = new Device()
    device.id = 1

    const attributes = new DeviceConfigurationAttributes(device)
    expect(attributes).toHaveProperty('device', device)
    expect(attributes).toHaveProperty('id', 1)
  })

  it('should create a DeviceConfigurationAttributes from an object', () => {
    const prop1 = new DeviceProperty()
    const prop2 = new DeviceProperty()

    const device = new Device()
    device.id = 1
    device.properties = [prop1, prop2]

    const now = new Date()
    const attributes = DeviceConfigurationAttributes.createFromObject({ device, offsetX: 1, offsetY: 1, offsetZ: 1, calibrationDate: now, deviceProperties: [prop1] })
    expect(typeof attributes).toBe('object')
    expect(attributes.device).toBe(device)
    expect(attributes).toHaveProperty('id', 1)
    expect(attributes).toHaveProperty('offsetX', 1)
    expect(attributes).toHaveProperty('offsetY', 1)
    expect(attributes).toHaveProperty('offsetZ', 1)
    expect(attributes).toHaveProperty('calibrationDate', now)
  })

  it('should assign a deviceProperty that is a member of the device', () => {
    const prop1 = new DeviceProperty()
    const device = new Device()
    device.properties = [prop1]

    const attributes = new DeviceConfigurationAttributes(device)
    attributes.addDeviceProperty(prop1)
    expect(attributes.deviceProperties[0]).toBe(prop1)
    expect(attributes.deviceProperties).toHaveLength(1)
  })

  it('should throw an error when assigning a property that is not a member of the device', () => {
    const prop1 = new DeviceProperty()
    const device = new Device()

    const attributes = new DeviceConfigurationAttributes(device)
    expect(() => { attributes.addDeviceProperty(prop1) }).toThrow(Error)
  })

  it('should assign a deviceProperty that is a member of the device by its id', () => {
    const prop1 = new DeviceProperty()
    prop1.id = 1
    const device = new Device()
    device.properties = [prop1]

    const attributes = new DeviceConfigurationAttributes(device)
    attributes.addDevicePropertyById(prop1.id)
    expect(attributes.deviceProperties[0]).toBe(prop1)
    expect(attributes.deviceProperties).toHaveLength(1)
  })

  it('should throw an error when assigning a property by its id that is not a member of the device', () => {
    const prop1 = new DeviceProperty()
    prop1.id = 1
    const device = new Device()

    const attributes = new DeviceConfigurationAttributes(device)
    expect(() => { attributes.addDevicePropertyById(prop1.id) }).toThrow(Error)
  })

  it('should set a property by its path', () => {
    const device = new Device()
    device.id = 1

    const now = new Date()
    const attributes = new DeviceConfigurationAttributes(device)
    attributes.setPath('offsetX', 1)
    attributes.setPath('offsetY', 1)
    attributes.setPath('offsetZ', 1)
    attributes.setPath('calibrationDate', now)

    expect(attributes).toHaveProperty('id', 1)
    expect(attributes).toHaveProperty('offsetX', 1)
    expect(attributes).toHaveProperty('offsetY', 1)
    expect(attributes).toHaveProperty('offsetZ', 1)
    expect(attributes).toHaveProperty('calibrationDate', now)
  })

  it('should remove a deviceProperty', () => {
    const prop1 = new DeviceProperty()
    const device = new Device()
    device.properties = [prop1]

    const attributes = new DeviceConfigurationAttributes(device)
    attributes.addDeviceProperty(prop1)

    attributes.removeDeviceProperty(prop1)
    expect(attributes.deviceProperties).toHaveLength(0)
  })

  it('should remove a deviceProperty by its id', () => {
    const prop1 = new DeviceProperty()
    prop1.id = 1
    const device = new Device()
    device.properties = [prop1]

    const attributes = new DeviceConfigurationAttributes(device)
    attributes.addDeviceProperty(prop1)

    attributes.removeDevicePropertyById(prop1.id)
    expect(attributes.deviceProperties).toHaveLength(0)
  })

  it('should throw an error when removing a property that is not assigned', () => {
    const prop1 = new DeviceProperty()
    prop1.id = 1
    const device = new Device()

    const attributes = new DeviceConfigurationAttributes(device)
    expect(() => { attributes.addDevicePropertyById(prop1.id) }).toThrow(Error)
  })

  it('should throw an error when using a invalid path', () => {
    const device = new Device()
    device.id = 1

    const attributes = new DeviceConfigurationAttributes(device)
    expect(() => attributes.setPath('id', 2)).toThrow(TypeError)
  })
})
