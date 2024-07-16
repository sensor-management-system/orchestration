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

import { IMountAction, MountAction } from '@/models/MountAction'
import { Platform } from '@/models/Platform'
import { Contact } from '@/models/Contact'
import { Device } from '@/models/Device'

export interface IDeviceMountAction extends IMountAction {
  device: Device
  parentDevice: Device | null
}

export class DeviceMountAction extends MountAction implements IDeviceMountAction {
  private _device: Device
  private _parentDevice: Device | null

  constructor (
    id: string,
    device: Device,
    parentPlatform: Platform | null,
    parentDevice: Device | null,
    beginDate: DateTime,
    endDate: DateTime | null,
    offsetX: number,
    offsetY: number,
    offsetZ: number,
    epsgCode: string,
    x: number | null,
    y: number | null,
    z: number | null,
    elevationDatumName: string,
    elevationDatumUri: string,
    beginContact: Contact,
    endContact: Contact | null,
    beginDescription: string,
    endDescription: string | null,
    label: string
  ) {
    super(
      id,
      parentPlatform,
      beginDate,
      endDate,
      offsetX,
      offsetY,
      offsetZ,
      epsgCode,
      x,
      y,
      z,
      elevationDatumName,
      elevationDatumUri,
      beginContact,
      endContact,
      beginDescription,
      endDescription,
      label
    )
    this._device = device
    this._parentDevice = parentDevice
  }

  get TYPE (): string {
    return 'DEVICE_MOUNT_ACTION'
  }

  get device (): Device {
    return this._device
  }

  get parentDevice (): Device | null {
    return this._parentDevice
  }

  isDeviceMountAction (): this is IDeviceMountAction {
    return true
  }

  static createFromObject (otherAction: Omit<IDeviceMountAction, 'TYPE'>): DeviceMountAction {
    return new DeviceMountAction(
      otherAction.id,
      Device.createFromObject(otherAction.device),
      otherAction.parentPlatform === null ? null : Platform.createFromObject(otherAction.parentPlatform),
      otherAction.parentDevice === null ? null : Device.createFromObject(otherAction.parentDevice),
      otherAction.beginDate,
      otherAction.endDate === null ? null : otherAction.endDate,
      otherAction.offsetX,
      otherAction.offsetY,
      otherAction.offsetZ,
      otherAction.epsgCode,
      otherAction.x,
      otherAction.y,
      otherAction.z,
      otherAction.elevationDatumName,
      otherAction.elevationDatumUri,
      Contact.createFromObject(otherAction.beginContact),
      otherAction.endContact === null ? null : Contact.createFromObject(otherAction.endContact),
      otherAction.beginDescription,
      otherAction.endDescription === null ? null : otherAction.endDescription,
      otherAction.label
    )
  }
}
