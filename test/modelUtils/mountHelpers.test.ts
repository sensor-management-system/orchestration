/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020, 2021
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
import { DeviceUnmountAction } from '@/models/DeviceUnmountAction'
import { Platform } from '@/models/Platform'
import { PlatformMountAction } from '@/models/PlatformMountAction'
import { PlatformUnmountAction } from '@/models/PlatformUnmountAction'

import {
  byDateOldestLast,
  byDateOldestFirst,
  buildConfigurationTree,
  getActiveDevices,
  getActivePlatforms,
  mountDevice,
  mountPlatform,
  unmount
} from '@/modelUtils/mountHelpers'

import { PlatformNode } from '@/viewmodels/PlatformNode'
import { DeviceNode } from '@/viewmodels/DeviceNode'

import { dateTimesEqual } from '@/utils/dateHelper'

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
      platformUnmountActions: [],
      deviceMountActions: [],
      deviceUnmountActions: []
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
      date: DateTime.utc(2020, 1, 1),
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0,
      contact,
      description: 'First mount'
    })

    const mountActions = {
      platformMountActions: [platformMountAction],
      platformUnmountActions: [],
      deviceMountActions: [],
      deviceUnmountActions: []
    }

    const treeAfterMount = buildConfigurationTree(mountActions, DateTime.utc(2020, 1, 1))

    expect(treeAfterMount.length).toEqual(1)
    expect(treeAfterMount.at(0).unpack()).toEqual(platformMountAction)

    const treeBeforeMount = buildConfigurationTree(mountActions, DateTime.utc(2019, 12, 31))
    expect(treeBeforeMount.length).toEqual(0)
  })
  it('should support platformUnmountActions and change the tree accordingly', () => {
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
      date: DateTime.utc(2020, 1, 1),
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0,
      contact,
      description: 'First mount'
    })
    const platformUnmountAction = PlatformUnmountAction.createFromObject({
      id: '',
      platform,
      date: DateTime.utc(2021, 1, 1),
      contact,
      description: 'First unmount'
    })

    const mountActions = {
      platformMountActions: [platformMountAction],
      platformUnmountActions: [platformUnmountAction],
      deviceMountActions: [],
      deviceUnmountActions: []
    }

    const treeAfterMount = buildConfigurationTree(mountActions, DateTime.utc(2020, 1, 1))
    expect(treeAfterMount.length).toEqual(1)
    expect(treeAfterMount.at(0).unpack()).toEqual(platformMountAction)

    const treeAfterUnmount = buildConfigurationTree(mountActions, DateTime.utc(2021, 1, 1))
    expect(treeAfterUnmount.length).toEqual(0)
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
      date: DateTime.utc(2020, 1, 1),
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0,
      contact,
      description: 'First mount'
    })

    const platformMountAction2 = PlatformMountAction.createFromObject({
      id: '',
      platform: platform2,
      parentPlatform: platform1,
      date: DateTime.utc(2020, 2, 1),
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0,
      contact,
      description: 'Second mount'
    })
    const platformUnmountAction1 = PlatformUnmountAction.createFromObject({
      id: '',
      platform: platform1,
      date: DateTime.utc(2021, 1, 1),
      contact,
      description: 'Platform 1 unmount'
    })
    const platformUnmountAction2 = PlatformUnmountAction.createFromObject({
      id: '',
      platform: platform2,
      date: DateTime.utc(2020, 12, 1),
      contact,
      description: 'Platform 2 unmount'
    })

    const mountActions = {
      platformMountActions: [platformMountAction1, platformMountAction2],
      platformUnmountActions: [platformUnmountAction1, platformUnmountAction2],
      deviceMountActions: [],
      deviceUnmountActions: []
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
      date: DateTime.utc(2020, 1, 1),
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0,
      contact,
      description: 'First mount'
    })

    const platformMountAction2 = PlatformMountAction.createFromObject({
      id: '',
      platform: platform2,
      parentPlatform: platform1,
      date: DateTime.utc(2020, 2, 1),
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0,
      contact,
      description: 'Second mount'
    })
    const platformUnmountAction1 = PlatformUnmountAction.createFromObject({
      id: '',
      platform: platform1,
      date: DateTime.utc(2021, 1, 1),
      contact,
      description: 'Platform 1 unmount'
    })
    const platformUnmountAction2 = PlatformUnmountAction.createFromObject({
      id: '',
      platform: platform2,
      date: DateTime.utc(2020, 12, 1),
      contact,
      description: 'Platform 2 unmount'
    })
    const deviceMountAction1 = DeviceMountAction.createFromObject({
      id: '',
      device: device1,
      parentPlatform: null,
      date: DateTime.utc(2020, 1, 2),
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0,
      contact,
      description: 'Device 1 mount'
    })
    const deviceMountAction2 = DeviceMountAction.createFromObject({
      id: '',
      device: device2,
      parentPlatform: platform2,
      date: DateTime.utc(2020, 2, 2),
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0,
      contact,
      description: 'Device 2 mount'
    })
    const deviceUnmountAction1 = DeviceUnmountAction.createFromObject({
      id: '',
      device: device1,
      date: DateTime.utc(2020, 3, 1),
      contact,
      description: 'Device 1 unmount'
    })
    const deviceUnmountAction2 = DeviceUnmountAction.createFromObject({
      id: '',
      device: device2,
      date: DateTime.utc(2020, 5, 1),
      contact,
      description: 'Device 2 unmount'
    })

    const mountActions = {
      platformMountActions: [platformMountAction1, platformMountAction2],
      platformUnmountActions: [platformUnmountAction1, platformUnmountAction2],
      deviceMountActions: [deviceMountAction1, deviceMountAction2],
      deviceUnmountActions: [deviceUnmountAction1, deviceUnmountAction2]
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
      date: DateTime.utc(2020, 1, 1),
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0,
      contact,
      description: 'First mount'
    })

    const platformMountAction2 = PlatformMountAction.createFromObject({
      id: '',
      platform: platform2,
      parentPlatform: platform1,
      date: DateTime.utc(2020, 2, 1),
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0,
      contact,
      description: 'Second mount'
    })
    const platformUnmountAction1 = PlatformUnmountAction.createFromObject({
      id: '',
      platform: platform1,
      date: DateTime.utc(2021, 1, 1),
      contact,
      description: 'Platform 1 unmount'
    })

    const mountActions = {
      platformMountActions: [platformMountAction1, platformMountAction2],
      platformUnmountActions: [platformUnmountAction1],
      deviceMountActions: [],
      deviceUnmountActions: []
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
      date: DateTime.utc(2020, 1, 1),
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0,
      contact,
      description: 'First mount'
    })

    const deviceMountAction1 = DeviceMountAction.createFromObject({
      id: '',
      device: device1,
      parentPlatform: platform1,
      date: DateTime.utc(2020, 2, 1),
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0,
      contact,
      description: 'Second mount'
    })
    const platformUnmountAction1 = PlatformUnmountAction.createFromObject({
      id: '',
      platform: platform1,
      date: DateTime.utc(2021, 1, 1),
      contact,
      description: 'Platform 1 unmount'
    })

    const mountActions = {
      platformMountActions: [platformMountAction1],
      platformUnmountActions: [platformUnmountAction1],
      deviceMountActions: [deviceMountAction1],
      deviceUnmountActions: []
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
      date: DateTime.utc(2020, 1, 1),
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0,
      contact,
      description: 'First mount'
    })

    const platformMountAction2 = PlatformMountAction.createFromObject({
      id: '',
      platform,
      parentPlatform: null,
      date: DateTime.utc(2021, 1, 1),
      offsetX: 1,
      offsetY: 2,
      offsetZ: 3,
      contact,
      description: 'First remount'
    })

    const mountActions = {
      platformMountActions: [platformMountAction1, platformMountAction2],
      platformUnmountActions: [],
      deviceMountActions: [],
      deviceUnmountActions: []
    }

    const treeFirstMount = buildConfigurationTree(mountActions, DateTime.utc(2020, 2, 1))

    expect(treeFirstMount.length).toEqual(1)
    expect(treeFirstMount.at(0).unpack()).toEqual(platformMountAction1)
    expect(treeFirstMount.at(0).unpack().offsetX).toEqual(0)

    const treeSecondMount = buildConfigurationTree(mountActions, DateTime.utc(2021, 2, 1))

    expect(treeSecondMount.length).toEqual(1)
    expect(treeSecondMount.at(0).unpack()).toEqual(platformMountAction2)
    expect(treeSecondMount.at(0).unpack().offsetX).toEqual(1)
  })
})
describe('unmount', () => {
  it('should add a single unmount action', () => {
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
      date: DateTime.utc(2020, 1, 1),
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0,
      contact,
      description: 'First mount'
    })

    const mountActionsStart = {
      platformMountActions: [platformMountAction],
      platformUnmountActions: [],
      deviceMountActions: [],
      deviceUnmountActions: []
    }

    expect(mountActionsStart.platformUnmountActions.length).toEqual(0)

    const unmountDate = DateTime.utc(2020, 2, 1)

    const mountActionsEnd = unmount(
      mountActionsStart,
      new PlatformNode(platformMountAction),
      unmountDate,
      contact,
      'unmount action'
    )

    expect(mountActionsEnd.platformUnmountActions.length).toEqual(1)
    const platformUnmountAction = mountActionsEnd.platformUnmountActions[0]
    expect(platformUnmountAction.platform).toEqual(platform)
    expect(platformUnmountAction.contact).toEqual(contact)
    expect(platformUnmountAction.date).toEqual(unmountDate)
    expect(platformUnmountAction.description).toEqual('unmount action')
  })
  it('should also unmount devices', () => {
    const device = new Device()
    device.id = '1'
    device.shortName = 'Device 1'

    const contact = new Contact()
    contact.id = '1'
    contact.givenName = 'Max'
    contact.familyName = 'Mustermann'
    contact.email = 'max@mustermann.mail'

    const deviceMountAction = DeviceMountAction.createFromObject({
      id: '',
      device,
      parentPlatform: null,
      date: DateTime.utc(2020, 1, 1),
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0,
      contact,
      description: 'First mount'
    })

    const mountActionsStart = {
      platformMountActions: [],
      platformUnmountActions: [],
      deviceMountActions: [deviceMountAction],
      deviceUnmountActions: []
    }

    expect(mountActionsStart.deviceUnmountActions.length).toEqual(0)

    const unmountDate = DateTime.utc(2020, 2, 1)

    const mountActionsEnd = unmount(
      mountActionsStart,
      new DeviceNode(deviceMountAction),
      unmountDate,
      contact,
      'unmount action'
    )

    expect(mountActionsEnd.deviceUnmountActions.length).toEqual(1)
    const deviceUnmountAction = mountActionsEnd.deviceUnmountActions[0]
    expect(deviceUnmountAction.device).toEqual(device)
    expect(deviceUnmountAction.contact).toEqual(contact)
    expect(deviceUnmountAction.date).toEqual(unmountDate)
    expect(deviceUnmountAction.description).toEqual('unmount action')
  })
  it('should delete all later mount & unmount actions', () => {
    const platform1 = new Platform()
    platform1.id = '1'
    platform1.shortName = 'Platform 1'

    const platform2 = new Platform()
    platform2.id = '2'
    platform2.shortName = 'Platform 2'

    const device1 = new Device()
    device1.id = '1'
    device1.shortName = 'Device 1'

    const contact = new Contact()
    contact.id = '1'
    contact.givenName = 'Max'
    contact.familyName = 'Mustermann'
    contact.email = 'max@mustermann.mail'

    const platformMountAction1 = PlatformMountAction.createFromObject({
      id: '',
      platform: platform1,
      parentPlatform: null,
      date: DateTime.utc(2020, 1, 1),
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0,
      contact,
      description: 'First mount'
    })

    const platformMountAction2 = PlatformMountAction.createFromObject({
      id: '',
      platform: platform2,
      parentPlatform: platform1,
      date: DateTime.utc(2021, 1, 1),
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0,
      contact,
      description: 'Second mount'
    })

    const platformUnmountAction1 = PlatformUnmountAction.createFromObject({
      id: '',
      platform: platform1,
      date: DateTime.utc(2021, 5, 26),
      contact,
      description: 'Unmount platform 1'
    })

    const platformUnmountAction2 = PlatformUnmountAction.createFromObject({
      id: '',
      platform: platform2,
      date: DateTime.utc(2021, 5, 25),
      contact,
      description: 'Unmount platform 2'
    })

    const deviceMountAction1 = DeviceMountAction.createFromObject({
      id: '',
      device: device1,
      parentPlatform: platform2,
      date: DateTime.utc(2021, 1, 2),
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0,
      contact,
      description: 'Mount device 1'
    })

    const deviceUnmountAction1 = DeviceUnmountAction.createFromObject({
      id: '',
      device: device1,
      date: DateTime.utc(2021, 5, 24),
      contact,
      description: 'Unmount device 1'
    })

    const mountActionsStart = {
      platformMountActions: [platformMountAction1, platformMountAction2],
      platformUnmountActions: [platformUnmountAction1, platformUnmountAction2],
      deviceMountActions: [deviceMountAction1],
      deviceUnmountActions: [deviceUnmountAction1]
    }

    const unmountDate = DateTime.utc(2020, 2, 1)

    const mountActionsEnd = unmount(
      mountActionsStart,
      new PlatformNode(platformMountAction1),
      unmountDate,
      contact,
      'unmount action for whole tree'
    )

    // all the later mount & unmount actions with the very same parent
    // platform should be removed

    expect(mountActionsEnd.platformMountActions.length).toEqual(1)
    expect(mountActionsEnd.platformUnmountActions.length).toEqual(1)
    expect(mountActionsEnd.deviceMountActions.length).toEqual(0)
    expect(mountActionsEnd.deviceUnmountActions.length).toEqual(0)

    expect(mountActionsEnd.platformUnmountActions[0].date).toEqual(unmountDate)
    expect(mountActionsEnd.platformUnmountActions[0].platform).toEqual(platform1)
  })
  it('should delete all later mount & unmount actions - also with 3 platform levels', () => {
    const platform1 = new Platform()
    platform1.id = '1'
    platform1.shortName = 'Platform 1'

    const platform2 = new Platform()
    platform2.id = '2'
    platform2.shortName = 'Platform 2'

    const platform3 = new Platform()
    platform3.id = '3'
    platform3.shortName = 'Platform 3'

    const device1 = new Device()
    device1.id = '1'
    device1.shortName = 'Device 1'

    const contact = new Contact()
    contact.id = '1'
    contact.givenName = 'Max'
    contact.familyName = 'Mustermann'
    contact.email = 'max@mustermann.mail'

    const platformMountAction1 = PlatformMountAction.createFromObject({
      id: '',
      platform: platform1,
      parentPlatform: null,
      date: DateTime.utc(2020, 1, 1),
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0,
      contact,
      description: 'First mount'
    })

    const platformMountAction2 = PlatformMountAction.createFromObject({
      id: '',
      platform: platform2,
      parentPlatform: platform1,
      date: DateTime.utc(2021, 1, 1),
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0,
      contact,
      description: 'Second mount'
    })

    const platformMountAction3 = PlatformMountAction.createFromObject({
      id: '',
      platform: platform3,
      parentPlatform: platform2,
      date: DateTime.utc(2021, 1, 2),
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0,
      contact,
      description: 'Third mount'
    })

    const platformUnmountAction1 = PlatformUnmountAction.createFromObject({
      id: '',
      platform: platform1,
      date: DateTime.utc(2021, 5, 26),
      contact,
      description: 'Unmount platform 1'
    })

    const platformUnmountAction2 = PlatformUnmountAction.createFromObject({
      id: '',
      platform: platform2,
      date: DateTime.utc(2021, 5, 25),
      contact,
      description: 'Unmount platform 2'
    })

    const platformUnmountAction3 = PlatformUnmountAction.createFromObject({
      id: '',
      platform: platform3,
      date: DateTime.utc(2021, 5, 24),
      contact,
      description: 'Unmount platform 3'
    })

    const deviceMountAction1 = DeviceMountAction.createFromObject({
      id: '',
      device: device1,
      parentPlatform: platform3,
      date: DateTime.utc(2021, 1, 3),
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0,
      contact,
      description: 'Mount device 1'
    })

    const deviceUnmountAction1 = DeviceUnmountAction.createFromObject({
      id: '',
      device: device1,
      date: DateTime.utc(2021, 5, 23),
      contact,
      description: 'Unmount device 1'
    })

    const mountActionsStart = {
      platformMountActions: [platformMountAction1, platformMountAction2, platformMountAction3],
      platformUnmountActions: [platformUnmountAction1, platformUnmountAction2, platformUnmountAction3],
      deviceMountActions: [deviceMountAction1],
      deviceUnmountActions: [deviceUnmountAction1]
    }

    const unmountDate = DateTime.utc(2020, 2, 1)

    const mountActionsEnd = unmount(
      mountActionsStart,
      new PlatformNode(platformMountAction1),
      unmountDate,
      contact,
      'unmount action for whole tree'
    )

    // all the later mount & unmount actions with the very same parent
    // platform should be removed

    expect(mountActionsEnd.platformMountActions.length).toEqual(1)
    expect(mountActionsEnd.platformUnmountActions.length).toEqual(1)
    expect(mountActionsEnd.deviceMountActions.length).toEqual(0)
    expect(mountActionsEnd.deviceUnmountActions.length).toEqual(0)

    expect(mountActionsEnd.platformUnmountActions[0].date).toEqual(unmountDate)
    expect(mountActionsEnd.platformUnmountActions[0].platform).toEqual(platform1)
  })
  it('should just remove mount actions if the unmount has the very same date', () => {
    const platform1 = new Platform()
    platform1.id = '1'
    platform1.shortName = 'Platform 1'

    const device1 = new Device()
    device1.id = '1'
    device1.shortName = 'Device 1'

    const contact = new Contact()
    contact.id = '1'
    contact.givenName = 'Max'
    contact.familyName = 'Mustermann'
    contact.email = 'max@mustermann.mail'

    const date = DateTime.utc(2020, 1, 1)

    const platformMountAction1 = PlatformMountAction.createFromObject({
      id: '',
      platform: platform1,
      parentPlatform: null,
      date,
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0,
      contact,
      description: 'First mount'
    })

    const deviceMountAction1 = DeviceMountAction.createFromObject({
      id: '',
      device: device1,
      parentPlatform: platform1,
      date,
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0,
      contact,
      description: 'Mount device 1'
    })

    const mountActionsStart = {
      platformMountActions: [platformMountAction1],
      platformUnmountActions: [],
      deviceMountActions: [deviceMountAction1],
      deviceUnmountActions: []
    }

    const mountActionsEnd = unmount(
      mountActionsStart,
      new PlatformNode(platformMountAction1),
      date,
      contact,
      'unmount action for whole tree'
    )

    expect(mountActionsEnd.platformMountActions.length).toEqual(0)
    expect(mountActionsEnd.platformUnmountActions.length).toEqual(0)
    expect(mountActionsEnd.deviceMountActions.length).toEqual(0)
    expect(mountActionsEnd.deviceUnmountActions.length).toEqual(0)
  })
  it('should combine the removing logic & the unmount of future subcomponents', () => {
    const platform1 = new Platform()
    platform1.id = '13'
    platform1.shortName = 'Platform 1'

    const device1 = new Device()
    device1.id = '53'
    device1.shortName = 'Device 1'

    const contact = new Contact()
    contact.id = '1'
    contact.givenName = 'Max'
    contact.familyName = 'Mustermann'
    contact.email = 'max@mustermann.mail'

    const date = DateTime.utc(2020, 1, 1)

    const platformMountAction1 = PlatformMountAction.createFromObject({
      id: '',
      platform: platform1,
      parentPlatform: null,
      date,
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0,
      contact,
      description: 'First mount'
    })

    const deviceMountAction1 = DeviceMountAction.createFromObject({
      id: '',
      device: device1,
      parentPlatform: platform1,
      date,
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0,
      contact,
      description: 'Mount device 1'
    })

    const deviceUnmountAction1 = DeviceUnmountAction.createFromObject({
      id: '',
      device: device1,
      date: DateTime.utc(2020, 2, 1),
      contact,
      description: 'Unmount of device 1'
    })

    const mountActionsStart = {
      platformMountActions: [platformMountAction1],
      platformUnmountActions: [],
      deviceMountActions: [deviceMountAction1],
      deviceUnmountActions: [deviceUnmountAction1]
    }

    const mountActionsEnd = unmount(
      mountActionsStart,
      new PlatformNode(platformMountAction1),
      date,
      contact,
      'unmount action for whole tree'
    )

    expect(mountActionsEnd.platformMountActions.length).toEqual(0)
    expect(mountActionsEnd.platformUnmountActions.length).toEqual(0)
    expect(mountActionsEnd.deviceMountActions.length).toEqual(0)
    expect(mountActionsEnd.deviceUnmountActions.length).toEqual(0)
  })
  it('should combine the removing logic & the unmount of future subcomponents (later device mount)', () => {
    const platform1 = new Platform()
    platform1.id = '1'
    platform1.shortName = 'Platform 1'

    const device1 = new Device()
    device1.id = '1'
    device1.shortName = 'Device 1'

    const contact = new Contact()
    contact.id = '1'
    contact.givenName = 'Max'
    contact.familyName = 'Mustermann'
    contact.email = 'max@mustermann.mail'

    const date = DateTime.utc(2020, 1, 1)

    const platformMountAction1 = PlatformMountAction.createFromObject({
      id: '',
      platform: platform1,
      parentPlatform: null,
      date,
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0,
      contact,
      description: 'First mount'
    })

    const deviceMountAction1 = DeviceMountAction.createFromObject({
      id: '',
      device: device1,
      parentPlatform: platform1,
      date: DateTime.utc(2020, 1, 2),
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0,
      contact,
      description: 'Mount device 1'
    })

    const deviceUnmountAction1 = DeviceUnmountAction.createFromObject({
      id: '',
      device: device1,
      date: DateTime.utc(2020, 2, 1),
      contact,
      description: 'Unmount of device 1'
    })

    const mountActionsStart = {
      platformMountActions: [platformMountAction1],
      platformUnmountActions: [],
      deviceMountActions: [deviceMountAction1],
      deviceUnmountActions: [deviceUnmountAction1]
    }

    const mountActionsEnd = unmount(
      mountActionsStart,
      new PlatformNode(platformMountAction1),
      date,
      contact,
      'unmount action for whole tree'
    )

    expect(mountActionsEnd.platformMountActions.length).toEqual(0)
    expect(mountActionsEnd.platformUnmountActions.length).toEqual(0)
    expect(mountActionsEnd.deviceMountActions.length).toEqual(0)
    expect(mountActionsEnd.deviceUnmountActions.length).toEqual(0)
  })
  it('should combine the removing logic & the unmount of future subcomponents - and should be resistent to datetime value equality', () => {
    const platform1 = new Platform()
    platform1.id = '13'
    platform1.shortName = 'Platform 1'

    const device1 = new Device()
    device1.id = '53'
    device1.shortName = 'Device 1'

    const contact = new Contact()
    contact.id = '1'
    contact.givenName = 'Max'
    contact.familyName = 'Mustermann'
    contact.email = 'max@mustermann.mail'

    const date = DateTime.utc(2020, 1, 1, 0, 0, 0, 0)

    const platformMountAction1 = PlatformMountAction.createFromObject({
      id: '',
      platform: platform1,
      parentPlatform: null,
      date,
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0,
      contact,
      description: 'First mount'
    })

    const deviceMountAction1 = DeviceMountAction.createFromObject({
      id: '',
      device: device1,
      parentPlatform: platform1,
      date,
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0,
      contact,
      description: 'Mount device 1'
    })

    const deviceUnmountAction1 = DeviceUnmountAction.createFromObject({
      id: '',
      device: device1,
      date: DateTime.utc(2020, 2, 1),
      contact,
      description: 'Unmount of device 1'
    })

    const mountActionsStart = {
      platformMountActions: [platformMountAction1],
      platformUnmountActions: [],
      deviceMountActions: [deviceMountAction1],
      deviceUnmountActions: [deviceUnmountAction1]
    }

    const dateUnmount = DateTime.fromISO(date.toISO())

    // they are not really equal
    // but they must be equivalent
    expect(date).not.toEqual(dateUnmount)
    expect(dateTimesEqual(date, dateUnmount)).toBeTruthy()

    const mountActionsEnd = unmount(
      mountActionsStart,
      new PlatformNode(platformMountAction1),
      dateUnmount,
      contact,
      'unmount action for whole tree'
    )

    expect(mountActionsEnd.platformMountActions.length).toEqual(0)
    expect(mountActionsEnd.platformUnmountActions.length).toEqual(0)
    expect(mountActionsEnd.deviceMountActions.length).toEqual(0)
    expect(mountActionsEnd.deviceUnmountActions.length).toEqual(0)
  })
})
describe('getActivePlatforms', () => {
  it('should return an empty dict if there is no device mount action at all', () => {
    const mountActions = {
      platformMountActions: [],
      platformUnmountActions: [],
      deviceMountActions: [],
      deviceUnmountActions: []
    }
    const activePlatforms = getActivePlatforms(mountActions, DateTime.utc(2020, 1, 1))

    expect(Object.keys(activePlatforms).length).toEqual(0)
  })
  it('should return an empty dict if we ask for the tree before any mount action', () => {
    const platform1 = new Platform()
    platform1.id = '1'
    platform1.shortName = 'Platform 1'

    const contact = new Contact()
    contact.id = '1'
    contact.givenName = 'Max'
    contact.familyName = 'Mustermann'
    contact.email = 'max@mustermann.mail'

    const date = DateTime.utc(2020, 1, 1)

    const platformMountAction1 = PlatformMountAction.createFromObject({
      id: '',
      platform: platform1,
      parentPlatform: null,
      date,
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0,
      contact,
      description: 'First mount'
    })

    const mountActions = {
      platformMountActions: [platformMountAction1],
      platformUnmountActions: [],
      deviceMountActions: [],
      deviceUnmountActions: []
    }
    const activePlatformsEmpty = getActivePlatforms(mountActions, DateTime.utc(2019, 1, 1))

    expect(Object.keys(activePlatformsEmpty).length).toEqual(0)
  })
  it('should return a dict for the current mounts after the mount date', () => {
    const platform1 = new Platform()
    platform1.id = '1'
    platform1.shortName = 'Platform 1'

    const contact = new Contact()
    contact.id = '1'
    contact.givenName = 'Max'
    contact.familyName = 'Mustermann'
    contact.email = 'max@mustermann.mail'

    const date = DateTime.utc(2020, 1, 1)

    const platformMountAction1 = PlatformMountAction.createFromObject({
      id: '',
      platform: platform1,
      parentPlatform: null,
      date,
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0,
      contact,
      description: 'First mount'
    })

    const mountActions = {
      platformMountActions: [platformMountAction1],
      platformUnmountActions: [],
      deviceMountActions: [],
      deviceUnmountActions: []
    }
    const activePlatformsNotEmpty = getActivePlatforms(mountActions, DateTime.utc(2020, 1, 2))
    expect(Object.keys(activePlatformsNotEmpty).length).toEqual(1)
    expect(activePlatformsNotEmpty[platform1.id]).toEqual(platformMountAction1)
  })
  it('should return the latest mount action that is active', () => {
    const platform1 = new Platform()
    platform1.id = '1'
    platform1.shortName = 'Platform 1'

    const contact = new Contact()
    contact.id = '1'
    contact.givenName = 'Max'
    contact.familyName = 'Mustermann'
    contact.email = 'max@mustermann.mail'

    const platformMountAction1 = PlatformMountAction.createFromObject({
      id: '',
      platform: platform1,
      parentPlatform: null,
      date: DateTime.utc(2020, 1, 1),
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0,
      contact,
      description: 'First mount'
    })

    const platformUnmountAction1 = PlatformUnmountAction.createFromObject({
      id: '',
      platform: platform1,
      date: DateTime.utc(2020, 2, 1),
      contact,
      description: 'First unmount'
    })

    const platformMountAction2 = PlatformMountAction.createFromObject({
      id: '',
      platform: platform1,
      parentPlatform: null,
      date: DateTime.utc(2020, 3, 1),
      offsetX: 1,
      offsetY: 1,
      offsetZ: 1,
      contact,
      description: 'First remount'
    })

    const platformMountAction3 = PlatformMountAction.createFromObject({
      id: '',
      platform: platform1,
      parentPlatform: null,
      date: DateTime.utc(2020, 4, 1),
      offsetX: 2,
      offsetY: 2,
      offsetZ: 2,
      contact,
      description: 'Second remount'
    })

    const platformUnmountAction2 = PlatformUnmountAction.createFromObject({
      id: '',
      platform: platform1,
      date: DateTime.utc(2020, 5, 1),
      contact,
      description: 'Second unmount'
    })

    const mountActions = {
      platformMountActions: [platformMountAction1, platformMountAction3, platformMountAction2],
      platformUnmountActions: [platformUnmountAction1, platformUnmountAction2],
      deviceMountActions: [],
      deviceUnmountActions: []
    }
    const activePlatforms2019 = getActivePlatforms(mountActions, DateTime.utc(2019, 1, 1))
    expect(Object.keys(activePlatforms2019).length).toEqual(0)

    const activePlatforms2020Jan = getActivePlatforms(mountActions, DateTime.utc(2020, 1, 2))
    expect(Object.keys(activePlatforms2020Jan).length).toEqual(1)
    expect(activePlatforms2020Jan[platform1.id]).toEqual(platformMountAction1)
    const activePlatforms2020Feb = getActivePlatforms(mountActions, DateTime.utc(2020, 2, 2))
    expect(Object.keys(activePlatforms2020Feb).length).toEqual(0)
    const activePlatforms2020Mar = getActivePlatforms(mountActions, DateTime.utc(2020, 3, 2))
    expect(Object.keys(activePlatforms2020Mar).length).toEqual(1)
    expect(activePlatforms2020Mar[platform1.id]).toEqual(platformMountAction2)
    const activePlatforms2020Apr = getActivePlatforms(mountActions, DateTime.utc(2020, 4, 2))
    expect(Object.keys(activePlatforms2020Apr).length).toEqual(1)
    expect(activePlatforms2020Apr[platform1.id]).toEqual(platformMountAction3)
    const activePlatforms2020May = getActivePlatforms(mountActions, DateTime.utc(2020, 5, 2))
    expect(Object.keys(activePlatforms2020May).length).toEqual(0)
  })
  it('should just return an empty dict if there is just an unmount action', () => {
    const platform1 = new Platform()
    platform1.id = '1'
    platform1.shortName = 'Platform 1'

    const contact = new Contact()
    contact.id = '1'
    contact.givenName = 'Max'
    contact.familyName = 'Mustermann'
    contact.email = 'max@mustermann.mail'

    const platformUnmountAction1 = PlatformUnmountAction.createFromObject({
      id: '',
      platform: platform1,
      date: DateTime.utc(2020, 2, 1),
      contact,
      description: 'First unmount'
    })

    const mountActions = {
      platformMountActions: [],
      platformUnmountActions: [platformUnmountAction1],
      deviceMountActions: [],
      deviceUnmountActions: []
    }

    const activePlatforms = getActivePlatforms(mountActions, DateTime.utc(2020, 3, 1))
    expect(Object.keys(activePlatforms).length).toEqual(0)
  })
  it('a platform without an id can\'t be active', () => {
    const platform1 = new Platform()
    platform1.shortName = 'Platform 1'

    const contact = new Contact()
    contact.id = '1'
    contact.givenName = 'Max'
    contact.familyName = 'Mustermann'
    contact.email = 'max@mustermann.mail'

    const platformUnmountAction1 = PlatformUnmountAction.createFromObject({
      id: '',
      platform: platform1,
      date: DateTime.utc(2020, 2, 1),
      contact,
      description: 'First unmount'
    })

    const mountActions = {
      platformMountActions: [],
      platformUnmountActions: [platformUnmountAction1],
      deviceMountActions: [],
      deviceUnmountActions: []
    }

    const activePlatforms = getActivePlatforms(mountActions, DateTime.utc(2020, 3, 1))
    expect(Object.keys(activePlatforms).length).toEqual(0)
  })
  it('a platform without an id can\'t be active mounted', () => {
    const platform1 = new Platform()
    platform1.shortName = 'Platform 1'

    const contact = new Contact()
    contact.id = '1'
    contact.givenName = 'Max'
    contact.familyName = 'Mustermann'
    contact.email = 'max@mustermann.mail'

    const platformMountAction1 = PlatformMountAction.createFromObject({
      id: '',
      platform: platform1,
      parentPlatform: null,
      date: DateTime.utc(2020, 2, 1),
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0,
      contact,
      description: 'First unmount'
    })

    const mountActions = {
      platformMountActions: [platformMountAction1],
      platformUnmountActions: [],
      deviceMountActions: [],
      deviceUnmountActions: []
    }

    const activePlatforms = getActivePlatforms(mountActions, DateTime.utc(2020, 3, 1))
    expect(Object.keys(activePlatforms).length).toEqual(0)
  })
})
describe('getActiveDevices', () => {
  it('a device without an id can\'t be active', () => {
    const device1 = new Device()
    device1.shortName = 'Device 1'

    const contact = new Contact()
    contact.id = '1'
    contact.givenName = 'Max'
    contact.familyName = 'Mustermann'
    contact.email = 'max@mustermann.mail'

    const deviceUnmountAction1 = DeviceUnmountAction.createFromObject({
      id: '',
      device: device1,
      date: DateTime.utc(2020, 2, 1),
      contact,
      description: 'First unmount'
    })

    const mountActions = {
      platformMountActions: [],
      platformUnmountActions: [],
      deviceMountActions: [],
      deviceUnmountActions: [deviceUnmountAction1]
    }

    const activeDevices = getActiveDevices(mountActions, DateTime.utc(2020, 3, 1))
    expect(Object.keys(activeDevices).length).toEqual(0)
  })
  it('a device without an id can\'t be active mount', () => {
    const device1 = new Device()
    device1.shortName = 'Device 1'

    const contact = new Contact()
    contact.id = '1'
    contact.givenName = 'Max'
    contact.familyName = 'Mustermann'
    contact.email = 'max@mustermann.mail'

    const deviceMountAction1 = DeviceMountAction.createFromObject({
      id: '',
      device: device1,
      parentPlatform: null,
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0,
      date: DateTime.utc(2020, 2, 1),
      contact,
      description: 'First unmount'
    })

    const mountActions = {
      platformMountActions: [],
      platformUnmountActions: [],
      deviceMountActions: [deviceMountAction1],
      deviceUnmountActions: []
    }

    const activeDevices = getActiveDevices(mountActions, DateTime.utc(2020, 3, 1))
    expect(Object.keys(activeDevices).length).toEqual(0)
  })
  it('should just return an empty dict if there is just an unmount action', () => {
    const device1 = new Device()
    device1.id = '1'
    device1.shortName = 'Device 1'

    const contact = new Contact()
    contact.id = '1'
    contact.givenName = 'Max'
    contact.familyName = 'Mustermann'
    contact.email = 'max@mustermann.mail'

    const deviceUnmountAction1 = DeviceUnmountAction.createFromObject({
      id: '',
      device: device1,
      date: DateTime.utc(2020, 2, 1),
      contact,
      description: 'First unmount'
    })

    const mountActions = {
      platformMountActions: [],
      platformUnmountActions: [],
      deviceMountActions: [],
      deviceUnmountActions: [deviceUnmountAction1]
    }

    const activeDevices = getActiveDevices(mountActions, DateTime.utc(2020, 3, 1))
    expect(Object.keys(activeDevices).length).toEqual(0)
  })
  it('should return an empty dict after an unmount action', () => {
    const device1 = new Device()
    device1.id = '1'
    device1.shortName = 'Device 1'

    const contact = new Contact()
    contact.id = '1'
    contact.givenName = 'Max'
    contact.familyName = 'Mustermann'
    contact.email = 'max@mustermann.mail'

    const deviceMountAction = DeviceMountAction.createFromObject({
      id: '',
      device: device1,
      parentPlatform: null,
      date: DateTime.utc(2020, 1, 1),
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0,
      contact,
      description: 'First mount'
    })

    const deviceUnmountAction1 = DeviceUnmountAction.createFromObject({
      id: '',
      device: device1,
      date: DateTime.utc(2020, 2, 1),
      contact,
      description: 'First unmount'
    })

    const mountActions = {
      platformMountActions: [],
      platformUnmountActions: [],
      deviceMountActions: [deviceMountAction],
      deviceUnmountActions: [deviceUnmountAction1]
    }

    const activeDevices = getActiveDevices(mountActions, DateTime.utc(2020, 3, 1))
    expect(Object.keys(activeDevices).length).toEqual(0)
  })
  it('must work with multiple mount actions', () => {
    const device1 = new Device()
    device1.id = '1'
    device1.shortName = 'Device 1'

    const contact = new Contact()
    contact.id = '1'
    contact.givenName = 'Max'
    contact.familyName = 'Mustermann'
    contact.email = 'max@mustermann.mail'

    const deviceMountAction1 = DeviceMountAction.createFromObject({
      id: '',
      device: device1,
      parentPlatform: null,
      date: DateTime.utc(2020, 1, 1),
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0,
      contact,
      description: 'First mount'
    })

    const deviceMountAction2 = DeviceMountAction.createFromObject({
      id: '',
      device: device1,
      parentPlatform: null,
      date: DateTime.utc(2020, 1, 2),
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0,
      contact,
      description: 'Mount update'
    })

    const deviceMountAction3 = DeviceMountAction.createFromObject({
      id: '',
      device: device1,
      parentPlatform: null,
      date: DateTime.utc(2020, 2, 1),
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0,
      contact,
      description: 'Mount update'
    })

    const mountActions = {
      platformMountActions: [],
      platformUnmountActions: [],
      deviceMountActions: [deviceMountAction1, deviceMountAction3, deviceMountAction2],
      deviceUnmountActions: []
    }

    const activeDevices = getActiveDevices(mountActions, DateTime.utc(2020, 3, 1))
    expect(Object.keys(activeDevices).length).toEqual(1)
    expect(activeDevices[device1.id]).toEqual(deviceMountAction3)
  })
  it('must work with multiple unmount actions', () => {
    const device1 = new Device()
    device1.id = '1'
    device1.shortName = 'Device 1'

    const contact = new Contact()
    contact.id = '1'
    contact.givenName = 'Max'
    contact.familyName = 'Mustermann'
    contact.email = 'max@mustermann.mail'

    const deviceUnmountAction1 = DeviceUnmountAction.createFromObject({
      id: '',
      device: device1,
      date: DateTime.utc(2020, 1, 1),
      contact,
      description: 'First unmount'
    })

    const deviceUnmountAction2 = DeviceUnmountAction.createFromObject({
      id: '',
      device: device1,
      date: DateTime.utc(2020, 1, 2),
      contact,
      description: 'Unmount update'
    })

    const deviceUnmountAction3 = DeviceUnmountAction.createFromObject({
      id: '',
      device: device1,
      date: DateTime.utc(2020, 2, 1),
      contact,
      description: 'Ummount update II'
    })

    const mountActions = {
      platformMountActions: [],
      platformUnmountActions: [],
      deviceMountActions: [],
      deviceUnmountActions: [deviceUnmountAction1, deviceUnmountAction3, deviceUnmountAction2]
    }

    const activeDevices = getActiveDevices(mountActions, DateTime.utc(2020, 3, 1))
    expect(Object.keys(activeDevices).length).toEqual(0)
  })
})
describe('mountDevice', () => {
  it('should mount a device on the root if there is no parent', () => {
    const mountActionsStart = {
      platformMountActions: [],
      platformUnmountActions: [],
      deviceMountActions: [],
      deviceUnmountActions: []
    }
    const contact = new Contact()
    contact.id = '1'
    contact.givenName = 'Max'
    contact.familyName = 'Mustermann'
    contact.email = 'max@mustermann.mail'

    const device = new Device()
    device.id = '11'
    device.shortName = 'Device 1'

    const mountActionsAfterMount = mountDevice(
      mountActionsStart,
      device,
      0,
      0,
      0,
      contact,
      'First device mount',
      null,
      DateTime.utc(2020, 1, 1)
    )

    expect(mountActionsAfterMount.deviceMountActions.length).toEqual(1)
    const expectedMountAction = DeviceMountAction.createFromObject({
      id: '',
      device,
      parentPlatform: null,
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0,
      contact,
      date: DateTime.utc(2020, 1, 1),
      description: 'First device mount'
    })
    expect(mountActionsAfterMount.deviceMountActions[0]).toEqual(expectedMountAction)
  })
  it('must throw an error if we try to mount it on a device node', () => {
    const device1 = new Device()
    device1.id = '1'
    device1.shortName = 'Device 1'

    const device2 = new Device()
    device2.id = '2'
    device2.shortName = 'Device 2'

    const contact = new Contact()
    contact.id = '1'
    contact.givenName = 'Max'
    contact.familyName = 'Mustermann'
    contact.email = 'max@mustermann.mail'

    const deviceMountAction1 = DeviceMountAction.createFromObject({
      id: '',
      device: device1,
      parentPlatform: null,
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0,
      contact,
      description: 'First device mount',
      date: DateTime.utc(2020, 1, 1)
    })

    const mountActionsStart = {
      platformMountActions: [],
      platformUnmountActions: [],
      deviceMountActions: [deviceMountAction1],
      deviceUnmountActions: []
    }

    const parentNode = new DeviceNode(deviceMountAction1)

    const codeThatMustThrowAnException = () => {
      mountDevice(
        mountActionsStart,
        device2,
        0,
        0,
        0,
        contact,
        'Second device mount',
        parentNode,
        DateTime.utc(2020, 1, 1)
      )
    }
    expect(codeThatMustThrowAnException).toThrowError(/selected node-type cannot have children/)
  })
  it('should mount a device on a parent platform', () => {
    const device1 = new Device()
    device1.id = '1'
    device1.shortName = 'Device 1'

    const platform1 = new Platform()
    platform1.id = '11'
    platform1.shortName = 'Platform 1'

    const contact = new Contact()
    contact.id = '1'
    contact.givenName = 'Max'
    contact.familyName = 'Mustermann'
    contact.email = 'max@mustermann.mail'

    const platformMountAction1 = PlatformMountAction.createFromObject({
      id: '',
      platform: platform1,
      parentPlatform: null,
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0,
      contact,
      description: 'First device mount',
      date: DateTime.utc(2020, 1, 1)
    })

    const mountActionsStart = {
      platformMountActions: [platformMountAction1],
      platformUnmountActions: [],
      deviceMountActions: [],
      deviceUnmountActions: []
    }

    const parentNode = new PlatformNode(platformMountAction1)

    const mountActionsAfterMount = mountDevice(
      mountActionsStart,
      device1,
      0,
      0,
      0,
      contact,
      'First device mount',
      parentNode,
      DateTime.utc(2020, 1, 2)
    )

    expect(mountActionsAfterMount.deviceMountActions.length).toEqual(1)
    const expectedMountAction = DeviceMountAction.createFromObject({
      id: '',
      device: device1,
      parentPlatform: platform1,
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0,
      contact,
      date: DateTime.utc(2020, 1, 2),
      description: 'First device mount'
    })
    expect(mountActionsAfterMount.deviceMountActions[0]).toEqual(expectedMountAction)
  })
  it('should mount a device on the root if there is no parent', () => {
    const mountActionsStart = {
      platformMountActions: [],
      platformUnmountActions: [],
      deviceMountActions: [],
      deviceUnmountActions: []
    }
    const contact = new Contact()
    contact.id = '1'
    contact.givenName = 'Max'
    contact.familyName = 'Mustermann'
    contact.email = 'max@mustermann.mail'

    const device = new Device()
    device.id = '11'
    device.shortName = 'Device 1'

    const mountActionsAfterMount = mountDevice(
      mountActionsStart,
      device,
      0,
      0,
      0,
      contact,
      'First device mount',
      null,
      DateTime.utc(2020, 1, 1)
    )

    expect(mountActionsAfterMount.deviceMountActions.length).toEqual(1)
    const expectedMountAction = DeviceMountAction.createFromObject({
      id: '',
      device,
      parentPlatform: null,
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0,
      contact,
      date: DateTime.utc(2020, 1, 1),
      description: 'First device mount'
    })
    expect(mountActionsAfterMount.deviceMountActions[0]).toEqual(expectedMountAction)
  })
  it('must throw an error if we try to mount it on a device node', () => {
    const device1 = new Device()
    device1.id = '1'
    device1.shortName = 'Device 1'

    const device2 = new Device()
    device2.id = '2'
    device2.shortName = 'Device 2'

    const contact = new Contact()
    contact.id = '1'
    contact.givenName = 'Max'
    contact.familyName = 'Mustermann'
    contact.email = 'max@mustermann.mail'

    const deviceMountAction1 = DeviceMountAction.createFromObject({
      id: '',
      device: device1,
      parentPlatform: null,
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0,
      contact,
      description: 'First device mount',
      date: DateTime.utc(2020, 1, 1)
    })

    const mountActionsStart = {
      platformMountActions: [],
      platformUnmountActions: [],
      deviceMountActions: [deviceMountAction1],
      deviceUnmountActions: []
    }

    const parentNode = new DeviceNode(deviceMountAction1)

    const codeThatMustThrowAnException = () => {
      mountDevice(
        mountActionsStart,
        device2,
        0,
        0,
        0,
        contact,
        'Second device mount',
        parentNode,
        DateTime.utc(2020, 1, 1)
      )
    }

    expect(codeThatMustThrowAnException).toThrowError(/selected node-type cannot have children/)
  })
  it('should mount a device on a parent platform', () => {
    const device1 = new Device()
    device1.id = '1'
    device1.shortName = 'Device 1'

    const platform1 = new Platform()
    platform1.id = '11'
    platform1.shortName = 'Platform 1'

    const contact = new Contact()
    contact.id = '1'
    contact.givenName = 'Max'
    contact.familyName = 'Mustermann'
    contact.email = 'max@mustermann.mail'

    const platformMountAction1 = PlatformMountAction.createFromObject({
      id: '',
      platform: platform1,
      parentPlatform: null,
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0,
      contact,
      description: 'First platform mount',
      date: DateTime.utc(2020, 1, 1)
    })

    const mountActionsStart = {
      platformMountActions: [platformMountAction1],
      platformUnmountActions: [],
      deviceMountActions: [],
      deviceUnmountActions: []
    }

    const parentNode = new PlatformNode(platformMountAction1)

    const mountActionsAfterMount = mountDevice(
      mountActionsStart,
      device1,
      0,
      0,
      0,
      contact,
      'First device mount',
      parentNode,
      DateTime.utc(2020, 1, 2)
    )

    expect(mountActionsAfterMount.deviceMountActions.length).toEqual(1)
    const expectedMountAction = DeviceMountAction.createFromObject({
      id: '',
      device: device1,
      parentPlatform: platform1,
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0,
      contact,
      date: DateTime.utc(2020, 1, 2),
      description: 'First device mount'
    })
    expect(mountActionsAfterMount.deviceMountActions[0]).toEqual(expectedMountAction)
  })
})
describe('mountPlatform', () => {
  it('should mount a platform on the root if there is no parent', () => {
    const mountActionsStart = {
      platformMountActions: [],
      platformUnmountActions: [],
      deviceMountActions: [],
      deviceUnmountActions: []
    }
    const contact = new Contact()
    contact.id = '1'
    contact.givenName = 'Max'
    contact.familyName = 'Mustermann'
    contact.email = 'max@mustermann.mail'

    const platform = new Platform()
    platform.id = '11'
    platform.shortName = 'Platform 1'

    const mountActionsAfterMount = mountPlatform(
      mountActionsStart,
      platform,
      0,
      0,
      0,
      contact,
      'First platform mount',
      null,
      DateTime.utc(2020, 1, 1)
    )

    expect(mountActionsAfterMount.platformMountActions.length).toEqual(1)
    const expectedMountAction = PlatformMountAction.createFromObject({
      id: '',
      platform,
      parentPlatform: null,
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0,
      contact,
      date: DateTime.utc(2020, 1, 1),
      description: 'First platform mount'
    })
    expect(mountActionsAfterMount.platformMountActions[0]).toEqual(expectedMountAction)
  })
  it('must throw an error if we try to mount it on a device node', () => {
    const device1 = new Device()
    device1.id = '1'
    device1.shortName = 'Device 1'

    const platform1 = new Platform()
    platform1.id = '11'
    platform1.shortName = 'Platform 1'

    const contact = new Contact()
    contact.id = '1'
    contact.givenName = 'Max'
    contact.familyName = 'Mustermann'
    contact.email = 'max@mustermann.mail'

    const deviceMountAction1 = DeviceMountAction.createFromObject({
      id: '',
      device: device1,
      parentPlatform: null,
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0,
      contact,
      description: 'First device mount',
      date: DateTime.utc(2020, 1, 1)
    })

    const mountActionsStart = {
      platformMountActions: [],
      platformUnmountActions: [],
      deviceMountActions: [deviceMountAction1],
      deviceUnmountActions: []
    }

    const parentNode = new DeviceNode(deviceMountAction1)

    const codeThatMustThrowAnException = () => {
      mountPlatform(
        mountActionsStart,
        platform1,
        0,
        0,
        0,
        contact,
        'Second platform mount',
        parentNode,
        DateTime.utc(2020, 1, 1)
      )
    }

    expect(codeThatMustThrowAnException).toThrowError(/selected node-type cannot have children/)
  })
  it('should mount a platform on a parent platform', () => {
    const platform1 = new Platform()
    platform1.id = '11'
    platform1.shortName = 'Platform 1'

    const platform2 = new Platform()
    platform2.id = '22'
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
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0,
      contact,
      description: 'First platform mount',
      date: DateTime.utc(2020, 1, 1)
    })

    const mountActionsStart = {
      platformMountActions: [platformMountAction1],
      platformUnmountActions: [],
      deviceMountActions: [],
      deviceUnmountActions: []
    }

    const parentNode = new PlatformNode(platformMountAction1)

    const mountActionsAfterMount = mountPlatform(
      mountActionsStart,
      platform2,
      0,
      0,
      0,
      contact,
      'Second platform mount',
      parentNode,
      DateTime.utc(2020, 1, 2)
    )

    expect(mountActionsAfterMount.platformMountActions.length).toEqual(2)
    const expectedMountAction = PlatformMountAction.createFromObject({
      id: '',
      platform: platform2,
      parentPlatform: platform1,
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0,
      contact,
      date: DateTime.utc(2020, 1, 2),
      description: 'Second platform mount'
    })
    expect(mountActionsAfterMount.platformMountActions[0]).toEqual(platformMountAction1)
    expect(mountActionsAfterMount.platformMountActions[1]).toEqual(expectedMountAction)
  })
})
