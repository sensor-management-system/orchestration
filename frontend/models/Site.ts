/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2023
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Tim Eder <tim.eder@ufz.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 * - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
import { DateTime } from 'luxon'

import { Image, IImage } from '@/models/Image'
import { IContact, Contact } from '@/models/Contact'
import { PermissionGroup, IPermissionGroup, IPermissionableMultipleGroups } from '@/models/PermissionGroup'

import { Visibility, IVisible } from '@/models/Visibility'
import { IMetaCreationInfo } from '@/models/MetaCreationInfo'

export interface ILatLng {
  lat: number,
  lng: number
}

export interface IAddress {
  street?: string
  streetNumber?: string
  city?: string
  zipCode?: string
  country?: string
  building?: string
  room?: string
}

export interface ISite extends IPermissionableMultipleGroups, IMetaCreationInfo {
  id: string
  persistentIdentifier: string
  label: string
  geometry: ILatLng[]
  description: string
  epsgCode: string
  address: IAddress
  archived: boolean
  contacts: IContact[]
  configurationIds: string[]

  siteUsageUri: string
  siteUsageName: string

  siteTypeUri: string
  siteTypeName: string

  createdAt: DateTime | null
  updatedAt: DateTime | null
  createdBy: IContact | null
  updatedBy: IContact | null
  createdByUserId: string | null
  updateDescription: string
  visibility: Visibility
  permissionGroups: IPermissionGroup[]
  images: IImage[]
  website: string
  keywords: string[]

  outerSiteId: string | null
}

export class Site implements ISite, IVisible {
  private _id: string = ''
  private _persistentIdentifier: string = ''
  private _label: string = ''
  private _geometry: ILatLng[] = []
  private _description: string = ''
  private _epsgCode: string = '4326'
  private _address: IAddress = {}
  private _archived: boolean = false
  private _contacts: IContact[] = [] as IContact[]
  private _configurationIds: string[] = []

  private _siteUsageUri: string = ''
  private _siteUsageName: string = ''
  private _siteTypeUri: string = ''
  private _siteTypeName: string = ''

  private _createdAt: DateTime | null = null
  private _updatedAt: DateTime | null = null
  private _createdBy: IContact | null = null
  private _updatedBy: IContact | null = null
  private _createdByUserId: string | null = null
  private _updateDescription: string = ''

  private _visibility: Visibility = Visibility.Internal
  private _permissionGroups: PermissionGroup[] = []
  private _images: Image[] = []
  private _website: string = ''
  private _keywords: string[] = []
  private _outerSiteId: string | null = null

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

  get label (): string {
    return this._label
  }

  set label (label: string) {
    this._label = label
  }

  get geometry (): ILatLng[] {
    return this._geometry
  }

  set geometry (geometry: ILatLng[]) {
    this._geometry = geometry
  }

  get description (): string {
    return this._description
  }

  set description (newDescription: string) {
    this._description = newDescription
  }

  get epsgCode (): string {
    return this._epsgCode
  }

  set epsgCode (epsgCode: string) {
    this._epsgCode = epsgCode
  }

  get address (): IAddress {
    return this._address
  }

  set address (newAddress: IAddress) {
    this._address = newAddress
  }

  get contacts (): IContact[] {
    return this._contacts
  }

  set contacts (contacts: IContact[]) {
    this._contacts = contacts
  }

  get configurationIds (): string[] {
    return this._configurationIds
  }

  set configurationIds (configurationIds: string[]) {
    this._configurationIds = configurationIds
  }

  get siteUsageName (): string {
    return this._siteUsageName
  }

  set siteUsageName (siteUsageName: string) {
    this._siteUsageName = siteUsageName
  }

  get siteUsageUri (): string {
    return this._siteUsageUri
  }

  set siteUsageUri (siteUsageUri: string) {
    this._siteUsageUri = siteUsageUri
  }

  get siteTypeName (): string {
    return this._siteTypeName
  }

  set siteTypeName (siteTypeName: string) {
    this._siteTypeName = siteTypeName
  }

  get siteTypeUri (): string {
    return this._siteTypeUri
  }

  set siteTypeUri (siteTypeUri: string) {
    this._siteTypeUri = siteTypeUri
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

  get updateDescription (): string {
    return this._updateDescription
  }

  set updateDescription (newUpdateDescription: string) {
    this._updateDescription = newUpdateDescription
  }

  get visibility (): Visibility {
    return this._visibility
  }

  set visibility (visibility: Visibility) {
    this._visibility = visibility
  }

  get permissionGroups (): PermissionGroup[] {
    return this._permissionGroups
  }

  set permissionGroups (permissionGroups: PermissionGroup[]) {
    this._permissionGroups = permissionGroups
  }

  set images (images: Image[]) {
    this._images = images
  }

  get images (): Image[] {
    return this._images
  }

  get website (): string {
    return this._website
  }

  set website (newWebsite: string) {
    this._website = newWebsite
  }

  get keywords (): string[] {
    return this._keywords
  }

  set keywords (newKeywords: string[]) {
    this._keywords = newKeywords
  }

  // get isPrivate (): boolean {
  //   return this._visibility === Visibility.Private
  // }

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

  get outerSiteId (): string | null {
    return this._outerSiteId
  }

  set outerSiteId (newOuterSiteId: string | null) {
    this._outerSiteId = newOuterSiteId
  }

  get type (): string {
    return 'site'
  }

  toString (): string {
    return this._label
  }

  static createFromObject (someObject: ISite): Site {
    const newObject = new Site()
    newObject.id = someObject.id
    newObject.persistentIdentifier = someObject.persistentIdentifier
    newObject.label = someObject.label
    newObject.geometry = [...someObject.geometry]
    newObject.description = someObject.description
    newObject.epsgCode = someObject.epsgCode
    newObject.address = { ...someObject.address }
    newObject.archived = someObject.archived
    newObject.contacts = someObject.contacts.map(Contact.createFromObject)

    newObject.siteUsageName = someObject.siteUsageName
    newObject.siteUsageUri = someObject.siteUsageUri

    newObject.siteTypeName = someObject.siteTypeName
    newObject.siteTypeUri = someObject.siteTypeUri

    newObject.createdAt = someObject.createdAt
    newObject.updatedAt = someObject.updatedAt
    newObject.createdBy = someObject.createdBy ? Contact.createFromObject(someObject.createdBy) : null
    newObject.updatedBy = someObject.updatedBy ? Contact.createFromObject(someObject.updatedBy) : null
    newObject.updateDescription = someObject.updateDescription
    newObject.visibility = someObject.visibility
    newObject.permissionGroups = someObject.permissionGroups.map(PermissionGroup.createFromObject)

    newObject.images = someObject.images.map(Image.createFromObject)
    newObject.website = someObject.website
    newObject.keywords = [...someObject.keywords]

    newObject.outerSiteId = someObject.outerSiteId

    return newObject
  }
}
