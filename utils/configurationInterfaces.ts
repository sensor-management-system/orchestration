/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020, 2021
 * - Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
 * - Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
 * - Tobias Kuhnert (UFZ, tobias.kuhnert@ufz.de)
 * - Erik Pongratz (UFZ, erik.pongratz@ufz.de)
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
import { Platform } from '@/models/Platform'
import { Contact } from '@/models/Contact'
import { Device } from '@/models/Device'
import { DeviceProperty } from '@/models/DeviceProperty'
import { PlatformMountAction } from '@/models/PlatformMountAction'
import { DeviceMountAction } from '@/models/DeviceMountAction'
import { PlatformUnmountAction } from '@/models/PlatformUnmountAction'
import { DeviceUnmountAction } from '@/models/DeviceUnmountAction'
import { DynamicLocationBeginAction } from '@/models/DynamicLocationBeginAction'
import { DynamicLocationEndAction } from '@/models/DynamicLocationEndAction'
import { StaticLocationBeginAction } from '@/models/StaticLocationBeginAction'
import { StaticLocationEndAction } from '@/models/StaticLocationEndAction'

export interface IActionDateWithText {
  date: DateTime
  text: string
}

export interface IActionDateWithTextItem extends IActionDateWithText {
  isSelected?: boolean
  isNow?: boolean
}

export interface IMountInfo {
  parentPlatform: Platform | null
  offsetX: number
  offsetY: number
  offsetZ: number
}

export interface IStaticLocationInfo {
  x: number | null
  y: number | null
  z: number | null
  epsgCode: string
  elevationDatumName: string
}

export interface IDynamicLocationInfo {
  x: string | null
  y: string | null
  z: string | null
  deviceX: string | null
  deviceY: string | null
  deviceZ: string | null
  epsgCode: string
  elevationDatumName: string
}

export interface IMountTimelineAction {
  key: string
  color: string
  icon: string
  date: DateTime
  title: string
  contact: Contact
  mountInfo: IMountInfo | null
  description: string
}

export interface IStaticLocationTimelineAction {
  key: string
  color: string
  icon: string
  date: DateTime
  title: string
  contact: Contact
  description: string
  staticLocationInfo: IStaticLocationInfo | null
}

export interface IDynamicLocationTimelineAction {
  key: string
  color: string
  icon: string
  date: DateTime
  title: string
  contact: Contact
  description: string
  dynamicLocationInfo: IDynamicLocationInfo | null
}

export type ITimelineAction = IMountTimelineAction | IStaticLocationTimelineAction | IDynamicLocationTimelineAction
export class PlatformMountTimelineAction implements IMountTimelineAction {
  private mountAction: PlatformMountAction

  constructor (mountAction: PlatformMountAction) {
    this.mountAction = mountAction
  }

  get key (): string {
    return 'Platform-mount-action-' + this.mountAction.id
  }

  get color (): string {
    return 'blue'
  }

  get icon (): string {
    return 'mdi-rocket'
  }

  get date (): DateTime {
    return this.mountAction.date
  }

  get title (): string {
    return this.mountAction.platform.shortName + ' mounted'
  }

  get contact (): Contact {
    return this.mountAction.contact
  }

  get mountInfo (): IMountInfo {
    return {
      parentPlatform: this.mountAction.parentPlatform,
      offsetX: this.mountAction.offsetX,
      offsetY: this.mountAction.offsetY,
      offsetZ: this.mountAction.offsetZ
    }
  }

  get description (): string {
    return this.mountAction.description
  }
}

export class DeviceMountTimelineAction implements IMountTimelineAction {
  private mountAction: DeviceMountAction

  constructor (mountAction: DeviceMountAction) {
    this.mountAction = mountAction
  }

  get key (): string {
    return 'Device-mount-action-' + this.mountAction.id
  }

  get color (): string {
    return 'blue'
  }

  get icon (): string {
    return 'mdi-network'
  }

  get date (): DateTime {
    return this.mountAction.date
  }

  get title (): string {
    return this.mountAction.device.shortName + ' mounted'
  }

  get contact (): Contact {
    return this.mountAction.contact
  }

  get mountInfo (): IMountInfo {
    return {
      parentPlatform: this.mountAction.parentPlatform,
      offsetX: this.mountAction.offsetX,
      offsetY: this.mountAction.offsetY,
      offsetZ: this.mountAction.offsetZ
    }
  }

  get description (): string {
    return this.mountAction.description
  }
}

export class PlatformUnmountTimelineAction implements IMountTimelineAction {
  private unmountAction: PlatformUnmountAction

  constructor (unmountAction: PlatformUnmountAction) {
    this.unmountAction = unmountAction
  }

  get key (): string {
    return 'Platform-unmount-action-' + this.unmountAction.id
  }

  get color (): string {
    return 'red'
  }

  get icon (): string {
    return 'mdi-rocket'
  }

  get date (): DateTime {
    return this.unmountAction.date
  }

  get title (): string {
    return this.unmountAction.platform.shortName + ' unmounted'
  }

  get contact (): Contact {
    return this.unmountAction.contact
  }

  get mountInfo (): null {
    return null
  }

  get description (): string {
    return this.unmountAction.description
  }
}

export class DeviceUnmountTimelineAction implements IMountTimelineAction {
  private unmountAction: DeviceUnmountAction

  constructor (unmountAction: DeviceUnmountAction) {
    this.unmountAction = unmountAction
  }

  get key (): string {
    return 'Device-unmount-action-' + this.unmountAction.device.id + this.unmountAction.date.toString()
  }

  get color (): string {
    return 'red'
  }

