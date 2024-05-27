/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2023
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Tobias Kuhnert <tobias.kuhnert@ufz.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 * - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */

import { DateTime } from 'luxon'

import { MountActionValidationResult, MountActionValidator } from '@/utils/MountActionValidator'

import { PlatformMountAction } from '@/models/PlatformMountAction'
import { Platform } from '@/models/Platform'
import { Contact } from '@/models/Contact'
import { MountAction } from '@/models/MountAction'

import { ConfigurationsTree } from '@/viewmodels/ConfigurationsTree'
import { PlatformNode } from '@/viewmodels/PlatformNode'
import { Availability } from '@/models/Availability'
import { DeviceProperty } from '@/models/DeviceProperty'
import { Device } from '@/models/Device'
import { DeviceMountAction } from '@/models/DeviceMountAction'
import { DynamicLocationAction } from '@/models/DynamicLocationAction'

describe('#actionConflictsWith', () => {
  it('should return an error if start date is before the start date of the parent', () => {
    const parentPlatform = new Platform()
    const mountAction = new MountAction(
      '3',
      parentPlatform,
      DateTime.fromISO('2022-08-31T10:00:00'), // < error
      DateTime.fromISO('2022-09-08T10:00:00'),
      0,
      0,
      0,
      '',
      null,
      null,
      null,
      '',
      '',
      new Contact(),
      new Contact(),
      'Start of mount',
      'End of mount'
    )

    const parentAction = new MountAction(
      '1',
      null,
      DateTime.fromISO('2022-09-01T10:00:00'), // <
      DateTime.fromISO('2022-09-30T10:00:00'),
      0,
      0,
      0,
      '',
      null,
      null,
      null,
      '',
      '',
      new Contact(),
      new Contact(),
      'Start of mount',
      'End of mount'
    )

    // we expect an error
    expect(MountActionValidator.actionConflictsWith(mountAction, parentAction)).toBeInstanceOf(MountActionValidationResult)
  })
  it('should return an error if start date is after the end date of the parent', () => {
    const parentPlatform = new Platform()
    const mountAction = new MountAction(
      '3',
      parentPlatform,
      DateTime.fromISO('2022-08-01T10:00:00'), // < error
      DateTime.fromISO('2022-08-31T10:00:00'),
      0,
      0,
      0,
      '',
      null,
      null,
      null,
      '',
      '',
      new Contact(),
      new Contact(),
      'Start of mount',
      'End of mount'
    )

    const parentAction = new MountAction(
      '1',
      null,
      DateTime.fromISO('2022-07-01T10:00:00'),
      DateTime.fromISO('2022-07-31T10:00:00'), // <
      0,
      0,
      0,
      '',
      null,
      null,
      null,
      '',
      '',
      new Contact(),
      new Contact(),
      'Start of mount',
      'End of mount'
    )

    // we expect an error
    expect(MountActionValidator.actionConflictsWith(mountAction, parentAction)).toBeInstanceOf(MountActionValidationResult)
  })
  it('should return an error if end date is before the start date of the parent', () => {
    const parentPlatform = new Platform()
    const mountAction = new MountAction(
      '3',
      parentPlatform,
      DateTime.fromISO('2022-07-01T10:00:00'),
      DateTime.fromISO('2022-07-31T10:00:00'), // < error
      0,
      0,
      0,
      '',
      null,
      null,
      null,
      '',
      '',
      new Contact(),
      new Contact(),
      'Start of mount',
      'End of mount'
    )

    const parentAction = new MountAction(
      '1',
      null,
      DateTime.fromISO('2022-08-01T10:00:00'), // <
      DateTime.fromISO('2022-08-31T10:00:00'),
      0,
      0,
      0,
      '',
      null,
      null,
      null,
      '',
      '',
      new Contact(),
      new Contact(),
      'Start of mount',
      'End of mount'
    )

    // we expect an error
    expect(MountActionValidator.actionConflictsWith(mountAction, parentAction)).toBeInstanceOf(MountActionValidationResult)
  })
  it('should return an error if end date is after the end date of parent', () => {
    const parentPlatform = new Platform()
    const mountAction = new MountAction(
      '3',
      parentPlatform,
      DateTime.fromISO('2022-08-01T10:00:00'),
      DateTime.fromISO('2022-08-31T10:00:00'), // < error
      0,
      0,
      0,
      '',
      null,
      null,
      null,
      '',
      '',
      new Contact(),
      new Contact(),
      'Start of mount',
      'End of mount'
    )

    const parentAction = new MountAction(
      '1',
      null,
      DateTime.fromISO('2022-08-01T10:00:00'),
      DateTime.fromISO('2022-08-15T10:00:00'), // <
      0,
      0,
      0,
      '',
      null,
      null,
      null,
      '',
      '',
      new Contact(),
      new Contact(),
      'Start of mount',
      'End of mount'
    )

    // we expect an error
    expect(MountActionValidator.actionConflictsWith(mountAction, parentAction)).toBeInstanceOf(MountActionValidationResult)
  })
  it('should return an error if open end but parent has an end date', () => {
    const parentPlatform = new Platform()
    const mountAction = new MountAction(
      '3',
      parentPlatform,
      DateTime.fromISO('2022-08-02T10:00:00'),
      null, // < error
      0,
      0,
      0,
      '',
      null,
      null,
      null,
      '',
      '',
      new Contact(),
      null,
      'Start of mount',
      null
    )

    const parentAction = new MountAction(
      '1',
      null,
      DateTime.fromISO('2022-08-01T10:00:00'),
      DateTime.fromISO('2022-08-31T10:00:00'), // <
      0,
      0,
      0,
      '',
      null,
      null,
      null,
      '',
      '',
      new Contact(),
      new Contact(),
      'Start of mount',
      'End of mount'
    )

    // we expect an error
    expect(MountActionValidator.actionConflictsWith(mountAction, parentAction)).toBeInstanceOf(MountActionValidationResult)
  })
  it('should not return an error if time range is in parent time range', () => {
    const parentPlatform = new Platform()
    const mountAction = new MountAction(
      '3',
      parentPlatform,
      DateTime.fromISO('2022-08-12T10:00:00'),
      DateTime.fromISO('2022-08-21T10:00:00'),
      0,
      0,
      0,
      '',
      null,
      null,
      null,
      '',
      '',
      new Contact(),
      new Contact(),
      'Start of mount',
      'End of mount'
    )

    const parentAction = new MountAction(
      '1',
      null,
      DateTime.fromISO('2022-08-01T10:00:00'),
      DateTime.fromISO('2022-08-31T10:00:00'),
      0,
      0,
      0,
      '',
      null,
      null,
      null,
      '',
      '',
      new Contact(),
      new Contact(),
      'Start of mount',
      'End of mount'
    )

    // we expect no error
    expect(typeof MountActionValidator.actionConflictsWith(mountAction, parentAction)).toBe('boolean')
    expect(MountActionValidator.actionConflictsWith(mountAction, parentAction)).toBe(false)
  })
})
describe('#actionConflictsWithMultiple', () => {
  it('should return an error if one action is not within the parent time range', () => {
    // we don't need to test every case as #actionConflictsWithMultiple calls
    // #actionIsWithinParentRage for each action provided
    const parentPlatform = new Platform()
    const mountActions: MountAction[] = [
      new MountAction(
        '3',
        parentPlatform,
        DateTime.fromISO('2022-08-12T10:00:00'),
        DateTime.fromISO('2022-08-21T10:00:00'),
        0,
        0,
        0,
        '',
        null,
        null,
        null,
        '',
        '',
        new Contact(),
        new Contact(),
        'Start of mount',
        'End of mount'
      ),
      new MountAction(
        '4',
        parentPlatform,
        DateTime.fromISO('2022-07-31T10:00:00'), // < error
        DateTime.fromISO('2022-08-21T10:00:00'),
        0,
        0,
        0,
        '',
        null,
        null,
        null,
        '',
        '',
        new Contact(),
        new Contact(),
        'Start of mount',
        'End of mount'
      ),
      new MountAction(
        '5',
        parentPlatform,
        DateTime.fromISO('2022-08-02T10:00:00'),
        DateTime.fromISO('2022-08-30T10:00:00'),
        0,
        0,
        0,
        '',
        null,
        null,
        null,
        '',
        '',
        new Contact(),
        new Contact(),
        'Start of mount',
        'End of mount'
      )
    ]

    const parentAction = new MountAction(
      '1',
      null,
      DateTime.fromISO('2022-08-01T10:00:00'),
      DateTime.fromISO('2022-08-31T10:00:00'),
      0,
      0,
      0,
      '',
      null,
      null,
      null,
      '',
      '',
      new Contact(),
      new Contact(),
      'Start of mount',
      'End of mount'
    )

    // we expect an error
    expect(MountActionValidator.actionConflictsWithMultiple(parentAction, mountActions)).toBeInstanceOf(MountActionValidationResult)
  })
  it('should not return an error if all actions are within the parent time range', () => {
    const parentPlatform = new Platform()
    const mountActions: MountAction[] = [
      new MountAction(
        '3',
        parentPlatform,
        DateTime.fromISO('2022-08-12T10:00:00'),
        DateTime.fromISO('2022-08-21T10:00:00'),
        0,
        0,
        0,
        '',
        null,
        null,
        null,
        '',
        '',
        new Contact(),
        new Contact(),
        'Start of mount',
        'End of mount'
      ),
      new MountAction(
        '4',
        parentPlatform,
        DateTime.fromISO('2022-08-09T10:00:00'),
        DateTime.fromISO('2022-08-10T10:00:00'),
        0,
        0,
        0,
        '',
        null,
        null,
        null,
        '',
        '',
        new Contact(),
        new Contact(),
        'Start of mount',
        'End of mount'
      ),
      new MountAction(
        '5',
        parentPlatform,
        DateTime.fromISO('2022-08-02T10:00:00'),
        DateTime.fromISO('2022-08-30T10:00:00'),
        0,
        0,
        0,
        '',
        null,
        null,
        null,
        '',
        '',
        new Contact(),
        new Contact(),
        'Start of mount',
        'End of mount'
      )
    ]

    const parentAction = new MountAction(
      '1',
      null,
      DateTime.fromISO('2022-08-01T10:00:00'),
      DateTime.fromISO('2022-08-31T10:00:00'),
      0,
      0,
      0,
      '',
      null,
      null,
      null,
      '',
      '',
      new Contact(),
      new Contact(),
      'Start of mount',
      'End of mount'
    )

    // we expect no error
    expect(typeof MountActionValidator.actionConflictsWithMultiple(parentAction, mountActions)).toBe('boolean')
    expect(MountActionValidator.actionConflictsWithMultiple(parentAction, mountActions)).toBe(false)
  })
})
describe('#nodeIsWithinParentRange', () => {
  it('should return an error if the timerange of a node is not within the timerange of its parent node', () => {
    // we don't need to test every case as #nodeIsWithinParentRange calls
    // #actionIsWithinParentRage for the node and its parent
    const parentPlatform = new Platform()
    const platform = new Platform()

    const mountAction = new PlatformMountAction(
      '3',
      platform,
      parentPlatform,
      DateTime.fromISO('2022-08-31T10:00:00'), // < error
      DateTime.fromISO('2022-09-08T10:00:00'),
      0,
      0,
      0,
      '',
      null,
      null,
      null,
      '',
      '',
      new Contact(),
      new Contact(),
      'Start of mount',
      'End of mount'
    )
    const node = new PlatformNode(mountAction)

    const parentAction = new PlatformMountAction(
      '1',
      parentPlatform,
      null,
      DateTime.fromISO('2022-09-01T10:00:00'), // <
      DateTime.fromISO('2022-09-30T10:00:00'),
      0,
      0,
      0,
      '',
      null,
      null,
      null,
      '',
      '',
      new Contact(),
      new Contact(),
      'Start of mount',
      'End of mount'
    )
    const parentNode = new PlatformNode(parentAction)
    parentNode.children = [node]

    const tree = ConfigurationsTree.fromArray([parentNode])
    const validator = new MountActionValidator(tree)

    // we expect an error
    expect(validator.nodeIsWithinParentRange(node)).toBeInstanceOf(MountActionValidationResult)
  })
  it('should return true if the timerange of a node is within the timerange of its parent node', () => {
    const parentPlatform = new Platform()
    const platform = new Platform()

    const mountAction = new PlatformMountAction(
      '3',
      platform,
      parentPlatform,
      DateTime.fromISO('2022-09-15T10:00:00'),
      DateTime.fromISO('2022-09-17T10:00:00'),
      0,
      0,
      0,
      '',
      null,
      null,
      null,
      '',
      '',
      new Contact(),
      new Contact(),
      'Start of mount',
      'End of mount'
    )
    const node = new PlatformNode(mountAction)

    const parentAction = new PlatformMountAction(
      '1',
      parentPlatform,
      null,
      DateTime.fromISO('2022-09-14T10:00:00'),
      DateTime.fromISO('2022-09-18T10:00:00'),
      0,
      0,
      0,
      '',
      null,
      null,
      null,
      '',
      '',
      new Contact(),
      new Contact(),
      'Start of mount',
      'End of mount'
    )
    const parentNode = new PlatformNode(parentAction)
    parentNode.children = [node]

    const tree = ConfigurationsTree.fromArray([parentNode])
    const validator = new MountActionValidator(tree)

    // we expect no error
    expect(typeof validator.nodeIsWithinParentRange(node)).toBe('boolean')
    expect(validator.nodeIsWithinParentRange(node)).toBe(true)
  })
})
describe('#nodeChildrenAreWithinRange', () => {
  it('should return an error if the timerange of one of a nodes children is not within the timerange of its parent', () => {
    const parentPlatform = new Platform()
    const platform = new Platform()
    const anotherPlatform = new Platform()

    const mountAction = new PlatformMountAction(
      '3',
      platform,
      parentPlatform,
      DateTime.fromISO('2022-09-15T10:00:00'),
      DateTime.fromISO('2022-09-20T10:00:00'),
      0,
      0,
      0,
      '',
      null,
      null,
      null,
      '',
      '',
      new Contact(),
      new Contact(),
      'Start of mount',
      'End of mount'
    )
    const node = new PlatformNode(mountAction)

    const anotherMountAction = new PlatformMountAction(
      '4',
      anotherPlatform,
      platform,
      DateTime.fromISO('2022-08-31T10:00:00'), // < error
      DateTime.fromISO('2022-09-08T10:00:00'),
      0,
      0,
      0,
      '',
      null,
      null,
      null,
      '',
      '',
      new Contact(),
      new Contact(),
      'Start of mount',
      'End of mount'
    )
    const anotherNode = new PlatformNode(anotherMountAction)
    node.children = [anotherNode]

    const parentAction = new PlatformMountAction(
      '1',
      parentPlatform,
      null,
      DateTime.fromISO('2022-09-01T10:00:00'), // <
      DateTime.fromISO('2022-09-30T10:00:00'),
      0,
      0,
      0,
      '',
      null,
      null,
      null,
      '',
      '',
      new Contact(),
      new Contact(),
      'Start of mount',
      'End of mount'
    )
    const parentNode = new PlatformNode(parentAction)
    parentNode.children = [node]

    const tree = ConfigurationsTree.fromArray([parentNode])
    const validator = new MountActionValidator(tree)

    // we expect an error no matter what level the faulty child is on
    expect(validator.nodeChildrenAreWithinRange(parentNode)).toBeInstanceOf(MountActionValidationResult)
    expect(validator.nodeChildrenAreWithinRange(node)).toBeInstanceOf(MountActionValidationResult)
  })
  it('should return true if the timeranges of all children of a node are within the timerange of this node', () => {
    const parentPlatform = new Platform()
    const platform = new Platform()
    const anotherPlatform = new Platform()

    const mountAction = new PlatformMountAction(
      '3',
      platform,
      parentPlatform,
      DateTime.fromISO('2022-09-15T10:00:00'),
      DateTime.fromISO('2022-09-20T10:00:00'),
      0,
      0,
      0,
      '',
      null,
      null,
      null,
      '',
      '',
      new Contact(),
      new Contact(),
      'Start of mount',
      'End of mount'
    )
    const node = new PlatformNode(mountAction)

    const anotherMountAction = new PlatformMountAction(
      '4',
      anotherPlatform,
      platform,
      DateTime.fromISO('2022-09-15T20:00:00'),
      DateTime.fromISO('2022-09-19T08:00:00'),
      0,
      0,
      0,
      '',
      null,
      null,
      null,
      '',
      '',
      new Contact(),
      new Contact(),
      'Start of mount',
      'End of mount'
    )
    const anotherNode = new PlatformNode(anotherMountAction)
    node.children = [anotherNode]

    const parentAction = new PlatformMountAction(
      '1',
      parentPlatform,
      null,
      DateTime.fromISO('2022-09-01T10:00:00'),
      DateTime.fromISO('2022-09-30T10:00:00'),
      0,
      0,
      0,
      '',
      null,
      null,
      null,
      '',
      '',
      new Contact(),
      new Contact(),
      'Start of mount',
      'End of mount'
    )
    const parentNode = new PlatformNode(parentAction)
    parentNode.children = [node]

    const tree = ConfigurationsTree.fromArray([parentNode])
    const validator = new MountActionValidator(tree)

    // we expect no error for each parent node of the tree
    expect(typeof validator.nodeChildrenAreWithinRange(parentNode)).toBe('boolean')
    expect(validator.nodeChildrenAreWithinRange(parentNode)).toBe(true)
    expect(typeof validator.nodeChildrenAreWithinRange(node)).toBe('boolean')
    expect(validator.nodeChildrenAreWithinRange(node)).toBe(true)
  })
})
const failingMountActions: [string, MountAction][] = [
  ['begins before and ends within', new MountAction(
    '1',
    null,
    DateTime.fromISO('2022-08-21T08:00:00'),
    DateTime.fromISO('2022-09-15T08:00:00'),
    0,
    0,
    0,
    '',
    null,
    null,
    null,
    '',
    '',
    new Contact(),
    new Contact(),
    'begin of mount',
    'end of mount'
  )],
  ['begins and ends within', new MountAction(
    '1',
    null,
    DateTime.fromISO('2022-09-02T08:00:00'),
    DateTime.fromISO('2022-09-15T08:00:00'),
    0,
    0,
    0,
    '',
    null,
    null,
    null,
    '',
    '',
    new Contact(),
    new Contact(),
    'begin of mount',
    'end of mount'
  )],
  ['begins within and ends after', new MountAction(
    '1',
    null,
    DateTime.fromISO('2022-09-15T08:00:00'),
    DateTime.fromISO('2022-10-01T08:00:00'),
    0,
    0,
    0,
    '',
    null,
    null,
    null,
    '',
    '',
    new Contact(),
    new Contact(),
    'begin of mount',
    'end of mount'
  )],
  ['begins before and ends after', new MountAction(
    '1',
    null,
    DateTime.fromISO('2022-08-31T08:00:00'),
    DateTime.fromISO('2022-10-01T08:00:00'),
    0,
    0,
    0,
    '',
    null,
    null,
    null,
    '',
    '',
    new Contact(),
    new Contact(),
    'begin of mount',
    'end of mount'
  )],
  ['has no end date and begins before', new MountAction(
    '1',
    null,
    DateTime.fromISO('2022-08-31T08:00:00'),
    null,
    0,
    0,
    0,
    '',
    null,
    null,
    null,
    '',
    '',
    new Contact(),
    new Contact(),
    'begin of mount',
    'end of mount'
  )]
]
const availabilities: Availability[] = [
  (() => {
    const a = new Availability()
    a.available = false
    a.beginDate = DateTime.fromISO('2022-09-01T10:00:00')
    a.endDate = DateTime.fromISO('2022-09-30T10:00:00')
    return a
  })()
]
describe.each(failingMountActions)('#actionAvailableIn', (description, mountAction) => {
  it(`should return an error if the timerange of a mount action ${description} the timerange of a non-availability`, () => {
    // we expect an error
    expect(MountActionValidator.actionAvailableIn(mountAction, availabilities)).toBeInstanceOf(MountActionValidationResult)
  })
})
describe('#isDevicePropertyUsedInDynamicLocationAction', () => {
  it('should return true, when a device property of a device mount action is used within a dynamic location', () => {
    const property = new DeviceProperty()
    property.id = '1'

    const device = new Device()
    device.properties.push(property)

    const mountAction = new DeviceMountAction(
      '1',
      device,
      null,
      null,
      DateTime.utc(),
      null,
      0,
      0,
      0,
      '',
      null,
      null,
      null,
      '',
      '',
      new Contact(),
      null,
      '',
      null
    )

    const locationAction = new DynamicLocationAction()
    locationAction.x = null
    locationAction.y = property
    locationAction.z = null

    expect(MountActionValidator.isDevicePropertyUsedInDynamicLocationAction(mountAction, locationAction)).toBe(true)
  })
  it('should return false, when a device property of a device mount action is not used within a dynamic location', () => {
    const property1 = new DeviceProperty()
    property1.id = '1'

    const property2 = new DeviceProperty()
    property2.id = '2'

    const device = new Device()
    device.properties.push(property1)

    const mountAction = new DeviceMountAction(
      '1',
      device,
      null,
      null,
      DateTime.utc(),
      null,
      0,
      0,
      0,
      '',
      null,
      null,
      null,
      '',
      '',
      new Contact(),
      null,
      '',
      null
    )

    const locationAction = new DynamicLocationAction()
    locationAction.x = null
    locationAction.y = property2
    locationAction.z = null

    expect(MountActionValidator.isDevicePropertyUsedInDynamicLocationAction(mountAction, locationAction)).toBe(false)
  })
})
describe('#getRelatedDynamicLocationActions', () => {
  it('should return all dynamic location actions, that use the device property of the device of a device mount action and are within the timerange of the mount action', () => {
    const property1 = new DeviceProperty()
    property1.id = '1'

    const property2 = new DeviceProperty()
    property2.id = '2'

    const device = new Device()
    device.properties.push(property1)

    const mountAction = new DeviceMountAction(
      '1',
      device,
      null,
      null,
      DateTime.fromISO('2022-10-01T10:00:00'),
      DateTime.fromISO('2022-10-20T10:00:00'),
      0,
      0,
      0,
      '',
      null,
      null,
      null,
      '',
      '',
      new Contact(),
      new Contact(),
      '',
      ''
    )

    // uses a property, inside the timerange
    const locationAction1 = new DynamicLocationAction()
    locationAction1.beginDate = DateTime.fromISO('2022-10-02T10:00:00')
    locationAction1.endDate = DateTime.fromISO('2022-10-05T10:00:00')
    locationAction1.x = null
    locationAction1.y = property1
    locationAction1.z = null

    // uses a property, inside the timerange, too
    const locationAction2 = new DynamicLocationAction()
    locationAction2.beginDate = DateTime.fromISO('2022-10-19T10:00:00')
    locationAction2.endDate = DateTime.fromISO('2022-10-20T10:00:00')
    locationAction2.x = null
    locationAction2.y = property1
    locationAction2.z = null

    // uses a property, outside the timerange
    const locationAction3 = new DynamicLocationAction()
    locationAction3.beginDate = DateTime.fromISO('2022-11-03T10:00:00')
    locationAction3.endDate = DateTime.fromISO('2022-11-11T10:00:00')
    locationAction3.x = null
    locationAction3.y = property1
    locationAction3.z = null

    // does not use a property, inside the timerange
    const locationAction4 = new DynamicLocationAction()
    locationAction4.beginDate = DateTime.fromISO('2022-10-03T10:00:00')
    locationAction4.endDate = DateTime.fromISO('2022-10-11T10:00:00')
    locationAction4.x = null
    locationAction4.y = property2
    locationAction4.z = null

    const locationActions = [
      locationAction1,
      locationAction2,
      locationAction3,
      locationAction4
    ]

    const result = MountActionValidator.getRelatedDynamicLocationActions(mountAction, locationActions)
    expect(result).toHaveLength(2)
    expect(result[0]).toBe(locationAction1)
    expect(result[1]).toBe(locationAction2)
  })
})
