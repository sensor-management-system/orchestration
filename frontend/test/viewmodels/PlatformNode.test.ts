/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
import { DateTime } from 'luxon'
import { Contact } from '@/models/Contact'
import { Platform } from '@/models/Platform'
import { PlatformMountAction } from '@/models/PlatformMountAction'
import { PlatformNode } from '@/viewmodels/PlatformNode'

const contact = new Contact()
const date = DateTime.utc(2020, 2, 3, 0, 0, 0, 0)

describe('PlatformNode', () => {
  it('should create a PlatformNode object', () => {
    const platform = new Platform()
    platform.id = '1'

    const platformMountAction = PlatformMountAction.createFromObject({
      id: '',
      platform,
      parentPlatform: null,
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
      beginDescription: 'just a platform mount action',
      endDescription: '',
      label: ''
    })

    const node = new PlatformNode(platformMountAction)
    expect(Object.is(node.unpack(), platformMountAction)).toBeTruthy()
    expect(node).toHaveProperty('id', PlatformNode.ID_PREFIX + platform.id)
  })
  it('should create a PlatformNode from another one', () => {
    const platform = new Platform()
    platform.id = '1'

    const firstPlatformMountAction = PlatformMountAction.createFromObject({
      id: '',
      platform,
      parentPlatform: null,
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
      beginDescription: 'just a platform mount action',
      endDescription: '',
      label: ''
    })

    const firstNode = new PlatformNode(firstPlatformMountAction)
    const secondNode = PlatformNode.createFromObject(firstNode)

    expect(Object.is(secondNode, firstNode)).toBeFalsy()
    expect(Object.is(secondNode.unpack(), firstNode.unpack())).toBeTruthy()
    expect(Object.is(secondNode.getTree(), firstNode.getTree())).toBeFalsy()
  })
  it('should be allowed to have children', () => {
    const platform = new Platform()
    platform.id = '1'

    const platformMountAction = PlatformMountAction.createFromObject({
      id: '',
      platform,
      parentPlatform: null,
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
      beginDescription: 'just a platform mount action',
      endDescription: '',
      label: ''
    })

    const node = new PlatformNode(platformMountAction)
    expect(node.canHaveChildren()).toBeTruthy()
  })
  it('should return an Array for children', () => {
    const firstPlatform = new Platform()
    firstPlatform.id = '1'

    const firstPlatformMountAction = PlatformMountAction.createFromObject({
      id: '',
      platform: firstPlatform,
      parentPlatform: null,
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
      beginDescription: 'just a platform mount action',
      endDescription: '',
      label: ''
    })
    const firstNode = new PlatformNode(firstPlatformMountAction)

    const secondPlatform = new Platform()
    const secondPlatformMountAction = PlatformMountAction.createFromObject({
      id: '',
      platform: secondPlatform,
      parentPlatform: firstPlatform,
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
      beginDescription: 'a second platform mount action',
      endDescription: '',
      label: ''
    })
    const secondNode = new PlatformNode(secondPlatformMountAction)

    firstNode.getTree().push(secondNode)

    expect(firstNode.children).toBeInstanceOf(Array)
    expect(firstNode.children).toHaveLength(1)
    expect(Object.is(firstNode.children[0], secondNode)).toBeTruthy()
  })
  it('should set the tree from an array of children', () => {
    const firstPlatform = new Platform()
    firstPlatform.id = '1'

    const firstPlatformMountAction = PlatformMountAction.createFromObject({
      id: '',
      platform: firstPlatform,
      parentPlatform: null,
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
      beginDescription: 'just a platform mount action',
      endDescription: '',
      label: ''
    })
    const firstNode = new PlatformNode(firstPlatformMountAction)

    const secondPlatform = new Platform()
    const secondPlatformMountAction = PlatformMountAction.createFromObject({
      id: '',
      platform: secondPlatform,
      parentPlatform: firstPlatform,
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
      beginDescription: 'a second platform mount action',
      endDescription: '',
      label: ''
    })
    const secondNode = new PlatformNode(secondPlatformMountAction)

    firstNode.children = [secondNode]
    expect(firstNode.getTree()).toHaveLength(1)
    expect(Object.is(firstNode.children[0], secondNode)).toBeTruthy()
  })

  it('should return a simple name of no offsets are given', () => {
    const platform = new Platform()
    platform.id = '1'
    platform.shortName = 'ABC'

    const platformMountAction = PlatformMountAction.createFromObject({
      id: '',
      platform,
      parentPlatform: null,
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
      beginDescription: 'just a platform mount action',
      endDescription: '',
      label: ''
    })
    const node = new PlatformNode(platformMountAction)
    const name = node.name
    const expectedName = 'ABC'

    expect(name).toEqual(expectedName)
  })
  it('should include offsets in the name', () => {
    const platform = new Platform()
    platform.id = '1'
    platform.shortName = 'ABC'

    const platformMountAction = PlatformMountAction.createFromObject({
      id: '',
      platform,
      parentPlatform: null,
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
      beginDescription: 'just a platform mount action',
      endDescription: '',
      label: ''
    })
    const node = new PlatformNode(platformMountAction)
    const name = node.name
    const expectedName = 'ABC (x=1m, y=2m, z=3m)'

    expect(name).toEqual(expectedName)
  })
})
