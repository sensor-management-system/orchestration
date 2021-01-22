/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020
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
import { Device } from '@/models/Device'

export interface IDeviceConfigurationAttributes {
  device: Device
  offsetX: number
  offsetY: number
  offsetZ: number
  calibrationDate: DateTime | null
}

export class DeviceConfigurationAttributes implements IDeviceConfigurationAttributes {
  private _device: Device
  private _offsetX: number = 0
  private _offsetY: number = 0
  private _offsetZ: number = 0
  private _calibrationDate: DateTime | null = null

  constructor (device: Device) {
    this._device = device
  }

  static createFromObject (someObject: IDeviceConfigurationAttributes): DeviceConfigurationAttributes {
    const newObject = new DeviceConfigurationAttributes(someObject.device)

    newObject.offsetX = someObject.offsetX
    newObject.offsetY = someObject.offsetY
    newObject.offsetZ = someObject.offsetZ
    // luxon DateTime objects are immutable
    newObject.calibrationDate = someObject.calibrationDate

    return newObject
  }

  get id (): string | null {
    return this._device.id
  }

  get device (): Device {
    return this._device
  }

  get offsetX (): number {
    return this._offsetX
  }

  set offsetX (offsetX: number) {
    this._offsetX = offsetX
  }

  get offsetY (): number {
    return this._offsetY
  }

  set offsetY (offsetY: number) {
    this._offsetY = offsetY
  }

  get offsetZ (): number {
    return this._offsetZ
  }

  set offsetZ (offsetZ: number) {
    this._offsetZ = offsetZ
  }

  get calibrationDate (): DateTime | null {
    return this._calibrationDate
  }

  set calibrationDate (date: DateTime | null) {
    this._calibrationDate = date
  }
}
