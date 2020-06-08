import { PlatformOrDeviceType } from '../enums/PlatformOrDeviceType'

import Contact from './Contact'
import { DeviceProperty } from './DeviceProperty'
import { CustomTextField } from './CustomTextField'
import { IDeviceOrPlatformSearchObject } from './IDeviceOrPlatformSearchObject'

export default class Device {
  private _id: number | null = null
  private _persistentIdentifier: string = ''
  private _label: string = ''
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

  private _contacts: Contact[] = []
  private _properties: DeviceProperty[] = []
  private _customFields: CustomTextField[] = []

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

  get label (): string {
    return this._label
  }

  set label (label: string) {
    this._label = label
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

  get urn () {
    let urn = ''
    // TODO: how to add the manufacturer if we just want to have the uri in the model?
    urn += this.manufacturerName || ''
    urn += this.model ? '_' + this.model : ''
    urn += this.serialNumber ? '_' + this.serialNumber : ''
    return urn
  }

  toSearchObject () : IDeviceOrPlatformSearchObject {
    return new DeviceSearchObjectWrapper(this)
  }
}

class DeviceSearchObjectWrapper implements IDeviceOrPlatformSearchObject {
  private device: Device

  constructor (device: Device) {
    this.device = device
  }

  get id () : number | null {
    return this.device.id
  }

  get name () : string {
    return this.device.label
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
    // TODO
    return this.device.statusName
  }
}
