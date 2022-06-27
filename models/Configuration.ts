/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020-2021
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

import { IContact, Contact } from '@/models/Contact'
import { IMountActions } from '@/models/IMountActions'
import { DeviceMountAction } from '@/models/DeviceMountAction'
import { DeviceUnmountAction } from '@/models/DeviceUnmountAction'
import { PlatformMountAction } from '@/models/PlatformMountAction'
import { PlatformUnmountAction } from '@/models/PlatformUnmountAction'
import { IStationaryLocation, IDynamicLocation, StationaryLocation, DynamicLocation } from '@/models/Location'
import { StaticLocationBeginAction } from '@/models/StaticLocationBeginAction'
import { StaticLocationEndAction } from '@/models/StaticLocationEndAction'
import { DynamicLocationBeginAction } from '@/models/DynamicLocationBeginAction'
import { DynamicLocationEndAction } from '@/models/DynamicLocationEndAction'
import { PermissionGroup, IPermissionGroup, IPermissionableSingleGroup } from '@/models/PermissionGroup'
import { Visibility, IVisible } from '@/models/Visibility'

export interface IConfiguration extends IMountActions, IPermissionableSingleGroup {
  id: string
  startDate: DateTime | null
  endDate: DateTime | null
  projectUri: string
  projectName: string
  label: string
  status: string
  location: IStationaryLocation | IDynamicLocation | null
  contacts: IContact[]
  staticLocationBeginActions: StaticLocationBeginAction[]
  staticLocationEndActions: StaticLocationEndAction[]
  dynamicLocationBeginActions: DynamicLocationBeginAction[]
  dynamicLocationEndActions: DynamicLocationEndAction[]
  createdAt: DateTime | null
  updatedAt: DateTime | null
  createdBy: IContact | null
  updatedBy: IContact | null
  /*
    You may wonder why there is an extra createdByUserId entry here.
    The reason is that we use the createBy & updatedBy to show
    information about the contact that are responsible for the changes.
    Here we refer to the user object (which can have different ids).
  */
  createdByUserId: string | null
  visibility: Visibility
}

export class Configuration implements IConfiguration, IVisible {
  private _id: string = ''
  private _startDate: DateTime | null = null
  private _endDate: DateTime | null = null
  private _projectUri: string = ''
  private _projectName: string = ''
  private _label: string = ''
  private _status: string = ''
  private _location: IStationaryLocation | IDynamicLocation | null = null
  private _contacts: IContact[] = [] as IContact[]
  private _deviceMountActions: DeviceMountAction[] = []
  private _deviceUnmountActions: DeviceUnmountAction[] = []
  private _platformMountActions: PlatformMountAction[] = []
  private _platformUnmountActions: PlatformUnmountAction[] = []
  private _staticLocationBeginActions: StaticLocationBeginAction[] = []
  private _staticLocationEndActions: StaticLocationEndAction[] = []
  private _dynamicLocationBeginActions: DynamicLocationBeginAction[] = []
  private _dynamicLocationEndActions: DynamicLocationEndAction[] = []
  private _permissionGroup: IPermissionGroup | null = null
  private _createdAt: DateTime | null = null
  private _updatedAt: DateTime | null = null
  private _createdBy: IContact | null = null
  private _updatedBy: IContact | null = null
  private _createdByUserId: string | null = null
  private _visibility: Visibility = Visibility.Internal

  get id (): string {
    return this._id
  }

  set id (id: string) {
    this._id = id
  }

  get startDate (): DateTime | null {
    return this._startDate
  }

  set startDate (date: DateTime | null) {
    this._startDate = date
  }

  get endDate (): DateTime | null {
    return this._endDate
  }

  set endDate (date: DateTime | null) {
    this._endDate = date
  }

  get projectName (): string {
    return this._projectName
  }

  set projectName (newProjectName: string) {
    this._projectName = newProjectName
  }

  get projectUri (): string {
    return this._projectUri
  }

  set projectUri (newProjectUri: string) {
    this._projectUri = newProjectUri
  }

  get label (): string {
    return this._label
  }

  set label (newLabel: string) {
    this._label = newLabel
  }

  get status (): string {
    return this._status
  }

  set status (newStatus: string) {
    this._status = newStatus
  }

  get location (): IStationaryLocation | IDynamicLocation | null {
    return this._location
  }

  set location (location: IStationaryLocation | IDynamicLocation | null) {
    this._location = location
  }

  get contacts (): IContact[] {
    return this._contacts
  }

  set contacts (contacts: IContact[]) {
    this._contacts = contacts
  }

  get deviceMountActions (): DeviceMountAction[] {
    return this._deviceMountActions
  }

  set deviceMountActions (newDeviceMountActions: DeviceMountAction[]) {
    this._deviceMountActions = newDeviceMountActions
  }

  get deviceUnmountActions (): DeviceUnmountAction[] {
    return this._deviceUnmountActions
  }

  set deviceUnmountActions (newDeviceUnmountActions: DeviceUnmountAction[]) {
    this._deviceUnmountActions = newDeviceUnmountActions
  }

  get platformMountActions (): PlatformMountAction[] {
    return this._platformMountActions
  }

