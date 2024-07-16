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
import { Device } from '@/models/Device'
import { DeviceMountAction } from '@/models/DeviceMountAction'
import { Platform } from '@/models/Platform'
import { PlatformMountAction } from '@/models/PlatformMountAction'

import {
  byDateOldestLast,
  byDateOldestFirst,
  buildConfigurationTree
} from '@/modelUtils/mountHelpers'

import { PlatformNode } from '@/viewmodels/PlatformNode'
import { DeviceNode } from '@/viewmodels/DeviceNode'

// import { dateTimesEqual } from '@/utils/dateHelper'

describe('byDateOldestLast', () => {
  it('should sort a list so that the oldest entry is the last one', () => {
    const elementA = {
      date: DateTime.utc(2020, 1, 1)
    }
    const elementB = {
      date: DateTime.utc(2021, 1, 1)
    }
    const elementC = {
      date: DateTime.utc(2019, 1, 1)
    }
    const list = [elementA, elementB, elementC]
    list.sort(byDateOldestLast)

    expect(list[0].date.year).toEqual(2021)
    expect(list[1].date.year).toEqual(2020)
    expect(list[2].date.year).toEqual(2019)
  })
  it('should return 0 if both dates are equal', () => {
    const elementA = {
      date: DateTime.utc(2020, 1, 1)
    }
    const elementB = {
      date: DateTime.utc(2020, 1, 1)
    }

    const result = byDateOldestLast(elementA, elementB)
    expect(result).toEqual(0)
  })
})
describe('byDateOldestFirst', () => {
  it('should sort a list so that the oldest entry is the first one', () => {
    const elementA = {
      date: DateTime.utc(2020, 1, 1)
    }
    const elementB = {
      date: DateTime.utc(2021, 1, 1)
    }
    const elementC = {
      date: DateTime.utc(2019, 1, 1)
    }
    const list = [elementA, elementB, elementC]
    list.sort(byDateOldestFirst)

    expect(list[0].date.year).toEqual(2019)
    expect(list[1].date.year).toEqual(2020)
    expect(list[2].date.year).toEqual(2021)
  })
  it('should return 0 if both dates are equal', () => {
    const elementA = {
      date: DateTime.utc(2020, 1, 1)
    }
    const elementB = {
      date: DateTime.utc(2020, 1, 1)
    }

    const result = byDateOldestFirst(elementA, elementB)
    expect(result).toEqual(0)
  })
})
describe('buildConfigurationTree', () => {
  it('should give us an empty tree if we don\'t provide any mount actions', () => {
    const mountActions = {
      platformMountActions: [],
      deviceMountActions: []
    }
    const date = DateTime.utc(2020, 1, 1)

    const tree = buildConfigurationTree(mountActions, date)

    expect(tree.length).toEqual(0)
  })
  it('should have one entry for an already mounted platform', () => {
    const platform = new Platform()
    platform.id = '1'
    platform.shortName = 'Platform 1'

    const contact = new Contact()
    contact.id = '1'
    contact.givenName = 'Max'
    contact.familyName = 'Mustermann'
    contact.email = 'max@mustermann.mail'

    const platformMountAction = PlatformMountAction.createFromObject({
      id: '',
      platform,
      parentPlatform: null,
      beginDate: DateTime.utc(2020, 1, 1),
      endDate: null,
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
      beginDescription: 'First mount',
      endDescription: '',
      label: ''
    })

    const mountActions = {
      platformMountActions: [platformMountAction],
      deviceMountActions: []
    }

    const treeAfterMount = buildConfigurationTree(mountActions, DateTime.utc(2020, 1, 1))

    expect(treeAfterMount.length).toEqual(1)
    expect(treeAfterMount.at(0).unpack()).toEqual(platformMountAction)

    const treeBeforeMount = buildConfigurationTree(mountActions, DateTime.utc(2019, 12, 31))
    expect(treeBeforeMount.length).toEqual(0)
  })

  it('should support parent platforms for platforms', () => {
    const platform1 = new Platform()
    platform1.id = '1'
    platform1.shortName = 'Platform 1'

    const platform2 = new Platform()
    platform2.id = '2'
    platform2.shortName = 'Platform 2'

    const contact = new Contact()
    contact.id = '1'
    contact.givenName = 'Max'
    contact.familyName = 'Mustermann'
    contact.email = 'max@mustermann.mail'

    const platformMountAction1 = PlatformMountAction.createFromObject({
      id: '',
      platform: platform1,
      parentPlatform: null,
      beginDate: DateTime.utc(2020, 1, 1),
      endDate: null,
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
      beginDescription: 'First mount',
      endDescription: '',
      label: ''
    })

    const platformMountAction2 = PlatformMountAction.createFromObject({
      id: '',
      platform: platform2,
      parentPlatform: platform1,
      beginDate: DateTime.utc(2020, 2, 1),
      endDate: null,
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
      beginDescription: 'Second mount',
      endDescription: '',
      label: ''
    })

    const mountActions = {
      platformMountActions: [platformMountAction1, platformMountAction2],
      deviceMountActions: []
    }

    const treeWithTwoPlatforms = buildConfigurationTree(mountActions, DateTime.utc(2020, 6, 1))

    expect(treeWithTwoPlatforms.length).toEqual(1)
    const platformNode = treeWithTwoPlatforms.at(0) as PlatformNode
    expect(platformNode.children.length).toEqual(1)
    expect(platformNode.unpack()).toEqual(platformMountAction1)
    expect(platformNode.children[0].unpack()).toEqual(platformMountAction2)
  })
  it('should also work with devices', () => {
    const platform1 = new Platform()
    platform1.id = '1'
    platform1.shortName = 'Platform 1'

    const platform2 = new Platform()
    platform2.id = '2'
    platform2.shortName = 'Platform 2'

    const device1 = new Device()
    device1.id = '11'
    device1.shortName = 'Device 1'

    const device2 = new Device()
    device2.id = '22'
    device2.shortName = 'Device 2'

    const contact = new Contact()
    contact.id = '1'
    contact.givenName = 'Max'
    contact.familyName = 'Mustermann'
    contact.email = 'max@mustermann.mail'

    const platformMountAction1 = PlatformMountAction.createFromObject({
      id: '',
      platform: platform1,
      parentPlatform: null,
      beginDate: DateTime.utc(2020, 1, 1),
      endDate: null,
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
      beginDescription: 'First mount',
      endDescription: '',
      label: ''
    })

    const platformMountAction2 = PlatformMountAction.createFromObject({
      id: '',
      platform: platform2,
      parentPlatform: platform1,
      beginDate: DateTime.utc(2020, 2, 1),
      endDate: null,
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
      beginDescription: 'Second mount',
      endDescription: '',
      label: ''
    })

    const deviceMountAction1 = DeviceMountAction.createFromObject({
      id: '',
      device: device1,
      parentPlatform: null,
      parentDevice: null,
      beginDate: DateTime.utc(2020, 1, 2),
      endDate: null,
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
      beginDescription: 'Device 1 mount',
      endDescription: '',
      label: ''
    })
    const deviceMountAction2 = DeviceMountAction.createFromObject({
      id: '',
      device: device2,
      parentPlatform: platform2,
      parentDevice: null,
      beginDate: DateTime.utc(2020, 1, 2),
      endDate: null,
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
      beginDescription: 'Device 1 mount',
      endDescription: '',
      label: ''
    })

    const mountActions = {
      platformMountActions: [platformMountAction1, platformMountAction2],
      deviceMountActions: [deviceMountAction1, deviceMountAction2]
    }

    const fullTree = buildConfigurationTree(mountActions, DateTime.utc(2020, 2, 15))

    expect(fullTree.length).toEqual(2)
    expect(fullTree.at(0).unpack()).toEqual(platformMountAction1)
    expect(fullTree.at(1).unpack()).toEqual(deviceMountAction1)

    const platformNode1 = fullTree.at(0) as PlatformNode
    expect(platformNode1.children.length).toEqual(1)
    expect(platformNode1.children[0].unpack()).toEqual(platformMountAction2)
    const platformNode2 = platformNode1.children[0] as PlatformNode
    expect(platformNode2.children.length).toEqual(1)
    expect(platformNode2.children[0].unpack()).toEqual(deviceMountAction2)
  })
  it('should also contain platforms if only their parent platform was unmounted', () => {
    /* This here is a bit difficult use case. Normally we would unmount all the
       things that are below the current mount (so all the rest of the tree from
       the selected platform ongoing).
       However, we may get inconsistent data, so that we unmounted a platform that
       still have some sub platforms & devices - and for those there is no unmount
       action.

       So there are two strategies to deal with it.

       First - and this is the one I liked most of the time - we don't include those
       devices & platforms anymore. We unmounted their parent, so they are no longer
       part of the tree.

       However, this has one significant problem: The user isn't able to fix it.
       So the alternative is to show them as if there is no parent platform.

       The user will be able to unmount them explicitly.
    */
    const platform1 = new Platform()
    platform1.id = '1'
    platform1.shortName = 'Platform 1'

    const platform2 = new Platform()
    platform2.id = '2'
    platform2.shortName = 'Platform 2'

    const contact = new Contact()
    contact.id = '1'
    contact.givenName = 'Max'
    contact.familyName = 'Mustermann'
    contact.email = 'max@mustermann.mail'

    const platformMountAction1 = PlatformMountAction.createFromObject({
      id: '',
      platform: platform1,
      parentPlatform: null,
      beginDate: DateTime.utc(2020, 1, 1),
      endDate: DateTime.utc(2021, 1, 1),
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
      beginDescription: 'First mount',
      endDescription: '',
      label: ''
    })

    const platformMountAction2 = PlatformMountAction.createFromObject({
      id: '',
      platform: platform2,
      parentPlatform: platform1,
      beginDate: DateTime.utc(2020, 2, 1),
      endDate: null,
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
      beginDescription: 'Second mount',
      endDescription: '',
      label: ''
    })

    const mountActions = {
      platformMountActions: [platformMountAction1, platformMountAction2],
      deviceMountActions: []
    }
    const treeWithTwoPlatforms = buildConfigurationTree(mountActions, DateTime.utc(2020, 6, 1))

    expect(treeWithTwoPlatforms.length).toEqual(1)
    const platformNode1 = treeWithTwoPlatforms.at(0) as PlatformNode
    expect(platformNode1.children.length).toEqual(1)
    expect(platformNode1.unpack()).toEqual(platformMountAction1)
    expect(platformNode1.children[0].unpack()).toEqual(platformMountAction2)

    const treeAfterParentUnmount = buildConfigurationTree(mountActions, DateTime.utc(2021, 6, 1))

    expect(treeAfterParentUnmount.length).toEqual(1)
    const platformNode2 = treeAfterParentUnmount.at(0) as PlatformNode
    expect(platformNode2.children.length).toEqual(0)
    expect(platformNode2.unpack()).toEqual(platformMountAction2)
  })
  it('should support the behaviour for missing parent platforms also for devices', () => {
    const platform1 = new Platform()
    platform1.id = '1'
    platform1.shortName = 'Platform 1'

    const device1 = new Device()
    device1.id = '11'
    device1.shortName = 'Device 2'

    const contact = new Contact()
    contact.id = '1'
    contact.givenName = 'Max'
    contact.familyName = 'Mustermann'
    contact.email = 'max@mustermann.mail'

    const platformMountAction1 = PlatformMountAction.createFromObject({
      id: '',
      platform: platform1,
      parentPlatform: null,
      beginDate: DateTime.utc(2020, 1, 1),
      endDate: DateTime.utc(2021, 1, 1),
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
      beginDescription: 'First mount',
      endDescription: '',
      label: ''
    })

    const deviceMountAction1 = DeviceMountAction.createFromObject({
      id: '',
      device: device1,
      parentPlatform: platform1,
      parentDevice: null,
      beginDate: DateTime.utc(2020, 1, 2),
      endDate: null,
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
      beginDescription: 'second mount',
      endDescription: '',
      label: ''
    })

    const mountActions = {
      platformMountActions: [platformMountAction1],
      deviceMountActions: [deviceMountAction1]
    }

    const treeAfterParentUnmount = buildConfigurationTree(mountActions, DateTime.utc(2021, 6, 1))

    expect(treeAfterParentUnmount.length).toEqual(1)
    const deviceNode1 = treeAfterParentUnmount.at(0) as DeviceNode
    expect(deviceNode1.unpack()).toEqual(deviceMountAction1)
  })
  it('should take the latest available mount information', () => {
    const platform = new Platform()
    platform.id = '1'
    platform.shortName = 'Platform 1'

    const contact = new Contact()
    contact.id = '1'
    contact.givenName = 'Max'
    contact.familyName = 'Mustermann'
    contact.email = 'max@mustermann.mail'

    const platformMountAction1 = PlatformMountAction.createFromObject({
      id: '',
      platform,
      parentPlatform: null,
      beginDate: DateTime.utc(2020, 1, 1),
      endDate: null,
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
      beginDescription: 'First mount',
      endDescription: '',
      label: ''
    })

    const platformMountAction2 = PlatformMountAction.createFromObject({
      id: '',
      platform,
      parentPlatform: null,
      beginDate: DateTime.utc(2021, 1, 1),
      endDate: null,
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
      beginDescription: 'First remount',
      endDescription: '',
      label: ''
    })

    const mountActions = {
      platformMountActions: [platformMountAction1, platformMountAction2],
      deviceMountActions: []
    }

    const treeFirstMount = buildConfigurationTree(mountActions, DateTime.utc(2020, 2, 1))

    expect(treeFirstMount.length).toEqual(1)
    expect(treeFirstMount.at(0).unpack()).toEqual(platformMountAction1)
    expect((treeFirstMount.at(0).unpack() as PlatformMountAction).offsetX).toEqual(0)

    const treeSecondMount = buildConfigurationTree(mountActions, DateTime.utc(2021, 2, 1))

    expect(treeSecondMount.length).toEqual(1)
    expect(treeSecondMount.at(0).unpack()).toEqual(platformMountAction2)
    expect((treeSecondMount.at(0).unpack() as PlatformMountAction).offsetX).toEqual(1)
  })
})
