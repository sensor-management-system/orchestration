import Contact, { IContact } from '@/models/Contact'
import { DeviceProperty } from '@/models/DeviceProperty'
import { CustomTextField, ICustomTextField } from '@/models/CustomTextField'

import { Attachment, IAttachment } from '@/models/Attachment'

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
  attachments: IAttachment[]
}

export default class Device implements IDevice {
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
  private _attachments: Attachment[] = []

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

  get attachments (): Attachment[] {
    return this._attachments
  }

  set attachments (attachments: Attachment[]) {
    this._attachments = attachments
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
    newObject.attachments = someObject.attachments.map(Attachment.createFromObject)

    return newObject
  }
}
