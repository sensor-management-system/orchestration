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
import { DeviceMountTimelineAction, DeviceUnmountTimelineAction, PlatformMountTimelineAction, PlatformUnmountTimelineAction } from '@/utils/configurationInterfaces'
import { Device } from '@/models/Device'
import { DeviceMountAction } from '@/models/DeviceMountAction'

describe('logicOrder', () => {
  it('should have lower values for mounts then for unmounts', () => {
    // Background here is that we want to use it together with a sorting by date
    // so that the oldest entry is last.
    // Second criteria here is the logicOrder.
    // Used with hightestFirst setting, we can make sure
    // our unmounts are before the mounts in this list (as they have higher logic order values).
    const contact = new Contact()
    const platform = new Platform()
    const device = new Device()

    const platformMount = new PlatformMountAction(
      '1',
      platform,
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
      contact,
      null,
      '',
      null,
      ''
    )
    const deviceMountAction = new DeviceMountAction(
      '2',
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
      contact,
      null,
      '',
      null,
      ''
    )

    const platformMountTimelineAction = new PlatformMountTimelineAction(platformMount)
    const platformUnmountTimelineAction = new PlatformUnmountTimelineAction(platformMount)

    expect(platformMountTimelineAction.logicOrder).toBeLessThan(platformUnmountTimelineAction.logicOrder)

    const deviceMountTimelineAction = new DeviceMountTimelineAction(deviceMountAction)
    const deviceUnmountTimelineAction = new DeviceUnmountTimelineAction(deviceMountAction)

    expect(deviceMountTimelineAction.logicOrder).toBeLessThan(deviceUnmountTimelineAction.logicOrder)
  })
  it('should have lower values for platform mounts then for device mounts', () => {
    const contact = new Contact()
    const platform = new Platform()
    const device = new Device()

    const platformMount = new PlatformMountAction(
      '1',
      platform,
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
      contact,
      null,
      '',
      null,
      ''
    )
    const deviceMountAction = new DeviceMountAction(
      '2',
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
      contact,
      null,
      '',
      null,
      ''
    )

    const platformMountTimelineAction = new PlatformMountTimelineAction(platformMount)

    const deviceMountTimelineAction = new DeviceMountTimelineAction(deviceMountAction)

    expect(platformMountTimelineAction.logicOrder).toBeLessThan(deviceMountTimelineAction.logicOrder)
  })
  it('should have lower values for device unmounts then for platform unmounts', () => {
    const contact = new Contact()
    const platform = new Platform()
    const device = new Device()

    const platformMount = new PlatformMountAction(
      '1',
      platform,
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
      contact,
      null,
      '',
      null,
      ''
    )
    const deviceMountAction = new DeviceMountAction(
      '2',
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
      contact,
      null,
      '',
      null,
      ''
    )

    const platformUnmountTimelineAction = new PlatformUnmountTimelineAction(platformMount)

    const deviceUnmountTimelineAction = new DeviceUnmountTimelineAction(deviceMountAction)

    expect(deviceUnmountTimelineAction.logicOrder).toBeLessThan(platformUnmountTimelineAction.logicOrder)
  })
})
