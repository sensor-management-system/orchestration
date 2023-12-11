/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2023
 * - Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
 * - Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
 * - Tobias Kuhnert (UFZ, tobias.kuhnert@ufz.de)
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for
 *   Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
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
import { Contact } from '@/models/Contact'
import { Device } from '@/models/Device'
import { DeviceMountAction } from '@/models/DeviceMountAction'
import { Platform } from '@/models/Platform'
import { PlatformMountAction } from '@/models/PlatformMountAction'
import { sortActions } from '@/utils/actionHelper'
import { DeviceMountTimelineAction, DeviceUnmountTimelineAction, PlatformMountTimelineAction, PlatformUnmountTimelineAction } from '@/utils/configurationInterfaces'

describe('sortActions', () => {
  it('should return an empty array if empty', () => {
    const result = sortActions([])
    expect(result).toEqual([])
  })
  it('should have an more up to date entry first', () => {
    const deviceMount = DeviceMountAction.createFromObject({
      id: '123',
      device: new Device(),
      parentPlatform: null,
      parentDevice: null,
      beginDate: DateTime.utc(2023, 11, 30, 12, 0, 0),
      endDate: DateTime.utc(2023, 12, 24, 12, 0, 0),
      beginContact: new Contact(),
      endContact: null,
      beginDescription: '',
      endDescription: '',
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0
    })
    const deviceMountTimelineAction = new DeviceMountTimelineAction(deviceMount)
    const deviceUnmountTimelineAction = new DeviceUnmountTimelineAction(deviceMount)

    const elements = [deviceMountTimelineAction, deviceUnmountTimelineAction]

    const sorted = sortActions(elements)

    expect(sorted[0]).toEqual(deviceUnmountTimelineAction)
    expect(sorted[1]).toEqual(deviceMountTimelineAction)
  })
  it('should sort the unmount over the mount if both are related and at the same time', () => {
    const date = DateTime.utc(2023, 11, 30, 12, 0, 0)
    const deviceMount = DeviceMountAction.createFromObject({
      id: '123',
      device: new Device(),
      parentPlatform: null,
      parentDevice: null,
      beginDate: date,
      endDate: date,
      beginContact: new Contact(),
      endContact: null,
      beginDescription: '',
      endDescription: '',
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0
    })
    const deviceMountTimelineAction = new DeviceMountTimelineAction(deviceMount)
    const deviceUnmountTimelineAction = new DeviceUnmountTimelineAction(deviceMount)

    const elements = [deviceMountTimelineAction, deviceUnmountTimelineAction]

    const sorted = sortActions(elements)

    expect(sorted[0]).toEqual(deviceUnmountTimelineAction)
    expect(sorted[1]).toEqual(deviceMountTimelineAction)
  })
  it('should sort the mount over the unmount if both are not related but at the same time', () => {
    const date = DateTime.utc(2023, 11, 30, 12, 0, 0)
    const deviceMount1 = DeviceMountAction.createFromObject({
      id: '123',
      device: new Device(),
      parentPlatform: null,
      parentDevice: null,
      beginDate: DateTime.utc(2022, 11, 30, 12, 0, 0),
      endDate: date,
      beginContact: new Contact(),
      endContact: null,
      beginDescription: '',
      endDescription: '',
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0
    })
    const deviceMount2 = DeviceMountAction.createFromObject({
      id: '124',
      device: new Device(),
      parentPlatform: null,
      parentDevice: null,
      beginDate: date,
      endDate: null,
      beginContact: new Contact(),
      endContact: null,
      beginDescription: '',
      endDescription: '',
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0
    })
    const deviceUnmountTimelineAction = new DeviceUnmountTimelineAction(deviceMount1)
    const deviceMountTimelineAction = new DeviceMountTimelineAction(deviceMount2)

    const elements = [deviceUnmountTimelineAction, deviceMountTimelineAction]

    const sorted = sortActions(elements)

    expect(sorted[0]).toEqual(deviceMountTimelineAction)
    expect(sorted[1]).toEqual(deviceUnmountTimelineAction)
  })
  it('should have a platform mount below a device mount', () => {
    const date = DateTime.utc(2023, 11, 30, 12, 0, 0)
    const deviceMount = DeviceMountAction.createFromObject({
      id: '123',
      device: new Device(),
      parentPlatform: null,
      parentDevice: null,
      beginDate: date,
      endDate: null,
      beginContact: new Contact(),
      endContact: null,
      beginDescription: '',
      endDescription: '',
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0
    })
    const platformMount = PlatformMountAction.createFromObject({
      id: '124',
      platform: new Platform(),
      parentPlatform: null,
      beginDate: date,
      endDate: null,
      beginContact: new Contact(),
      endContact: null,
      beginDescription: '',
      endDescription: '',
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0
    })
    const deviceMountTimelineAction = new DeviceMountTimelineAction(deviceMount)
    const platformMountTimelineAction = new PlatformMountTimelineAction(platformMount)

    const elements = [deviceMountTimelineAction, platformMountTimelineAction]

    const sorted = sortActions(elements)

    expect(sorted[0]).toEqual(deviceMountTimelineAction)
    expect(sorted[1]).toEqual(platformMountTimelineAction)
  })
  it('should have a device unmount below a platform unmount', () => {
    const date = DateTime.utc(2023, 11, 30, 12, 0, 0)
    const deviceMount = DeviceMountAction.createFromObject({
      id: '123',
      device: new Device(),
      parentPlatform: null,
      parentDevice: null,
      beginDate: date,
      endDate: date,
      beginContact: new Contact(),
      endContact: null,
      beginDescription: '',
      endDescription: '',
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0
    })
    const platformMount = PlatformMountAction.createFromObject({
      id: '124',
      platform: new Platform(),
      parentPlatform: null,
      beginDate: date,
      endDate: date,
      beginContact: new Contact(),
      endContact: null,
      beginDescription: '',
      endDescription: '',
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0
    })
    const deviceUnmountTimelineAction = new DeviceUnmountTimelineAction(deviceMount)
    const platformUnmountTimelineAction = new PlatformUnmountTimelineAction(platformMount)

    const elements = [deviceUnmountTimelineAction, platformUnmountTimelineAction]

    const sorted = sortActions(elements)

    expect(sorted[0]).toEqual(platformUnmountTimelineAction)
    expect(sorted[1]).toEqual(deviceUnmountTimelineAction)
  })

  it('should have an more up to date entry first - also for platform mounts', () => {
    const platformMount = PlatformMountAction.createFromObject({
      id: '123',
      platform: new Platform(),
      parentPlatform: null,
      beginDate: DateTime.utc(2023, 11, 30, 12, 0, 0),
      endDate: DateTime.utc(2023, 12, 24, 12, 0, 0),
      beginContact: new Contact(),
      endContact: null,
      beginDescription: '',
      endDescription: '',
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0
    })
    const platformMountTimelineAction = new PlatformMountTimelineAction(platformMount)
    const platformUnmountTimelineAction = new PlatformUnmountTimelineAction(platformMount)

    const elements = [platformMountTimelineAction, platformUnmountTimelineAction]

    const sorted = sortActions(elements)

    expect(sorted[0]).toEqual(platformUnmountTimelineAction)
    expect(sorted[1]).toEqual(platformMountTimelineAction)
  })
  it('should sort the unmount over the mount if both are related and at the same time - also for paltform mounts', () => {
    const date = DateTime.utc(2023, 11, 30, 12, 0, 0)
    const platformMount = PlatformMountAction.createFromObject({
      id: '123',
      platform: new Platform(),
      parentPlatform: null,
      beginDate: date,
      endDate: date,
      beginContact: new Contact(),
      endContact: null,
      beginDescription: '',
      endDescription: '',
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0
    })
    const platformMountTimelineAction = new PlatformMountTimelineAction(platformMount)
    const platformUnmountTimelineAction = new PlatformUnmountTimelineAction(platformMount)

    const elements = [platformMountTimelineAction, platformUnmountTimelineAction]

    const sorted = sortActions(elements)

    expect(sorted[0]).toEqual(platformUnmountTimelineAction)
    expect(sorted[1]).toEqual(platformMountTimelineAction)
  })
  it('should sort the mount over the unmount if both are not related but at the same time - also for platforms', () => {
    const date = DateTime.utc(2023, 11, 30, 12, 0, 0)
    const platformMount1 = PlatformMountAction.createFromObject({
      id: '123',
      platform: new Platform(),
      parentPlatform: null,
      beginDate: DateTime.utc(2022, 11, 30, 12, 0, 0),
      endDate: date,
      beginContact: new Contact(),
      endContact: null,
      beginDescription: '',
      endDescription: '',
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0
    })
    const platformMount2 = PlatformMountAction.createFromObject({
      id: '124',
      platform: new Platform(),
      parentPlatform: null,
      beginDate: date,
      endDate: null,
      beginContact: new Contact(),
      endContact: null,
      beginDescription: '',
      endDescription: '',
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0
    })
    const platformUnmountTimelineAction = new PlatformUnmountTimelineAction(platformMount1)
    const platformMountTimelineAction = new PlatformMountTimelineAction(platformMount2)

    const elements = [platformUnmountTimelineAction, platformMountTimelineAction]

    const sorted = sortActions(elements)

    expect(sorted[0]).toEqual(platformMountTimelineAction)
    expect(sorted[1]).toEqual(platformUnmountTimelineAction)
  })
})
