/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Tobias Kuhnert <tobias.kuhnert@ufz.de>
 * - Maximilian Schaldach <maximilian.schaldach@ufz.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 * - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
import { DateTime } from 'luxon'
import { IPlatform } from '@/models/Platform'
import { IContact, Contact } from '@/models/Contact'
import { IDevice, Device } from '@/models/Device'
import { DeviceProperty } from '@/models/DeviceProperty'
import { PlatformMountAction } from '@/models/PlatformMountAction'
import { DeviceMountAction } from '@/models/DeviceMountAction'
import { DynamicLocationAction } from '@/models/DynamicLocationAction'
import { StaticLocationAction } from '@/models/StaticLocationAction'
import { GenericAction } from '@/models/GenericAction'
import { ParameterChangeAction } from '@/models/ParameterChangeAction'
import {
  KIND_OF_ACTION_TYPE_DEVICE_MOUNT,
  KIND_OF_ACTION_TYPE_DEVICE_UNMOUNT,
  KIND_OF_ACTION_TYPE_DYNAMIC_LOCATION_BEGIN,
  KIND_OF_ACTION_TYPE_DYNAMIC_LOCATION_END,
  KIND_OF_ACTION_TYPE_GENERIC_ACTION, KIND_OF_ACTION_TYPE_PARAMETER_CHANGE_ACTION,
  KIND_OF_ACTION_TYPE_PLATFORM_MOUNT,
  KIND_OF_ACTION_TYPE_PLATFORM_UNMOUNT,
  KIND_OF_ACTION_TYPE_STATIC_LOCATION_BEGIN,
  KIND_OF_ACTION_TYPE_STATIC_LOCATION_END
} from '@/models/ActionKind'

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
  parentDevice: IDevice | null
  offsetX: number
  offsetY: number
  offsetZ: number
  epsgCode: string
  x: number | null
  y: number | null
  z: number | null
  elevationDatumName: string
  elevationDatumUri: string
}

export interface IStaticLocationInfo {
  id: string
  x: number | null
  y: number | null
  z: number | null
  epsgCode: string
  elevationDatumName: string
}

export interface IDynamicLocationInfo {
  id: string
  x: string | null
  y: string | null
  z: string | null
  deviceX: string | null
  deviceY: string | null
  deviceZ: string | null
  epsgCode: string
  elevationDatumName: string
}

export interface IMountTimelineAction <T> {
  key: string
  color: string
  icon: string
  date: DateTime | null
  title: string
  subtitle: string
  contact: IContact | null
  mountInfo: IMountInfo | null
  description: string
  isUnmountAction: boolean
  mountAction: T
  // Logic order defines the ordering in the overview
  // of actions in case they have the same point in time.
  logicOrder: number
  kind: string
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
  kind: string
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
  kind: string
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
  kind: string
  actionTypeUrl: string

}

export type ITimelineAction = IMountTimelineAction<PlatformMountAction> | IMountTimelineAction<DeviceMountAction>| IStaticLocationTimelineAction | IDynamicLocationTimelineAction | IGenericTimelineAction

export class PlatformMountTimelineAction implements IMountTimelineAction<PlatformMountAction> {
  private _mountAction: PlatformMountAction

  constructor (mountAction: PlatformMountAction) {
    this._mountAction = mountAction
  }

  get id (): string {
    return this._mountAction.id
  }

  get key (): string {
    return 'Platform-mount-action-' + this._mountAction.id
  }

  get color (): string {
    return 'blue'
  }

  get icon (): string {
    return 'mdi-rocket'
  }

  get date (): DateTime {
    return this._mountAction.beginDate
  }

  get title (): string {
    return this._mountAction.platform.shortName + ' mounted'
  }

  get subtitle (): string {
    return this._mountAction.label
  }

  get contact (): IContact {
    return this._mountAction.beginContact
  }

