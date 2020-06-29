import { PlatformOrDeviceType } from '../enums/PlatformOrDeviceType'

import Contact, { IContact } from './Contact'
import { DeviceProperty } from './DeviceProperty'
import { CustomTextField, ICustomTextField } from './CustomTextField'
import { IDeviceOrPlatformSearchObject } from './IDeviceOrPlatformSearchObject'
import Status from './Status'
import IPathSetter from './IPathSetter'

export interface IDevice {
  id: number | null
  persistentIdentifier: string
  shortName: string
  longName: string

  statusUri: string
  statusName: string

  manufacturerUri: string
  manufacturerName: string

  deviceTypeUri: string
  deviceTypeName: string

  model: string
  description: string
  website: string
  serialNumber: string
  inventoryNumber: string
  dualUse: boolean

  createdAt: Date | null
  modifiedAt: Date | null
  createdByUserId: number | null
  modifiedByUserId: number | null

  contacts: IContact[]
  properties: DeviceProperty[]
  customFields: ICustomTextField[]
}

export default class Device implements IDevice, IPathSetter {
  private _id: number | null = null
  private _persistentIdentifier: string = ''
  private _shortName: string = ''
  private _longName: string = ''

  private _statusUri: string = ''
  private _statusName: string = ''

  private _manufacturerUri: string = ''
  private _manufacturerName: string = ''

  private _deviceTypeUri: string = ''
  private _deviceTypeName: string = ''

  private _model: string = ''

  private _description: string = ''
  private _website: string = ''
  private _serialNumber: string = ''
  private _inventoryNumber: string = ''
  private _dualUse: boolean = false

  private _createdAt: Date | null = null
  private _modifiedAt: Date | null = null

  private _createdByUserId: number | null = null
  private _modifiedByUserId: number | null = null

  private _contacts: Contact[] = []
  private _properties: DeviceProperty[] = []
  private _customFields: CustomTextField[] = []

  // TODO: Attachments
  // TODO: Events

  get id (): number | null {
    return this._id
  }

  set id (id: number | null) {
    this._id = id
  }

  get persistentIdentifier (): string {
    return this._persistentIdentifier
  }

  set persistentIdentifier (persistentIdentifier: string) {
    this._persistentIdentifier = persistentIdentifier
  }

  get shortName (): string {
    return this._shortName
  }

  set shortName (shortName: string) {
    this._shortName = shortName
  }

  get longName (): string {
    return this._longName
  }

  set longName (longName: string) {
    this._longName = longName
  }

  get statusUri (): string {
    return this._statusUri
  }

  set statusUri (statusUri: string) {
    this._statusUri = statusUri
  }

  get statusName (): string {
    return this._statusName
  }

  set statusName (statusName: string) {
    this._statusName = statusName
  }

  get manufacturerUri (): string {
    return this._manufacturerUri
  }

  set manufacturerUri (manufacturerUri: string) {
    this._manufacturerUri = manufacturerUri
  }

  get manufacturerName (): string {
    return this._manufacturerName
  }

  set manufacturerName (manufacturerName: string) {
    this._manufacturerName = manufacturerName
  }

  get deviceTypeUri (): string {
    return this._deviceTypeUri
  }

  set deviceTypeUri (deviceTypeUri: string) {
    this._deviceTypeUri = deviceTypeUri
  }

  get deviceTypeName (): string {
    return this._deviceTypeName
  }

  set deviceTypeName (deviceTypeName: string) {
    this._deviceTypeName = deviceTypeName
  }

  get model (): string {
    return this._model
  }

  set model (model: string) {
    this._model = model
  }

  get description (): string {
    return this._description
  }

  set description (description: string) {
    this._description = description
  }

  get website (): string {
    return this._website
  }

  set website (website: string) {
    this._website = website
  }

  get serialNumber (): string {
    return this._serialNumber
  }

  set serialNumber (serialNumber: string) {
    this._serialNumber = serialNumber
  }

  get inventoryNumber (): string {
    return this._inventoryNumber
  }

  set inventoryNumber (inventoryNumber: string) {
    this._inventoryNumber = inventoryNumber
  }

  get dualUse (): boolean {
    return this._dualUse
  }