  get icon (): string {
    return 'mdi-network'
  }

  get date (): DateTime {
    return this.unmountAction.date
  }

  get title (): string {
    return this.unmountAction.device.shortName + ' unmounted'
  }

  get contact (): Contact {
    return this.unmountAction.contact
  }

  get mountInfo (): null {
    return null
  }

  get description (): string {
    return this.unmountAction.description
  }
}

export class StaticLocationBeginTimelineAction implements IStaticLocationTimelineAction {
  private staticLocationBeginAction: StaticLocationBeginAction

  constructor (staticLocationBeginAction: StaticLocationBeginAction) {
    this.staticLocationBeginAction = staticLocationBeginAction
  }

  get key (): string {
    return 'Static-location-begin-action-' + this.staticLocationBeginAction.id
  }

  get color (): string {
    return 'blue'
  }

  get icon (): string {
    return 'mdi-earth'
  }

  get title (): string {
    return 'Static location begin'
  }

  get description (): string {
    return this.staticLocationBeginAction.description
  }

  get contact (): Contact {
    return this.staticLocationBeginAction.contact!
  }

  get date (): DateTime {
    return this.staticLocationBeginAction.beginDate!
  }

  get staticLocationInfo (): IStaticLocationInfo {
    return {
      x: this.staticLocationBeginAction.x,
      y: this.staticLocationBeginAction.y,
      z: this.staticLocationBeginAction.z,
      epsgCode: this.staticLocationBeginAction.epsgCode,
      elevationDatumName: this.staticLocationBeginAction.elevationDatumName
    }
  }
}

export class StaticLocationEndTimelineAction implements IStaticLocationTimelineAction {
  private staticLocationEndAction: StaticLocationEndAction

  constructor (staticLocationEndAction: StaticLocationEndAction) {
    this.staticLocationEndAction = staticLocationEndAction
  }

  get key (): string {
    return 'Static-location-end-action-' + this.staticLocationEndAction.id
  }

  get color (): string {
    return 'red'
  }

  get icon (): string {
    return 'mdi-earth'
  }

  get title (): string {
    return 'Static location end'
  }

  get description (): string {
    return this.staticLocationEndAction.description
  }

  get contact (): Contact {
    return this.staticLocationEndAction.contact!
  }

  get date (): DateTime {
    return this.staticLocationEndAction.endDate!
  }

  get staticLocationInfo (): null {
    return null
  }
}

export class DynamicLocationBeginTimelineAction implements IDynamicLocationTimelineAction {
  private dynamicLocationBeginAction: DynamicLocationBeginAction
  private devices: Device[]

  constructor (dynamicLocationBeginAction: DynamicLocationBeginAction, devices: Device[]) {
    this.dynamicLocationBeginAction = dynamicLocationBeginAction
    this.devices = devices
  }

  get key (): string {
    return 'Dynamic-location-begin-action-' + this.dynamicLocationBeginAction.id
  }

  get color (): string {
    return 'blue'
  }

  get icon (): string {
    return 'mdi-earth'
  }

  get title (): string {
    return 'Dynamic location begin'
  }

  get description (): string {
    return this.dynamicLocationBeginAction.description
  }

  get contact (): Contact {
    return this.dynamicLocationBeginAction.contact!
  }

  get date (): DateTime {
    return this.dynamicLocationBeginAction.beginDate!
  }

  get dynamicLocationInfo (): IDynamicLocationInfo {
    return {
      x: this.propertyText(this.dynamicLocationBeginAction.x),
      y: this.propertyText(this.dynamicLocationBeginAction.y),
      z: this.propertyText(this.dynamicLocationBeginAction.z),
      deviceX: this.deviceText(this.findDevice(this.dynamicLocationBeginAction.x)),
      deviceY: this.deviceText(this.findDevice(this.dynamicLocationBeginAction.y)),
      deviceZ: this.deviceText(this.findDevice(this.dynamicLocationBeginAction.z)),
      epsgCode: this.dynamicLocationBeginAction.epsgCode,
      elevationDatumName: this.dynamicLocationBeginAction.elevationDatumName
    }
  }

  propertyText (deviceProperty: DeviceProperty | null): string | null {
    if (!deviceProperty) {
      return null
    }
    return deviceProperty.propertyName
  }

  findDevice (deviceProperty: DeviceProperty | null): Device | null {
    if (!deviceProperty) {
      return null
    }
    for (const device of this.devices) {
      for (const someDeviceProperty of device.properties) {
        if (someDeviceProperty.id === deviceProperty.id) {
          return device
        }
      }
    }
    return null
  }

  deviceText (device: Device | null): string {
    if (!device || !device.shortName) {
      return ''
    }
    return device.shortName
  }
}

export class DynamicLocationEndTimelineAction implements IDynamicLocationTimelineAction {
  private dynamicLocationEndAction: DynamicLocationEndAction

  constructor (dynamicLocationEndAction: DynamicLocationEndAction) {
    this.dynamicLocationEndAction = dynamicLocationEndAction
  }

  get key (): string {
    return 'Dynamic-location-end-action-' + this.dynamicLocationEndAction.id
  }

  get color (): string {
    return 'red'
  }

  get icon (): string {
    return 'mdi-earth'
  }

  get title (): string {
    return 'Dynamic location end'
  }

  get description (): string {
    return this.dynamicLocationEndAction.description
  }

  get contact (): Contact {
    return this.dynamicLocationEndAction.contact!
  }

  get date (): DateTime {
    return this.dynamicLocationEndAction.endDate!
  }

  get dynamicLocationInfo (): null {
    return null
  }
}