  get mountInfo (): IMountInfo {
    return {
      parentPlatform: this._mountAction.parentPlatform,
      parentDevice: null,
      offsetX: this._mountAction.offsetX,
      offsetY: this._mountAction.offsetY,
      offsetZ: this._mountAction.offsetZ,
      epsgCode: this._mountAction.epsgCode,
      x: this._mountAction.x,
      y: this._mountAction.y,
      z: this._mountAction.z,
      elevationDatumName: this._mountAction.elevationDatumName,
      elevationDatumUri: this._mountAction.elevationDatumUri
    }
  }

  get description (): string {
    return this._mountAction.beginDescription
  }

  get isUnmountAction (): boolean {
    return false
  }

  get mountAction (): PlatformMountAction {
    return this._mountAction
  }

  get kind (): string {
    return KIND_OF_ACTION_TYPE_PLATFORM_MOUNT
  }

  get logicOrder (): number {
    return 100
  }
}

export class DeviceMountTimelineAction implements IMountTimelineAction<DeviceMountAction> {
  private _mountAction: DeviceMountAction

  constructor (mountAction: DeviceMountAction) {
    this._mountAction = mountAction
  }

  get id (): string {
    return this._mountAction.id
  }

  get key (): string {
    return 'Device-mount-action-' + this._mountAction.id
  }

  get color (): string {
    return 'blue'
  }

  get icon (): string {
    return 'mdi-network'
  }

  get date (): DateTime {
    return this._mountAction.beginDate
  }

  get title (): string {
    return this._mountAction.device.shortName + ' mounted'
  }

  get subtitle (): string {
    return this._mountAction.label
  }

  get contact (): IContact {
    return this._mountAction.beginContact
  }

  get mountInfo (): IMountInfo {
    return {
      parentPlatform: this._mountAction.parentPlatform,
      parentDevice: this._mountAction.parentDevice,
      offsetX: this._mountAction.offsetX,
      offsetY: this._mountAction.offsetY,
      offsetZ: this._mountAction.offsetZ,
      epsgCode: this._mountAction.epsgCode,
      x: this._mountAction.x,
      y: this._mountAction.y,
      z: this._mountAction.z,
      elevationDatumName: this._mountAction.elevationDatumName,
      elevationDatumUri: this._mountAction.elevationDatumUri
    }
  }

  get description (): string {
    return this._mountAction.beginDescription
  }

  get isUnmountAction (): boolean {
    return false
  }

  get mountAction (): DeviceMountAction {
    return this._mountAction
  }

  get kind (): string {
    return KIND_OF_ACTION_TYPE_DEVICE_MOUNT
  }

  get logicOrder (): number {
    return 200
  }
}

export class PlatformUnmountTimelineAction implements IMountTimelineAction<PlatformMountAction> {
  private _mountAction: PlatformMountAction

  constructor (mountAction: PlatformMountAction) {
    this._mountAction = mountAction
  }

  get id (): string {
    return this._mountAction.id
  }

  get key (): string {
    return 'Platform-unmount-action-' + this._mountAction.id
  }

  get color (): string {
    return 'red'
  }

  get icon (): string {
    return 'mdi-rocket'
  }

  get date (): DateTime | null {
    return this._mountAction.endDate
  }

  get title (): string {
    return this._mountAction.platform.shortName + ' unmounted'
  }

  get subtitle (): string {
    return this._mountAction.label
  }

  get contact (): IContact | null {
    return this._mountAction.endContact || this._mountAction.beginContact
  }

  get mountInfo (): IMountInfo {
    return {
      parentPlatform: this._mountAction.parentPlatform,
      parentDevice: null,
      offsetX: this._mountAction.offsetX,
      offsetY: this._mountAction.offsetY,
      offsetZ: this._mountAction.offsetZ,
      epsgCode: this._mountAction.epsgCode,
      x: this._mountAction.x,
      y: this._mountAction.y,
      z: this._mountAction.z,
      elevationDatumName: this._mountAction.elevationDatumName,
      elevationDatumUri: this._mountAction.elevationDatumUri
    }
  }

  get description (): string {
    return this._mountAction.endDescription || ''
  }

  get isUnmountAction (): boolean {
    return true
  }

  get mountAction (): PlatformMountAction {
    return this._mountAction
  }

  get kind (): string {
    return KIND_OF_ACTION_TYPE_PLATFORM_UNMOUNT
  }

