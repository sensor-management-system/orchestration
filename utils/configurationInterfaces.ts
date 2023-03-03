/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020-2023
 * - Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
 * - Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
 * - Tobias Kuhnert (UFZ, tobias.kuhnert@ufz.de)
 * - Maximilian Schaldach (UFZ, maximilian.schaldach@ufz.de)
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for
 *   Geosciences (GFZ, https://www.gfz-potsdam.de)
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
import { IPlatform } from '@/models/Platform'
import { IContact, Contact } from '@/models/Contact'
import { Device } from '@/models/Device'
import { DeviceProperty } from '@/models/DeviceProperty'
import { PlatformMountAction } from '@/models/PlatformMountAction'
import { DeviceMountAction } from '@/models/DeviceMountAction'
import { DynamicLocationAction } from '@/models/DynamicLocationAction'
import { StaticLocationAction } from '@/models/StaticLocationAction'
import { GenericAction } from '@/models/GenericAction'

export interface IActionDateWithText {
  date: DateTime
  text: string
}

export interface IActionDateWithTextItem extends IActionDateWithText {
  isSelected?: boolean
  isNow?: boolean
}

export interface IMountInfo {
  parentPlatform: IPlatform | null
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
  date: DateTime | null
  title: string
  contact: IContact | null
  mountInfo: IMountInfo | null
  description: string
  isUnmountAction: boolean
}

export interface IStaticLocationTimelineAction {
  key: string
  color: string
  icon: string
  date: DateTime
  title: string
  contact: Contact
  description: string | null
  staticLocationInfo: IStaticLocationInfo | null
}

export interface IDynamicLocationTimelineAction {
  key: string
  color: string
  icon: string
  date: DateTime
  title: string
  contact: Contact
  description: string | null
  dynamicLocationInfo: IDynamicLocationInfo | null
}

export interface IGenericTimelineAction {
  key: string
  color: string
  icon?: string
  date: DateTime
  endDate: DateTime | null
  title: string
  contact: Contact
  description: string | null
  type: string
}

export type ITimelineAction = IMountTimelineAction | IStaticLocationTimelineAction | IDynamicLocationTimelineAction | IGenericTimelineAction

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
    return this.mountAction.beginDate
  }

  get title (): string {
    return this.mountAction.platform.shortName + ' mounted'
  }

  get contact (): IContact {
    return this.mountAction.beginContact
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
    return this.mountAction.beginDescription
  }

  get isUnmountAction (): boolean {
    return false
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
    return this.mountAction.beginDate
  }

  get title (): string {
    return this.mountAction.device.shortName + ' mounted'
  }

  get contact (): IContact {
    return this.mountAction.beginContact
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
    return this.mountAction.beginDescription
  }

  get isUnmountAction (): boolean {
    return false
  }
}

export class PlatformUnmountTimelineAction implements IMountTimelineAction {
  private mountAction: PlatformMountAction

  constructor (mountAction: PlatformMountAction) {
    this.mountAction = mountAction
  }

  get key (): string {
    return 'Platform-unmount-action-' + this.mountAction.id
  }

  get color (): string {
    return 'red'
  }

  get icon (): string {
    return 'mdi-rocket'
  }

  get date (): DateTime | null {
    return this.mountAction.endDate
  }

  get title (): string {
    return this.mountAction.platform.shortName + ' unmounted'
  }

  get contact (): IContact | null {
    return this.mountAction.endContact
  }

  get mountInfo (): null {
    return null
  }

  get description (): string {
    return this.mountAction.endDescription || ''
  }

  get isUnmountAction (): boolean {
    return true
  }
}

export class DeviceUnmountTimelineAction implements IMountTimelineAction {
  private mountAction: DeviceMountAction

  constructor (mountAction: DeviceMountAction) {
    this.mountAction = mountAction
  }

  get key (): string {
    return 'Device-unmount-action-' + this.mountAction.id
  }

  get color (): string {
    return 'red'
  }

  get icon (): string {
    return 'mdi-network'
  }

  get date (): DateTime | null {
    return this.mountAction.endDate
  }

  get title (): string {
    return this.mountAction.device.shortName + ' unmounted'
  }

  get contact (): IContact | null {
    return this.mountAction.endContact
  }

  get mountInfo (): null {
    return null
  }

  get description (): string {
    return this.mountAction.endDescription || ''
  }

  get isUnmountAction (): boolean {
    return true
  }
}

export class StaticLocationBeginTimelineAction implements IStaticLocationTimelineAction {
  private staticLocationBeginAction: StaticLocationAction

  constructor (staticLocationBeginAction: StaticLocationAction) {
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

  get description (): string|null {
    return this.staticLocationBeginAction.beginDescription
  }

  get contact (): Contact {
    return this.staticLocationBeginAction.beginContact!
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
  private staticLocationEndAction: StaticLocationAction

  constructor (staticLocationEndAction: StaticLocationAction) {
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

  get description (): string | null {
    return this.staticLocationEndAction.endDescription
  }

  get contact (): Contact {
    return this.staticLocationEndAction.endContact!
  }

  get date (): DateTime {
    return this.staticLocationEndAction.endDate!
  }

  get staticLocationInfo (): null {
    return null
  }
}

export class DynamicLocationBeginTimelineAction implements IDynamicLocationTimelineAction {
  private dynamicLocationBeginAction: DynamicLocationAction
  private devices: Device[]

  constructor (dynamicLocationBeginAction: DynamicLocationAction, devices: Device[]) {
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

  get description (): string |null {
    return this.dynamicLocationBeginAction.beginDescription
  }

  get contact (): Contact {
    return this.dynamicLocationBeginAction.beginContact!
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
  private dynamicLocationEndAction: DynamicLocationAction

  constructor (dynamicLocationEndAction: DynamicLocationAction) {
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

  get description (): string | null {
    return this.dynamicLocationEndAction.endDescription
  }

  get contact (): Contact {
    return this.dynamicLocationEndAction.endContact!
  }

  get date (): DateTime {
    return this.dynamicLocationEndAction.endDate!
  }

  get dynamicLocationInfo (): null {
    return null
  }
}

export class GenericTimelineAction implements IGenericTimelineAction {
  private genericAction: GenericAction

  constructor (genericAction: GenericAction) {
    this.genericAction = genericAction
  }

  get key (): string {
    return 'Generic-action-' + this.genericAction.id
  }

  get color (): string {
    return 'blue'
  }

  get title (): string {
    return this.genericAction.actionTypeName
  }

  get description (): string | null {
    return this.genericAction.description
  }

  get contact (): Contact {
    return this.genericAction.contact!
  }

  get date (): DateTime {
    return this.genericAction.beginDate!
  }

  get endDate (): DateTime | null {
    return this.genericAction.endDate
  }

  get type (): string {
    return 'generic_configuration_action'
  }
}

export type MountActionDateDTO = {
  beginDate: DateTime | null,
  endDate: DateTime | null
}

export type MountActionInformationDTO = {
  beginDate: DateTime | null
  endDate: DateTime | null
  offsetX: number
  offsetY: number
  offsetZ: number
  beginContact: IContact | null
  endContact: IContact | null
  beginDescription: string
  endDescription: string | null
}

export interface IOffsets {
  offsetX: number
  offsetY: number
  offsetZ: number
}
