/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2023
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
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
      parentDevice: null,
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0,
      epsgCode: '',
      x: null,
      y: null,
      z: null,
      elevationDatumName: '',
      elevationDatumUri: '',
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
      parentDevice: null,
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0,
      epsgCode: '',
      x: null,
      y: null,
      z: null,
      elevationDatumName: '',
      elevationDatumUri: '',
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
  it('should be allowed to have children', () => {
    const device = new Device()
    device.id = '1'

    const deviceMountAction = DeviceMountAction.createFromObject({
      id: '',
      device,
      parentPlatform: null,
      parentDevice: null,
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0,
      epsgCode: '',
      x: null,
      y: null,
      z: null,
      elevationDatumName: '',
      elevationDatumUri: '',
      beginContact: contact,
      endContact: null,
      beginDate: date,
      endDate: null,
      beginDescription: 'just a device mount action',
      endDescription: ''
    })
    const node = new DeviceNode(deviceMountAction)
    expect(node.canHaveChildren()).toBeTruthy()
  })
  it('should return an Array for children', () => {
    const firstDevice = new Device()
    firstDevice.id = '1'

    const firstDeviceMountAction = DeviceMountAction.createFromObject({
      id: '',
      device: firstDevice,
      parentPlatform: null,
      parentDevice: null,
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0,
      epsgCode: '',
      x: null,
      y: null,
      z: null,
      elevationDatumName: '',
      elevationDatumUri: '',
      beginContact: contact,
      endContact: null,
      beginDate: date,
      endDate: null,
      beginDescription: 'just a device mount action',
      endDescription: ''
    })
    const firstNode = new DeviceNode(firstDeviceMountAction)

    const secondDevice = new Device()
    const secondDeviceMountAction = DeviceMountAction.createFromObject({
      id: '',
      device: secondDevice,
      parentPlatform: null,
      parentDevice: firstDevice,
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0,
      epsgCode: '',
      x: null,
      y: null,
      z: null,
      elevationDatumName: '',
      elevationDatumUri: '',
      beginContact: contact,
      endContact: null,
      beginDate: date,
      endDate: null,
      beginDescription: 'a second device mount action',
      endDescription: ''
    })
    const secondNode = new DeviceNode(secondDeviceMountAction)

    firstNode.getTree().push(secondNode)

    expect(firstNode.children).toBeInstanceOf(Array)
    expect(firstNode.children).toHaveLength(1)
    expect(Object.is(firstNode.children[0], secondNode)).toBeTruthy()
  })
  it('should set the tree from an array of children', () => {
    const firstDevice = new Device()
    firstDevice.id = '1'

    const firstDeviceMountAction = DeviceMountAction.createFromObject({
      id: '',
      device: firstDevice,
      parentPlatform: null,
      parentDevice: null,
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0,
      epsgCode: '',
      x: null,
      y: null,
      z: null,
      elevationDatumName: '',
      elevationDatumUri: '',
      beginContact: contact,
      endContact: null,
      beginDate: date,
      endDate: null,
      beginDescription: 'just a device mount action',
      endDescription: ''
    })
    const firstNode = new DeviceNode(firstDeviceMountAction)

    const secondDevice = new Device()
    const secondDeviceMountAction = DeviceMountAction.createFromObject({
      id: '',
      device: secondDevice,
      parentPlatform: null,
      parentDevice: firstDevice,
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0,
      epsgCode: '',
      x: null,
      y: null,
      z: null,
      elevationDatumName: '',
      elevationDatumUri: '',
      beginContact: contact,
      endContact: null,
      beginDate: date,
      endDate: null,
      beginDescription: 'a second device mount action',
      endDescription: ''
    })
    const secondNode = new DeviceNode(secondDeviceMountAction)

    firstNode.children = [secondNode]
    expect(firstNode.getTree()).toHaveLength(1)
    expect(Object.is(firstNode.children[0], secondNode)).toBeTruthy()
  })
  it('should return a simple name of no offsets are given', () => {
    const device = new Device()
    device.id = '1'
    device.shortName = 'ABC'

    const deviceMountAction = DeviceMountAction.createFromObject({
      id: '',
      device,
      parentPlatform: null,
      parentDevice: null,
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0,
      epsgCode: '',
      x: null,
      y: null,
      z: null,
      elevationDatumName: '',
      elevationDatumUri: '',
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
      parentDevice: null,
      offsetX: 1,
      offsetY: 2,
      offsetZ: 3,
      epsgCode: '',
      x: null,
      y: null,
      z: null,
      elevationDatumName: '',
      elevationDatumUri: '',
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
