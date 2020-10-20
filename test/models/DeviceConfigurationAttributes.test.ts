/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020
 * - Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
 * - Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
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
import { Device } from '@/models/Device'
import { DeviceConfigurationAttributes } from '@/models/DeviceConfigurationAttributes'
import { DeviceProperty } from '@/models/DeviceProperty'

describe('DeviceConfigurationAttributes', () => {
  it('should create a DeviceConfigurationAttributes object', () => {
    const device = new Device()
    device.id = '1'

    const attributes = new DeviceConfigurationAttributes(device)
    expect(attributes).toHaveProperty('device', device)
    expect(attributes).toHaveProperty('id', '1')
  })

  it('should create a DeviceConfigurationAttributes from an object', () => {
    const prop1 = new DeviceProperty()
    const prop2 = new DeviceProperty()

    const device = new Device()
    device.id = '1'
    device.properties = [prop1, prop2]

    const now = new Date()
    const attributes = DeviceConfigurationAttributes.createFromObject({ device, offsetX: 1, offsetY: 1, offsetZ: 1, calibrationDate: now, deviceProperties: [prop1] })
    expect(typeof attributes).toBe('object')
    expect(attributes.device).toBe(device)
    expect(attributes).toHaveProperty('id', '1')
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
    prop1.id = '1'
    const device = new Device()
    device.properties = [prop1]

    const attributes = new DeviceConfigurationAttributes(device)
    attributes.addDevicePropertyById(prop1.id)
    expect(attributes.deviceProperties[0]).toBe(prop1)
    expect(attributes.deviceProperties).toHaveLength(1)
  })

  it('should throw an error when assigning a property by its id that is not a member of the device', () => {
    const prop1 = new DeviceProperty()
    prop1.id = '1'
    const device = new Device()

    const attributes = new DeviceConfigurationAttributes(device)
    expect(() => { attributes.addDevicePropertyById(prop1.id) }).toThrow(Error)
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
    prop1.id = '1'
    const device = new Device()
    device.properties = [prop1]

    const attributes = new DeviceConfigurationAttributes(device)
    attributes.addDeviceProperty(prop1)

    attributes.removeDevicePropertyById(prop1.id)
    expect(attributes.deviceProperties).toHaveLength(0)
  })

  it('should throw an error when removing a property that is not assigned', () => {
    const prop1 = new DeviceProperty()
    prop1.id = '1'
    const device = new Device()

    const attributes = new DeviceConfigurationAttributes(device)
    expect(() => { attributes.addDevicePropertyById(prop1.id) }).toThrow(Error)
  })
})
