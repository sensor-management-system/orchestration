/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020 - 2023
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

    const platformMount = new PlatformMountAction('1', platform, null, DateTime.utc(), null, 0, 0, 0, contact, null, '', null)
    const deviceMountAction = new DeviceMountAction('2', device, null, DateTime.utc(), null, 0, 0, 0, contact, null, '', null)

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

    const platformMount = new PlatformMountAction('1', platform, null, DateTime.utc(), null, 0, 0, 0, contact, null, '', null)
    const deviceMountAction = new DeviceMountAction('2', device, null, DateTime.utc(), null, 0, 0, 0, contact, null, '', null)

    const platformMountTimelineAction = new PlatformMountTimelineAction(platformMount)

    const deviceMountTimelineAction = new DeviceMountTimelineAction(deviceMountAction)

    expect(platformMountTimelineAction.logicOrder).toBeLessThan(deviceMountTimelineAction.logicOrder)
  })
  it('should have lower values for device unmounts then for platform unmounts', () => {
    const contact = new Contact()
    const platform = new Platform()
    const device = new Device()

    const platformMount = new PlatformMountAction('1', platform, null, DateTime.utc(), null, 0, 0, 0, contact, null, '', null)
    const deviceMountAction = new DeviceMountAction('2', device, null, DateTime.utc(), null, 0, 0, 0, contact, null, '', null)

    const platformUnmountTimelineAction = new PlatformUnmountTimelineAction(platformMount)

    const deviceUnmountTimelineAction = new DeviceUnmountTimelineAction(deviceMountAction)

    expect(deviceUnmountTimelineAction.logicOrder).toBeLessThan(platformUnmountTimelineAction.logicOrder)
  })
})
