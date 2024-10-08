/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2023
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Tim Eder <tim.eder@ufz.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
import { DateTime } from 'luxon'

import { Image, IImage } from '@/models/Image'
import { Attachment, IAttachment } from '@/models/Attachment'
import { IContact, Contact } from '@/models/Contact'
import { IMetaCreationInfo } from '@/models/MetaCreationInfo'
import { Parameter, IParameter } from '@/models/Parameter'
import { PermissionGroup, IPermissionGroup, IPermissionableMultipleGroups } from '@/models/PermissionGroup'
import { Visibility, IVisible } from '@/models/Visibility'

export interface IPlatform extends IPermissionableMultipleGroups, IMetaCreationInfo {
  id: string | null

  platformTypeUri: string
  platformTypeName: string

  shortName: string
  longName: string
  description: string

  manufacturerUri: string
  manufacturerName: string

  model: string

  statusUri: string
  statusName: string

  inventoryNumber: string
  serialNumber: string
  website: string
  persistentIdentifier: string

  archived: boolean
  country: string

  createdAt: DateTime | null
  updatedAt: DateTime | null

  createdBy: IContact | null
  updatedBy: IContact | null
  updateDescription: string

  /*
    You may wonder why there is an extra createdByUserId entry here.
    The reason is that we use the createBy & updatedBy to show
    information about the contact that are responsible for the changes.
    Here we refer to the user object (which can have different ids).
  */
  createdByUserId: string | null

  contacts: IContact[]
  attachments: IAttachment[]
  images: IImage[]
  parameters: IParameter[]
  permissionGroups: IPermissionGroup[]
  keywords: string[]

  visibility: Visibility
}

export class Platform implements IPlatform, IVisible {
  private _id: string | null = null

  private _platformTypeUri: string = ''
  private _platformTypeName: string = ''

  private _shortName: string = ''
  private _longName: string = ''
  private _description: string = ''

  private _manufacturerUri: string = ''
  private _manufacturerName: string = ''

  private _model: string = ''

  private _statusUri: string = ''
  private _statusName: string = ''

  private _inventoryNumber: string = ''
  private _serialNumber: string = ''
  private _website: string = ''
  private _persistentIdentifier: string = ''

  private _archived: boolean = false
  private _country: string = ''
  private _createdAt: DateTime | null = null
  private _updatedAt: DateTime | null = null

  private _createdBy: IContact | null = null
  private _updatedBy: IContact | null = null
  private _updateDescription: string = ''

  private _createdByUserId: string | null = null

  private _contacts: Contact[] = []
  private _images: Image[] = []
  private _attachments: Attachment[] = []
  private _parameters: Parameter[] = []
  private _permissionGroups: PermissionGroup[] = []
  private _keywords: string[] = []

  private _visibility: Visibility = Visibility.Internal

  get id (): string | null {
    return this._id
  }

  set id (newId: string | null) {
    this._id = newId
  }

  get platformTypeUri (): string {
    return this._platformTypeUri
  }

  set platformTypeUri (newPlatformTypeUri: string) {
    this._platformTypeUri = newPlatformTypeUri
  }

  get platformTypeName (): string {
    return this._platformTypeName
  }

  set platformTypeName (newPlatformTypeName: string) {
    this._platformTypeName = newPlatformTypeName
  }

  get shortName (): string {
    return this._shortName
  }

  set shortName (newShortName: string) {
    this._shortName = newShortName
  }

  get longName (): string {
    return this._longName
  }

  set longName (newLongName: string) {
    this._longName = newLongName
  }

  get description (): string {
    return this._description
  }

  set description (newDescription: string) {
    this._description = newDescription
  }

  get manufacturerUri (): string {
    return this._manufacturerUri
  }

  set manufacturerUri (newManufacturerUri: string) {
    this._manufacturerUri = newManufacturerUri
  }

  get manufacturerName (): string {
    return this._manufacturerName
  }

  set manufacturerName (newManufacturerName: string) {
    this._manufacturerName = newManufacturerName
  }