  get logicOrder (): number {
    return 400
  }
}

export class DeviceUnmountTimelineAction implements IMountTimelineAction<DeviceMountAction> {
  private _mountAction: DeviceMountAction

  constructor (mountAction: DeviceMountAction) {
    this._mountAction = mountAction
  }

  get id (): string {
    return this._mountAction.id
  }

  get key (): string {
    return 'Device-unmount-action-' + this._mountAction.id
  }

  get color (): string {
    return 'red'
  }

  get icon (): string {
    return 'mdi-network'
  }

  get date (): DateTime | null {
    return this._mountAction.endDate
  }

  get title (): string {
    return this._mountAction.device.shortName + ' unmounted'
  }

  get subtitle (): string {
    return this._mountAction.label
  }

  get contact (): IContact | null {
    return this._mountAction.endContact || this._mountAction.beginContact
  }

  get mountInfo (): IMountInfo {
    return {
      parentPlatform: this._mountAction.parentPlatform,
      parentDevice: this._mountAction.parentDevice,
      offsetX: this._mountAction.offsetX,
      offsetY: this._mountAction.offsetY,
      offsetZ: this._mountAction.offsetZ,
      epsgCode: this._mountAction.epsgCode,
      x: this._mountAction.x,
      y: this._mountAction.y,
      z: this._mountAction.z,
      elevationDatumName: this._mountAction.elevationDatumName,
      elevationDatumUri: this._mountAction.elevationDatumUri
    }
  }

  get description (): string {
    return this._mountAction.endDescription || ''
  }

  get isUnmountAction (): boolean {
    return true
  }

  get mountAction (): DeviceMountAction {
    return this._mountAction
  }

  get kind (): string {
    return KIND_OF_ACTION_TYPE_DEVICE_UNMOUNT
  }

  get logicOrder (): number {
    return 300
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
    let title = 'Static location begin'
    if (this.staticLocationBeginAction.label) {
      title = title + ' - ' + this.staticLocationBeginAction.label
    }
    return title
  }

  get subtitle (): string {
    return ''
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
      id: this.staticLocationBeginAction.id,
      x: this.staticLocationBeginAction.x,
      y: this.staticLocationBeginAction.y,
      z: this.staticLocationBeginAction.z,
      epsgCode: this.staticLocationBeginAction.epsgCode,
      elevationDatumName: this.staticLocationBeginAction.elevationDatumName
    }
  }

  get kind (): string {
    return KIND_OF_ACTION_TYPE_STATIC_LOCATION_BEGIN
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
    let title = 'Static location end'
    if (this.staticLocationEndAction.label) {
      title = title + ' - ' + this.staticLocationEndAction.label
    }
    return title
  }

  get subtitle (): string {
    return ''
  }

  get description (): string | null {
    return this.staticLocationEndAction.endDescription
  }

  get contact (): Contact {
    return this.staticLocationEndAction.endContact || this.staticLocationEndAction.beginContact!
  }

  get date (): DateTime {
    return this.staticLocationEndAction.endDate!
  }

  get staticLocationInfo (): IStaticLocationInfo {
    return {
      id: this.staticLocationEndAction.id,
      x: this.staticLocationEndAction.x,
      y: this.staticLocationEndAction.y,
      z: this.staticLocationEndAction.z,
      epsgCode: this.staticLocationEndAction.epsgCode,
      elevationDatumName: this.staticLocationEndAction.elevationDatumName
    }
  }

  get kind (): string {
    return KIND_OF_ACTION_TYPE_STATIC_LOCATION_END
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
    let title = 'Dynamic location begin'
    if (this.dynamicLocationBeginAction.label) {
      title = title + ' - ' + this.dynamicLocationBeginAction.label
    }
    return title
  }

  get subtitle (): string {
    return ''
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
      id: this.dynamicLocationBeginAction.id,
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

  get kind (): string {
    return KIND_OF_ACTION_TYPE_DYNAMIC_LOCATION_BEGIN
  }
}

export class DynamicLocationEndTimelineAction implements IDynamicLocationTimelineAction {
  private dynamicLocationEndAction: DynamicLocationAction
  private devices: Device[]

