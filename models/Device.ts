import { PlatformOrDeviceType } from '../enums/PlatformOrDeviceType'

import Contact from './Contact'
import { DeviceProperty } from './DeviceProperty'
import { CustomTextField } from './CustomTextField'
import { IDeviceOrPlatformSearchObject } from './IDeviceOrPlatformSearchObject'

export default class Device {
  private _id: number | null = null
  private _persistentId: string = ''
  private _label: string = ''
  private _state: string = ''
  private _type: string = ''
  private _manufacturerUri: string = ''
  private _model: string = ''
  private _description: string = ''
  private _urlWebsite: string = ''
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

  get persistentId (): string {
    return this._persistentId
  }

  set persistentId (persistentId: string) {
    this._persistentId = persistentId
  }

  get label (): string {
    return this._label
  }

  set label (label: string) {
    this._label = label
  }

  get state (): string {
    return this._state
  }

  set state (state: string) {
    this._state = state
  }

  get type (): string {
    return this._type
  }

  set type (type: string) {
    this._type = type
  }

  get manufacturerUri (): string {
    return this._manufacturerUri
  }

  set manufacturerUri (manufacturerUri: string) {
    this._manufacturerUri = manufacturerUri
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

  get urlWebsite (): string {
    return this._urlWebsite
  }

  set urlWebsite (urlWebsite: string) {
    this._urlWebsite = urlWebsite
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
    urn += this.manufacturerUri || ''
    urn += this.model ? '_' + this.model : ''
    urn += this.type ? '_' + this.type : ''
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
    return this.device.type
  }

  get searchType () : PlatformOrDeviceType {
    return PlatformOrDeviceType.DEVICE
  }

  get project (): string {
    // TODO
    return 'No project yet'
  }

  get state () : string {
    return this.device.state
  }
}
