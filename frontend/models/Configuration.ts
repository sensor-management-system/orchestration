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

import { Image, IImage } from '@/models/Image'
import { IContact, Contact } from '@/models/Contact'
import { IMountActions } from '@/models/IMountActions'
import { DeviceMountAction } from '@/models/DeviceMountAction'
import { PlatformMountAction } from '@/models/PlatformMountAction'
import { PermissionGroup, IPermissionGroup, IPermissionableSingleGroup } from '@/models/PermissionGroup'
import { Visibility, IVisible } from '@/models/Visibility'
import { Parameter, IParameter } from '@/models/Parameter'

export interface IConfiguration extends IMountActions, IPermissionableSingleGroup {
  id: string
  persistentIdentifier: string
  startDate: DateTime | null
  endDate: DateTime | null
  label: string
  description: string
  project: string
  campaign: string
  status: string
  archived: boolean
  contacts: IContact[]
  parameters: IParameter[]
  images: IImage[]
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
  siteId?: string
  keywords: string[]
}

export class Configuration implements IConfiguration, IVisible {
  private _id: string = ''
  private _persistentIdentifier: string = ''
  private _startDate: DateTime | null = null
  private _endDate: DateTime | null = null
  private _label: string = ''
  private _description: string = ''
  private _project: string = ''
  private _campaign: string = ''
  private _status: string = ''
  private _archived: boolean = false
  private _contacts: IContact[] = [] as IContact[]
  private _parameters: Parameter[] = []
  private _images: Image[] = []
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
  private _siteId: string = ''
  private _keywords: string[] = []

  get id (): string {
    return this._id
  }

  set id (id: string) {
    this._id = id
  }

  get persistentIdentifier (): string {
    return this._persistentIdentifier
  }

  set persistentIdentifier (persistentIdentifier: string) {
    this._persistentIdentifier = persistentIdentifier
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

  get description (): string {
    return this._description
  }

  set description (newDescription: string) {
    this._description = newDescription
  }

  get project (): string {
    return this._project
  }

  set project (newProject: string) {
    this._project = newProject
  }

  get campaign (): string {
    return this._campaign
  }

  set campaign (newCampaign: string) {
    this._campaign = newCampaign
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

  get parameters (): Parameter[] {
    return this._parameters
  }

  set images (images: Image[]) {
    this._images = images
  }

  get images (): Image[] {
    return this._images
  }

  set parameters (parameters: Parameter[]) {
    this._parameters = parameters
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

  get siteId (): string {
    return this._siteId
  }

  set siteId (id: string) {
    this._siteId = id
  }

  get keywords (): string[] {
    return this._keywords
  }

  set keywords (newKeywords: string[]) {
    this._keywords = newKeywords
  }

  static createFromObject (someObject: IConfiguration): Configuration {
    const newObject = new Configuration()

    newObject.id = someObject.id
    newObject.persistentIdentifier = someObject.persistentIdentifier
    // luxon DateTime objects are immutable
    newObject.startDate = someObject.startDate
    newObject.endDate = someObject.endDate

    newObject.label = someObject.label
    newObject.description = someObject.description
    newObject.project = someObject.project
    newObject.campaign = someObject.campaign
    newObject.status = someObject.status

    newObject.contacts = someObject.contacts.map(Contact.createFromObject)
    newObject.deviceMountActions = someObject.deviceMountActions.map(DeviceMountAction.createFromObject)
    newObject.platformMountActions = someObject.platformMountActions.map(PlatformMountAction.createFromObject)

    newObject.parameters = someObject.parameters.map(Parameter.createFromObject)
    newObject.images = someObject.images.map(Image.createFromObject)
    newObject.permissionGroup = someObject.permissionGroup ? PermissionGroup.createFromObject(someObject.permissionGroup) : null

    newObject.createdAt = someObject.createdAt
    newObject.updatedAt = someObject.updatedAt
    newObject.updateDescription = someObject.updateDescription
    newObject.createdBy = someObject.createdBy ? Contact.createFromObject(someObject.createdBy) : null
    newObject.updatedBy = someObject.updatedBy ? Contact.createFromObject(someObject.updatedBy) : null
    newObject.createdByUserId = someObject.createdByUserId

    newObject.visibility = someObject.visibility
    newObject.archived = someObject.archived

    newObject.siteId = someObject.siteId ?? ''
    newObject.keywords = [...someObject.keywords]

    return newObject
  }
}