  set dualUse (dualUse: boolean) {
    this._dualUse = dualUse
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

  get contacts (): Contact[] {
    return this._contacts
  }

  set contacts (contacts: Contact[]) {
    this._contacts = contacts
  }

  get properties (): DeviceProperty[] {
    return this._properties
  }

  set properties (properties: DeviceProperty[]) {
    this._properties = properties
  }

  get customFields (): CustomTextField[] {
    return this._customFields
  }

  set customFields (customFields: CustomTextField[]) {
    this._customFields = customFields
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
      case 'persistentIdentifier':
        this.persistentIdentifier = String(value)
        break
      case 'shortName':
        this.shortName = String(value)
        break
      case 'longName':
        this.longName = String(value)
        break
      case 'statusUri':
        this.statusUri = String(value)
        break
      case 'statusName':
        this.statusName = String(value)
        break
      case 'manufacturerUri':
        this.manufacturerUri = String(value)
        break
      case 'manufacturerName':
        this.manufacturerName = String(value)
        break
      case 'deviceTypeUri':
        this.deviceTypeUri = String(value)
        break
      case 'deviceTypeName':
        this.deviceTypeName = String(value)
        break
      case 'model':
        this.model = String(value)
        break
      case 'description':
        this.description = String(value)
        break
      case 'website':
        this.website = String(value)
        break
      case 'serialNumber':
        this.serialNumber = String(value)
        break
      case 'inventoryNumber':
        this.inventoryNumber = String(value)
        break
      case 'dualUse':
        this.dualUse = Boolean(value)
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
      case 'properties':
        this.properties = value.map(DeviceProperty.createFromObject)
        break
      case 'customFields':
        this.customFields = value.map(CustomTextField.createFromObject)
        break
      default:
        throw new TypeError('path ' + path + ' is not valid')
    }
  }

  static createFromObject (someObject: IDevice): Device {
    const newObject = new Device()

    newObject.id = someObject.id
    newObject.persistentIdentifier = someObject.persistentIdentifier
    newObject.shortName = someObject.shortName
    newObject.longName = someObject.longName

    newObject.statusUri = someObject.statusUri
    newObject.statusName = someObject.statusName

    newObject.manufacturerUri = someObject.manufacturerUri
    newObject.manufacturerName = someObject.manufacturerName

    newObject.deviceTypeUri = someObject.deviceTypeUri
    newObject.deviceTypeName = someObject.deviceTypeName

    newObject.model = someObject.model
    newObject.description = someObject.description
    newObject.website = someObject.website
    newObject.serialNumber = someObject.serialNumber
    newObject.inventoryNumber = someObject.inventoryNumber
    newObject.dualUse = someObject.dualUse

    newObject.createdAt = someObject.createdAt
    newObject.modifiedAt = someObject.modifiedAt
    newObject.createdByUserId = someObject.createdByUserId
    newObject.modifiedByUserId = someObject.modifiedByUserId

    newObject.contacts = someObject.contacts.map(Contact.createFromObject)
    newObject.properties = someObject.properties.map(DeviceProperty.createFromObject)
    newObject.customFields = someObject.customFields.map(CustomTextField.createFromObject)

    return newObject
  }

  toSearchObject (statusLookupByUri: Map<string, Status>) : IDeviceOrPlatformSearchObject {
    return new DeviceSearchObjectWrapper(this, statusLookupByUri)
  }
}

class DeviceSearchObjectWrapper implements IDeviceOrPlatformSearchObject {
  private device: Device
  private statusLookupByUri: Map<string, Status>

  constructor (device: Device, statusLookupByUri: Map<string, Status>) {
    this.device = device
    this.statusLookupByUri = statusLookupByUri
  }

  get id () : number | null {
    return this.device.id
  }

  get name () : string {
    return this.device.shortName
  }

  get type () : string {
    return 'Device'
  }

  get searchType () : PlatformOrDeviceType {
    return PlatformOrDeviceType.DEVICE
  }

  get project (): string {
    // TODO
    return 'No project yet'
  }

  get status () : string {
    if (this.statusLookupByUri.has(this.device.statusUri)) {
      const status: Status = this.statusLookupByUri.get(this.device.statusUri) as Status
      return status.name
    }
    if (this.device.statusName) {
      return this.device.statusName
    }
    return 'Unknow status'
  }
}
