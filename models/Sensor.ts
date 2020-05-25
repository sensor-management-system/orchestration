import Person from './Person'
import { SensorProperty } from './SensorProperty'
import CustomTextField from './CustomTextField'

export default class Sensor {
  private _id: number | null = null
  private _persistentId: string = ''
  private _label: string = ''
  private _state: string = ''
  private _type: string = ''
  private _manufacturer: string = ''
  private _model: string = ''
  private _description: string = ''
  private _urlWebsite: string = ''
  private _serialNumber: string = ''
  private _inventoryNumber: string = ''
  private _dualUse: boolean = false

  private _responsiblePersons: Person[] = []
  private _properties: SensorProperty[] = []
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

  get manufacturer (): string {
    return this._manufacturer
  }

  set manufacturer (manufacturer: string) {
    this._manufacturer = manufacturer
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

  get responsiblePersons (): Person[] {
    return this._responsiblePersons
  }

  set responsiblePersons (responsiblePersons: Person[]) {
    this._responsiblePersons = responsiblePersons
  }

  get properties (): SensorProperty[] {
    return this._properties
  }

  set properties (properties: SensorProperty[]) {
    this._properties = properties
  }

  get customFields (): CustomTextField[] {
    return this._customFields
  }

  set customFields (customFields: CustomTextField[]) {
    this._customFields = customFields
  }
}
