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
    expect(attributes).toHaveProperty('device', device)
    expect(attributes).toHaveProperty('id', 1)
    expect(attributes).toHaveProperty('offsetX', 1)
    expect(attributes).toHaveProperty('offsetY', 1)
    expect(attributes).toHaveProperty('offsetZ', 1)
    expect(attributes).toHaveProperty('calibrationDate', now)
  })

  it('should throw an error when assigning a property that is not a member of the device', () => {
    const prop1 = new DeviceProperty()
    const prop2 = new DeviceProperty()
    const prop3 = new DeviceProperty()

    const device = new Device()
    device.id = 1
    device.properties = [prop1, prop2]

    const attributes = new DeviceConfigurationAttributes(device)
    expect(() => { attributes.deviceProperties = [prop1, prop2, prop3]; return true }).toThrow(Error)
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

  it('should throw an error when using a invalid path', () => {
    const device = new Device()
    device.id = 1

    const attributes = new DeviceConfigurationAttributes(device)
    expect(() => attributes.setPath('id', 2)).toThrow(TypeError)
  })
})