  set platformMountActions (newPlatformMountActions: PlatformMountAction[]) {
    this._platformMountActions = newPlatformMountActions
  }

  get platformUnmountActions (): PlatformUnmountAction[] {
    return this._platformUnmountActions
  }

  set platformUnmountActions (newPlatformUnmountActions: PlatformUnmountAction[]) {
    this._platformUnmountActions = newPlatformUnmountActions
  }

  get staticLocationBeginActions (): StaticLocationBeginAction[] {
    return this._staticLocationBeginActions
  }

  set staticLocationBeginActions (newActions: StaticLocationBeginAction[]) {
    this._staticLocationBeginActions = newActions
  }

  get staticLocationEndActions (): StaticLocationEndAction[] {
    return this._staticLocationEndActions
  }

  set staticLocationEndActions (newActions: StaticLocationEndAction[]) {
    this._staticLocationEndActions = newActions
  }

  get dynamicLocationBeginActions (): DynamicLocationBeginAction[] {
    return this._dynamicLocationBeginActions
  }

  set dynamicLocationBeginActions (newActions: DynamicLocationBeginAction[]) {
    this._dynamicLocationBeginActions = newActions
  }

  get dynamicLocationEndActions (): DynamicLocationEndAction[] {
    return this._dynamicLocationEndActions
  }

  set dynamicLocationEndActions (newActions: DynamicLocationEndAction[]) {
    this._dynamicLocationEndActions = newActions
  }

  get permissionGroup (): IPermissionGroup | null {
    return this._permissionGroup
  }

  set permissionGroup (permissionGroup: IPermissionGroup | null) {
    this._permissionGroup = permissionGroup
  }

  get createdAt (): DateTime | null {
    return this._createdAt
  }

  set createdAt (newCreatedAt: DateTime | null) {
    this._createdAt = newCreatedAt
  }

  get updatedAt (): DateTime | null {
    return this._updatedAt
  }

  set updatedAt (newUpdatedAt: DateTime | null) {
    this._updatedAt = newUpdatedAt
  }

  get createdBy (): IContact | null {
    return this._createdBy
  }

  set createdBy (user: IContact | null) {
    this._createdBy = user
  }

  get updatedBy (): IContact | null {
    return this._updatedBy
  }

  set updatedBy (user: IContact | null) {
    this._updatedBy = user
  }

  get createdByUserId (): string | null {
    return this._createdByUserId
  }

  set createdByUserId (newId: string | null) {
    this._createdByUserId = newId
  }

  get visibility (): Visibility {
    return this._visibility
  }

  set visibility (visibility: Visibility) {
    this._visibility = visibility
  }

  get isInternal (): boolean {
    return this._visibility === Visibility.Internal
  }

  get isPublic (): boolean {
    return this._visibility === Visibility.Public
  }

  static createFromObject (someObject: IConfiguration): Configuration {
    const newObject = new Configuration()

    newObject.id = someObject.id
    // luxon DateTime objects are immutable
    newObject.startDate = someObject.startDate
    newObject.endDate = someObject.endDate

    newObject.projectName = someObject.projectName
    newObject.projectUri = someObject.projectUri

    newObject.label = someObject.label
    newObject.status = someObject.status

    switch (true) {
      case someObject.location instanceof StationaryLocation:
        newObject.location = StationaryLocation.createFromObject(someObject.location as StationaryLocation)
        break
      case someObject.location instanceof DynamicLocation:
        newObject.location = DynamicLocation.createFromObject(someObject.location as DynamicLocation)
        break
    }
    newObject.contacts = someObject.contacts.map(Contact.createFromObject)
    newObject.deviceMountActions = someObject.deviceMountActions.map(DeviceMountAction.createFromObject)
    newObject.deviceUnmountActions = someObject.deviceUnmountActions.map(DeviceUnmountAction.createFromObject)
    newObject.platformMountActions = someObject.platformMountActions.map(PlatformMountAction.createFromObject)
    newObject.platformUnmountActions = someObject.platformUnmountActions.map(PlatformUnmountAction.createFromObject)
    newObject.staticLocationBeginActions = someObject.staticLocationBeginActions.map(StaticLocationBeginAction.createFromObject)
    newObject.staticLocationEndActions = someObject.staticLocationEndActions.map(StaticLocationEndAction.createFromObject)
    newObject.dynamicLocationBeginActions = someObject.dynamicLocationBeginActions.map(DynamicLocationBeginAction.createFromObject)
    newObject.dynamicLocationEndActions = someObject.dynamicLocationEndActions.map(DynamicLocationEndAction.createFromObject)

    newObject.permissionGroup = someObject.permissionGroup ? PermissionGroup.createFromObject(someObject.permissionGroup) : null

    newObject.createdAt = someObject.createdAt
    newObject.updatedAt = someObject.updatedAt
    newObject.createdBy = someObject.createdBy ? Contact.createFromObject(someObject.createdBy) : null
    newObject.updatedBy = someObject.updatedBy ? Contact.createFromObject(someObject.updatedBy) : null
    newObject.createdByUserId = someObject.createdByUserId

    newObject.visibility = someObject.visibility

    return newObject
  }
}
