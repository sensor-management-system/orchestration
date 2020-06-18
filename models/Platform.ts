import { PlatformOrDeviceType } from '../enums/PlatformOrDeviceType'

import Contact, { IContact } from './Contact'

import { IDeviceOrPlatformSearchObject } from './IDeviceOrPlatformSearchObject'
import PlatformType from './PlatformType'
import Status from './Status'
import IPathSetter from './IPathSetter'

export interface IPlatform {
  id: number | null

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

  createdAt: Date | null
  modifiedAt: Date | null

  createdByUserId: number | null
  modifiedByUserId: number | null

  contacts: IContact[]
}

export default class Platform implements IPlatform, IPathSetter {
  private _id: number | null = null

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
  private _createdAt: Date | null = null
  private _modifiedAt: Date | null = null

  private _createdByUserId: number | null = null
  private _modifiedByUserId: number | null = null

  private _contacts: Contact[] = []
  // TODO: Add attachments

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

  setPath (path: string, value: any): void {
    const pathArray = path.split('.')
    const topLevelElement = pathArray.splice(0, 1)[0]

    switch (topLevelElement) {
      case 'id':
        if (value !== null) {
          this.id = Number(value)
        } else {
          this.id = null
        }
        break
      case 'platformTypeUri':
        this.platformTypeUri = String(value)
        break
      case 'platformTypeName':
        this.platformTypeName = String(value)
        break
      case 'shortName':
        this.shortName = String(value)
        break
      case 'longName':
        this.longName = String(value)
        break
      case 'description':
        this.description = String(value)
        break
      case 'manufacturerUri':
        this.manufacturerUri = String(value)
        break
      case 'manufacturerName':
        this.manufacturerName = String(value)
        break
      case 'model':
        this.model = String(value)
        break
      case 'statusUri':
        this.statusUri = String(value)
        break
      case 'statusName':
        this.statusName = String(value)
        break
      case 'inventoryNumber':
        this.inventoryNumber = String(value)
        break
      case 'serialNumber':
        this.serialNumber = String(value)
        break
      case 'website':
        this.website = String(value)
        break
      case 'persistentIdentifier':
        this.persistentIdentifier = String(value)
        break
      case 'createdAt':
        if (value !== null) {
          this.createdAt = value as Date
        } else {
          this.createdAt = null
        }
        break
      case 'modifiedAt':
        if (value !== null) {
          this.modifiedAt = value as Date
        } else {
          this.modifiedAt = null
        }
        break
      case 'createdByUserId':
        if (value !== null) {
          this.createdByUserId = Number(value)
        } else {
          this.createdByUserId = null
        }
        break
      case 'modifiedByUserId':
        if (value !== null) {
          this.modifiedByUserId = Number(value)
        } else {
          this.modifiedByUserId = null
        }
        break
      case 'contacts':
        this.contacts = value.map(Contact.createFromObject)
        break
      default:
        throw new TypeError('path ' + path + ' is not valid')
    }
  }

  toSearchObject (
    platformTypeLookupByUri: Map<string, PlatformType>,
    platformStatusLookupByUri: Map<string, Status>
  ) : IDeviceOrPlatformSearchObject {
    return new PlatformSearchObjectWrapper(this, platformTypeLookupByUri, platformStatusLookupByUri)
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
    newObject.modifiedAt = someObject.modifiedAt

    newObject.createdByUserId = someObject.createdByUserId
    newObject.modifiedByUserId = someObject.modifiedByUserId

    newObject.contacts = someObject.contacts.map(Contact.createFromObject)

    return newObject
  }
}

class PlatformSearchObjectWrapper implements IDeviceOrPlatformSearchObject {
  private platform: Platform
  private platformTypeLookupByUri: Map<string, PlatformType>
  private statusLookupByUri: Map<string, Status>

  constructor (platform: Platform, platformTypeLookupByUri: Map<string, PlatformType>, statusLookupByUri: Map<string, Status>) {
    this.platform = platform
    this.platformTypeLookupByUri = platformTypeLookupByUri
    this.statusLookupByUri = statusLookupByUri
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
    if (this.platform.platformTypeName) {
      return this.platform.platformTypeName
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
    if (this.statusLookupByUri.has(this.platform.statusUri)) {
      const platformStatus: Status = this.statusLookupByUri.get(this.platform.statusUri) as Status
      return platformStatus.name
    }
    if (this.platform.statusName) {
      return this.platform.statusName
    }
    return 'Unknown status'
  }
}
