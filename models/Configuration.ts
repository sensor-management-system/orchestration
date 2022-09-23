/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020-2022
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
import { PlatformMountAction } from '@/models/PlatformMountAction'
import { PermissionGroup, IPermissionGroup, IPermissionableSingleGroup } from '@/models/PermissionGroup'
import { Visibility, IVisible } from '@/models/Visibility'

export interface IConfiguration extends IMountActions, IPermissionableSingleGroup {
  id: string
  startDate: DateTime | null
  endDate: DateTime | null
  label: string
  status: string
  archived: boolean
  contacts: IContact[]
  createdAt: DateTime | null
  updatedAt: DateTime | null
  updateDescription: string
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
  private _label: string = ''
  private _status: string = ''
  private _archived: boolean = false
  private _contacts: IContact[] = [] as IContact[]
  private _deviceMountActions: DeviceMountAction[] = []
  private _platformMountActions: PlatformMountAction[] = []
  private _permissionGroup: IPermissionGroup | null = null
  private _createdAt: DateTime | null = null
  private _updatedAt: DateTime | null = null
  private _updateDescription: string = ''
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

  get platformMountActions (): PlatformMountAction[] {
    return this._platformMountActions
  }

  set platformMountActions (newPlatformMountActions: PlatformMountAction[]) {
    this._platformMountActions = newPlatformMountActions
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

  get updateDescription (): string {
    return this._updateDescription
  }

  set updateDescription (newDescription: string) {
    this._updateDescription = newDescription
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

  get archived (): boolean {
    return this._archived
  }

  set archived (newValue: boolean) {
    this._archived = newValue
  }

  get type (): string {
    return 'configuration'
  }

  static createFromObject (someObject: IConfiguration): Configuration {
    const newObject = new Configuration()

    newObject.id = someObject.id
    // luxon DateTime objects are immutable
    newObject.startDate = someObject.startDate
    newObject.endDate = someObject.endDate

    newObject.label = someObject.label
    newObject.status = someObject.status

    newObject.contacts = someObject.contacts.map(Contact.createFromObject)
    newObject.deviceMountActions = someObject.deviceMountActions.map(DeviceMountAction.createFromObject)
    newObject.platformMountActions = someObject.platformMountActions.map(PlatformMountAction.createFromObject)

    newObject.permissionGroup = someObject.permissionGroup ? PermissionGroup.createFromObject(someObject.permissionGroup) : null

    newObject.createdAt = someObject.createdAt
    newObject.updatedAt = someObject.updatedAt
    newObject.updateDescription = someObject.updateDescription
    newObject.createdBy = someObject.createdBy ? Contact.createFromObject(someObject.createdBy) : null
    newObject.updatedBy = someObject.updatedBy ? Contact.createFromObject(someObject.updatedBy) : null
    newObject.createdByUserId = someObject.createdByUserId

    newObject.visibility = someObject.visibility
    newObject.archived = someObject.archived

    return newObject
  }
}
