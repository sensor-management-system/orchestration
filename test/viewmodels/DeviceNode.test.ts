/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020-2021
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
import { DateTime } from 'luxon'
import { Contact } from '@/models/Contact'
import { Device } from '@/models/Device'
import { DeviceMountAction } from '@/models/DeviceMountAction'
import { DeviceNode } from '@/viewmodels/DeviceNode'

const contact = new Contact()
const date = DateTime.utc(2020, 2, 3, 0, 0, 0, 0)

describe('DeviceNode', () => {
  it('should create a DeviceNode object', () => {
    const device = new Device()
    device.id = '1'

    const deviceMountAction = DeviceMountAction.createFromObject({
      id: '',
      device,
      parentPlatform: null,
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0,
      beginContact: contact,
      endContact: null,
      beginDate: date,
      endDate: null,
      beginDescription: 'just a device mount action',
      endDescription: ''
    })
    const node = new DeviceNode(deviceMountAction)
    expect(Object.is(node.unpack(), deviceMountAction)).toBeTruthy()
    expect(node).toHaveProperty('id', DeviceNode.ID_PREFIX + device.id)
  })
  it('should create a DeviceNode from another one', () => {
    const firstDevice = new Device()
    firstDevice.id = '1'

    const firstDeviceMountAction = DeviceMountAction.createFromObject({
      id: '',
      device: firstDevice,
      parentPlatform: null,
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0,
      beginContact: contact,
      endContact: null,
      beginDate: date,
      endDate: null,
      beginDescription: 'just a device mount action',
      endDescription: ''
    })
    const firstNode = new DeviceNode(firstDeviceMountAction)
    const secondNode = DeviceNode.createFromObject(firstNode)

    expect(Object.is(secondNode, firstNode)).toBeFalsy()
    expect(Object.is(secondNode.unpack(), firstNode.unpack())).toBeTruthy()
  })
  it('should not be allowed to have children', () => {
    const device = new Device()
    device.id = '1'

    const deviceMountAction = DeviceMountAction.createFromObject({
      id: '',
      device,
      parentPlatform: null,
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0,
      beginContact: contact,
      endContact: null,
      beginDate: date,
      endDate: null,
      beginDescription: 'just a device mount action',
      endDescription: ''
    })
    const node = new DeviceNode(deviceMountAction)
    expect(node.canHaveChildren()).toBeFalsy()
  })
  it('should return a simple name of no offsets are given', () => {
    const device = new Device()
    device.id = '1'
    device.shortName = 'ABC'

    const deviceMountAction = DeviceMountAction.createFromObject({
      id: '',
      device,
      parentPlatform: null,
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0,
      beginContact: contact,
      endContact: null,
      beginDate: date,
      endDate: null,
      beginDescription: 'just a device mount action',
      endDescription: ''
    })
    const node = new DeviceNode(deviceMountAction)
    const name = node.name
    const expectedName = 'ABC'

    expect(name).toEqual(expectedName)
  })
  it('should include offsets in the name', () => {
    const device = new Device()
    device.id = '1'
    device.shortName = 'ABC'

    const deviceMountAction = DeviceMountAction.createFromObject({
      id: '',
      device,
      parentPlatform: null,
      offsetX: 1,
      offsetY: 2,
      offsetZ: 3,
      beginContact: contact,
      endContact: null,
      beginDate: date,
      endDate: null,
      beginDescription: 'just a device mount action',
      endDescription: ''
    })
    const node = new DeviceNode(deviceMountAction)
    const name = node.name
    const expectedName = 'ABC (x=1m, y=2m, z=3m)'

    expect(name).toEqual(expectedName)
  })
})
