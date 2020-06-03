import { PlatformOrDeviceType } from '../enums/PlatformOrDeviceType'

import Contact from './Contact'

import { IDeviceOrPlatformSearchObject } from './IDeviceOrPlatformSearchObject'
import PlatformType from './PlatformType'
import PlatformStatus from './PlatformStatus'

export default class Platform {
  private _id: number | null = null
  private _platformTypeUri: string = ''
  private _shortName: string = ''
  private _longName: string = ''
  private _description: string = ''
  private _manufacturerUri: string = ''
  private _model: string = ''
  private _platformStatusUri: string = ''
  private _inventoryNumber: string = ''
  private _serialNumber: string = ''
  private _website: string = ''
  private _persistentIdentifier: string = ''
  private _createdAt: Date | null = null
  private _modifiedAt: Date | null = null
  /*
  private _createdByUserId: number | null = null
  private _modifiedByUserId: number | null = null
  */

  private _contacts: Contact[] = []

  get id (): number | null {
    return this._id
  }

  set id (newId: number | null) {
    this._id = newId
  }

  get platformTypeUri (): string {
    return this._platformTypeUri
  }

  set platformTypeUri (newPlatformTypeUri: string) {
    this._platformTypeUri = newPlatformTypeUri
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

  get model (): string {
    return this._model
  }

  set model (newModel: string) {
    this._model = newModel
  }

  get platformStatusUri (): string {
    return this._platformStatusUri
  }

  set platformStatusUri (newPlatformStatusUri: string) {
    this._platformStatusUri = newPlatformStatusUri
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

  get createdAt (): Date | null {
    return this._createdAt
  }

  set createdAt (newCreatedAt: Date | null) {
    this._createdAt = newCreatedAt
  }

  get modifiedAt (): Date | null {
    return this._modifiedAt
  }

  set modifiedAt (newModifiedAt: Date | null) {
    this._modifiedAt = newModifiedAt
  }

  /*
  get createdByUserId (): number | null {
    return this._createdByUserId
  }

  set createdByUserId (newCreatedByUserId: number | null) {
    this._createdByUserId = newCreatedByUserId
  }

  get modifiedByUserId (): number | null {
    return this._modifiedByUserId
  }

  set modifiedByUserId (newModifiedByUserId: number | null) {
    this._modifiedByUserId = newModifiedByUserId
  }
  */

  toSearchObject (
    platformTypeLookupByUri: Map<string, PlatformType>,
    platformStatusLookupByUri: Map<string, PlatformStatus>
  ) : IDeviceOrPlatformSearchObject {
    return new PlatformSearchObjectWrapper(this, platformTypeLookupByUri, platformStatusLookupByUri)
  }

  static createEmpty (): Platform {
    return new Platform()
  }
}

class PlatformSearchObjectWrapper implements IDeviceOrPlatformSearchObject {
  private platform: Platform
  private platformTypeLookupByUri: Map<string, PlatformType>
  private platformStatusLookupByUri: Map<string, PlatformStatus>

  constructor (platform: Platform, platformTypeLookupByUri: Map<string, PlatformType>, platformStatusLookupByUri: Map<string, PlatformStatus>) {
    this.platform = platform
    this.platformTypeLookupByUri = platformTypeLookupByUri
    this.platformStatusLookupByUri = platformStatusLookupByUri
  }

  get id () : number | null {
    return this.platform.id
  }

  get name () : string {
    return this.platform.shortName
  }

  get type () : string {
    // TODO: As we don't have the platform types
    // we can't give the exact type for the uri
    if (this.platformTypeLookupByUri.has(this.platform.platformTypeUri)) {
      const platformType: PlatformType = this.platformTypeLookupByUri.get(this.platform.platformTypeUri) as PlatformType
      return platformType.name
    }
    return 'Unknown type'
  }

  get searchType () : PlatformOrDeviceType {
    return PlatformOrDeviceType.PLATFORM
  }

  get project (): string {
    // TODO
    return 'No project yet'
  }

  get status () : string {
    if (this.platformStatusLookupByUri.has(this.platform.platformStatusUri)) {
      const platformStatus: PlatformStatus = this.platformStatusLookupByUri.get(this.platform.platformStatusUri) as PlatformStatus
      return platformStatus.name
    }
    // TODO
    return 'Unknown status'
  }
}
