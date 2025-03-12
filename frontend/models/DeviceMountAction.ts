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
    beginContact: Contact | null,
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

  set device (device: Device) {
    this._device = device
  }

  get parentDevice (): Device | null {
    return this._parentDevice
  }

  set parentDevice (newDevice: Device | null) {
    this._parentDevice = newDevice
  }

  isDeviceMountAction (): this is IDeviceMountAction {
    return true
  }

  static createFromObject (otherAction: Omit<IDeviceMountAction, 'TYPE'>): DeviceMountAction {
    return new DeviceMountAction(
      otherAction.id,
      Device.createFromObject(otherAction.device),
      otherAction.parentPlatform ? Platform.createFromObject(otherAction.parentPlatform) : null,
      otherAction.parentDevice ? Device.createFromObject(otherAction.parentDevice) : null,
      otherAction.beginDate,
      otherAction.endDate ? otherAction.endDate : null,
      otherAction.offsetX,
      otherAction.offsetY,
      otherAction.offsetZ,
      otherAction.epsgCode,
      otherAction.x,
      otherAction.y,
      otherAction.z,
      otherAction.elevationDatumName,
      otherAction.elevationDatumUri,
      otherAction.beginContact ? Contact.createFromObject(otherAction.beginContact) : null,
      otherAction.endContact ? Contact.createFromObject(otherAction.endContact) : null,
      otherAction.beginDescription,
      otherAction.endDescription === null ? null : otherAction.endDescription,
      otherAction.label
    )
  }
}