  get model (): string {
    return this._model
  }

  set model (newModel: string) {
    this._model = newModel
  }

  get statusUri (): string {
    return this._statusUri
  }

  set statusUri (newStatusUri: string) {
    this._statusUri = newStatusUri
  }

  get statusName (): string {
    return this._statusName
  }

  set statusName (newStatusName: string) {
    this._statusName = newStatusName
  }

  get inventoryNumber (): string {
    return this._inventoryNumber
  }

  set inventoryNumber (newInventoryNumber: string) {
    this._inventoryNumber = newInventoryNumber
  }

  get serialNumber (): string {
    return this._serialNumber
  }

  set serialNumber (newSerialNumber: string) {
    this._serialNumber = newSerialNumber
  }

  get website (): string {
    return this._website
  }

  set website (newWebsite: string) {
    this._website = newWebsite
  }

  get contacts (): Contact[] {
    return this._contacts
  }

  set contacts (newContacts: Contact[]) {
    this._contacts = newContacts
  }

  get persistentIdentifier (): string {
    return this._persistentIdentifier
  }

  set persistentIdentifier (newPersistentIdentifier: string) {
    this._persistentIdentifier = newPersistentIdentifier
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

  set images (images: Image[]) {
    this._images = images
  }

  get images (): Image[] {
    return this._images
  }

  get attachments (): Attachment[] {
    return this._attachments
  }

  set attachments (attachments: Attachment[]) {
    this._attachments = attachments
  }

  get parameters (): Parameter[] {
    return this._parameters
  }

  set parameters (parameters: Parameter[]) {
    this._parameters = parameters
  }

  get permissionGroups (): PermissionGroup[] {
    return this._permissionGroups
  }

  set permissionGroups (permissionGroups: PermissionGroup[]) {
    this._permissionGroups = permissionGroups
  }

  get keywords (): string[] {
    return this._keywords
  }

  set keywords (newKeywords: string[]) {
    this._keywords = newKeywords
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

  get isPrivate (): boolean {
    return this._visibility === Visibility.Private
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

  get country (): string {
    return this._country
  }

  set country (newCountry: string) {
    this._country = newCountry
  }

  get type (): string {
    return 'platform'
  }

  static createEmpty (): Platform {
    return new Platform()
  }

  static createFromObject (someObject: IPlatform): Platform {
    const newObject = new Platform()

    newObject.id = someObject.id

    newObject.platformTypeUri = someObject.platformTypeUri
    newObject.platformTypeName = someObject.platformTypeName

    newObject.shortName = someObject.shortName
    newObject.longName = someObject.longName

    newObject.description = someObject.description

    newObject.manufacturerUri = someObject.manufacturerUri
    newObject.manufacturerName = someObject.manufacturerName

    newObject.model = someObject.model

    newObject.statusUri = someObject.statusUri
    newObject.statusName = someObject.statusName

    newObject.inventoryNumber = someObject.inventoryNumber
    newObject.serialNumber = someObject.serialNumber
    newObject.website = someObject.website
    newObject.persistentIdentifier = someObject.persistentIdentifier

    newObject.createdAt = someObject.createdAt
    newObject.updatedAt = someObject.updatedAt
    newObject.updateDescription = someObject.updateDescription

    newObject.createdBy = someObject.createdBy
    newObject.updatedBy = someObject.updatedBy
    newObject.contacts = someObject.contacts.map(Contact.createFromObject)
    newObject.attachments = someObject.attachments.map(Attachment.createFromObject)
    newObject.images = someObject.images.map(Image.createFromObject)
    newObject.parameters = someObject.parameters.map(Parameter.createFromObject)
    newObject.permissionGroups = someObject.permissionGroups.map(PermissionGroup.createFromObject)
    newObject.keywords = [...someObject.keywords]
    newObject.createdByUserId = someObject.createdByUserId

    newObject.visibility = someObject.visibility

    newObject.archived = someObject.archived
    newObject.country = someObject.country

    return newObject
  }
}
