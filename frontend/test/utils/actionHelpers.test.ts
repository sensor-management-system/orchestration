/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2023 - 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Tobias Kuhnert <tobias.kuhnert@ufz.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 * - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
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
      epsgCode: '',
      x: null,
      y: null,
      z: null,
      elevationDatumName: '',
      elevationDatumUri: '',
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
      epsgCode: '',
      x: null,
      y: null,
      z: null,
      elevationDatumName: '',
      elevationDatumUri: '',
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
      epsgCode: '',
      x: null,
      y: null,
      z: null,
      elevationDatumName: '',
      elevationDatumUri: '',
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
      epsgCode: '',
      x: null,
      y: null,
      z: null,
      elevationDatumName: '',
      elevationDatumUri: '',
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
      epsgCode: '',
      x: null,
      y: null,
      z: null,
      elevationDatumName: '',
      elevationDatumUri: '',
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
      epsgCode: '',
      x: null,
      y: null,
      z: null,
      elevationDatumName: '',
      elevationDatumUri: '',
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
      epsgCode: '',
      x: null,
      y: null,
      z: null,
      elevationDatumName: '',
      elevationDatumUri: '',
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
      epsgCode: '',
      x: null,
      y: null,
      z: null,
      elevationDatumName: '',
      elevationDatumUri: '',
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
      epsgCode: '',
      x: null,
      y: null,
      z: null,
      elevationDatumName: '',
      elevationDatumUri: '',
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
      epsgCode: '',
      x: null,
      y: null,
      z: null,
      elevationDatumName: '',
      elevationDatumUri: '',
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
      epsgCode: '',
      x: null,
      y: null,
      z: null,
      elevationDatumName: '',
      elevationDatumUri: '',
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
      epsgCode: '',
      x: null,
      y: null,
      z: null,
      elevationDatumName: '',
      elevationDatumUri: '',
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
