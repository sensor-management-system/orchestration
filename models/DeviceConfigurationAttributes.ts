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
import { DeviceProperty } from '@/models/DeviceProperty'
import Device from '@/models/Device'

export interface IDeviceConfigurationAttributes {
  device: Device
  offsetX: number
  offsetY: number
  offsetZ: number
  calibrationDate: Date | null
  deviceProperties: DeviceProperty[]
}

export class DeviceConfigurationAttributes implements IDeviceConfigurationAttributes {
  private _device: Device
  private _offsetX: number = 0
  private _offsetY: number = 0
  private _offsetZ: number = 0
  private _calibrationDate: Date | null = null
  private _deviceProperties: DeviceProperty[] = []

  constructor (device: Device) {
    this._device = device
  }

  static createFromObject (someObject: IDeviceConfigurationAttributes): DeviceConfigurationAttributes {
    const newObject = new DeviceConfigurationAttributes(someObject.device)

    newObject.offsetX = someObject.offsetX
    newObject.offsetY = someObject.offsetY
    newObject.offsetZ = someObject.offsetZ
    newObject.calibrationDate = someObject.calibrationDate instanceof Date ? new Date(someObject.calibrationDate.getTime()) : null
    newObject.deviceProperties = [...someObject.deviceProperties]

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

  get calibrationDate (): Date | null {
    return this._calibrationDate
  }

  set calibrationDate (date: Date | null) {
    this._calibrationDate = date
  }

  get deviceProperties (): DeviceProperty[] {
    return this._deviceProperties
  }

  set deviceProperties (properties: DeviceProperty[]) {
    this._deviceProperties = []
    properties.forEach(property => this.addDeviceProperty(property))
  }

  addDeviceProperty (property: DeviceProperty): number {
    if (!this.device.properties.find(e => e === property)) {
      throw new Error('property is not a member of the device')
    }
    return this._deviceProperties.push(property)
  }

  addDevicePropertyById (id: string | null): number {
    const property = this.device.properties.find(e => e.id === id)
    if (!property) {
      throw new Error('unknown property id')
    }
    return this._deviceProperties.push(property)
  }

  removeDeviceProperty (property: DeviceProperty): number {
    const index = this.device.properties.findIndex(e => e === property)
    if (index === -1) {
      throw new Error('unknown property')
    }
    this._deviceProperties.splice(index, 1)
    return index
  }

  removeDevicePropertyById (id: string | null): number {
    const index = this.device.properties.findIndex(e => e.id === id)
    if (index === -1) {
      throw new Error('unknown property id')
    }
    this._deviceProperties.splice(index, 1)
    return index
  }
}