  constructor (dynamicLocationEndAction: DynamicLocationAction, devices: Device[]) {
    this.dynamicLocationEndAction = dynamicLocationEndAction
    this.devices = devices
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
    let title = 'Dynamic location end'
    if (this.dynamicLocationEndAction.label) {
      title = title + ' - ' + this.dynamicLocationEndAction.label
    }
    return title
  }

  get subtitle (): string {
    return ''
  }

  get description (): string | null {
    return this.dynamicLocationEndAction.endDescription
  }

  get contact (): Contact {
    return this.dynamicLocationEndAction.endContact || this.dynamicLocationEndAction.beginContact!
  }

  get date (): DateTime {
    return this.dynamicLocationEndAction.endDate!
  }

  get dynamicLocationInfo (): IDynamicLocationInfo {
    return {
      id: this.dynamicLocationEndAction.id,
      x: this.propertyText(this.dynamicLocationEndAction.x),
      y: this.propertyText(this.dynamicLocationEndAction.y),
      z: this.propertyText(this.dynamicLocationEndAction.z),
      deviceX: this.deviceText(this.findDevice(this.dynamicLocationEndAction.x)),
      deviceY: this.deviceText(this.findDevice(this.dynamicLocationEndAction.y)),
      deviceZ: this.deviceText(this.findDevice(this.dynamicLocationEndAction.z)),
      epsgCode: this.dynamicLocationEndAction.epsgCode,
      elevationDatumName: this.dynamicLocationEndAction.elevationDatumName
    }
  }

  deviceText (device: Device | null): string {
    if (!device || !device.shortName) {
      return ''
    }
    return device.shortName
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

  get kind (): string {
    return KIND_OF_ACTION_TYPE_DYNAMIC_LOCATION_END
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
    return 'grey'
  }

  get title (): string {
    return this.genericAction.actionTypeName
  }

  get subtitle (): string {
    return ''
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

  get kind (): string {
    return KIND_OF_ACTION_TYPE_GENERIC_ACTION
  }

  get actionTypeUrl (): string {
    return this.genericAction.actionTypeUrl
  }

  get icon (): string {
    return this.genericAction.icon
  }
}

export class ParameterChangeTimelineAction implements IGenericTimelineAction {
  private _parameterChangeAction: ParameterChangeAction

  constructor (parameterChangeAction: ParameterChangeAction) {
    this._parameterChangeAction = parameterChangeAction
  }

  get key (): string {
    return 'Parameter-change-action-' + this._parameterChangeAction.id
  }

  get color (): string {
    return 'purple'
  }

  get title (): string {
    let title = 'unknown paramter change action'
    if (this._parameterChangeAction.parameter) {
      title = this._parameterChangeAction.parameter.label + ' change'
    }
    return title
  }

  get subtitle (): string {
    return ''
  }

  get description (): string | null {
    return this._parameterChangeAction.description
  }

  get contact (): Contact {
    return this._parameterChangeAction.contact!
  }

  get date (): DateTime {
    return this._parameterChangeAction.date!
  }

  get endDate (): DateTime | null {
    return null
  }

  get type (): string {
    return 'parameter_change_action'
  }

  get parameterChangeAction (): ParameterChangeAction {
    return this._parameterChangeAction
  }

  get kind (): string {
    return KIND_OF_ACTION_TYPE_PARAMETER_CHANGE_ACTION
  }

  get actionTypeUrl (): string {
    return ''
  }

  get icon (): string {
    return this._parameterChangeAction.icon
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
  epsgCode: string
  x: number | null
  y: number | null
  z: number | null
  elevationDatumName: string
  elevationDatumUri: string
  beginContact: IContact | null
  endContact: IContact | null
  beginDescription: string
  endDescription: string | null
  label: string
}

export interface IOffsets {
  offsetX: number
  offsetY: number
  offsetZ: number
}

export type TsmDeviceMountPropertyCombination = {
  action: DeviceMountAction,
  measuredQuantities: DeviceProperty[]
}

export type TsmDeviceMountPropertyCombinationList = Array<TsmDeviceMountPropertyCombination>
