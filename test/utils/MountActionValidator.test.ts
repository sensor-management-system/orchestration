/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020 - 2022
 * - Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
 * - Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
 * - Tobias Kuhnert (UFZ, tobias.kuhnert@ufz.de)
* - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences
 *   (GFZ, https://www.gfz-potsdam.de)
 * - Helmholtz Centre for Environmental Research GmbH - UFZ
 *   (UFZ, https://www.ufz.de)
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

import { MountActionValidationResult, MountActionValidator } from '@/utils/MountActionValidator'

import { PlatformMountAction } from '@/models/PlatformMountAction'
import { Platform } from '@/models/Platform'
import { Contact } from '@/models/Contact'
import { MountAction } from '@/models/MountAction'

import { ConfigurationsTree } from '@/viewmodels/ConfigurationsTree'
import { PlatformNode } from '@/viewmodels/PlatformNode'
import { Availability } from '@/models/Availability'

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
      new Contact(),
      new Contact(),
      'Start of mount',
      'End of mount'
    )

    // we expect no error
    expect(typeof MountActionValidator.actionConflictsWith(mountAction, parentAction)).toBe('boolean')
    expect(MountActionValidator.actionConflictsWith(mountAction, parentAction)).toBe(true)
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
      new Contact(),
      new Contact(),
      'Start of mount',
      'End of mount'
    )

    // we expect no error
    expect(typeof MountActionValidator.actionConflictsWithMultiple(parentAction, mountActions)).toBe('boolean')
    expect(MountActionValidator.actionConflictsWithMultiple(parentAction, mountActions)).toBe(true)
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
