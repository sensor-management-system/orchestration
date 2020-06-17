import { PlatformOrDeviceType } from '../enums/PlatformOrDeviceType'

import Contact from './Contact'
import { DeviceProperty } from './DeviceProperty'
import { CustomTextField } from './CustomTextField'
import { Attachment } from './Attachment'
import { IDeviceOrPlatformSearchObject } from './IDeviceOrPlatformSearchObject'
import Status from './Status'

export default class Device {
  private _id: number | null = null
  private _persistentIdentifier: string = ''
  private _shortName: string = ''
  private _longName: string = ''

  private _statusUri: string = ''
  private _statusName: string = ''

  private _manufacturerUri: string = ''
  private _manufacturerName: string = ''
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
