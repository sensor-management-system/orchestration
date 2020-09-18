import { IMeasuringRange, MeasuringRange } from '@/models/MeasuringRange'

export interface IDeviceProperty {
  id: string | null
  label: string
  compartmentUri: string
  compartmentName: string
  unitUri: string
  unitName: string
  samplingMediaUri: string
  samplingMediaName: string
  propertyUri: string
  propertyName: string
  measuringRange: IMeasuringRange
  accuracy: number | null
  failureValue: number | null
}

export class DeviceProperty implements IDeviceProperty {
  private _id: string | null = null
  private _label: string = ''
  private _compartmentUri: string = ''
  private _compartmentName: string = ''
  private _unitUri: string = ''
  private _unitName: string = ''
  private _samplingMediaUri: string = ''
  private _samplingMediaName: string = ''
  private _propertyUri: string = ''
  private _propertyName: string = ''
  private _measuringRange: MeasuringRange = new MeasuringRange()
  private _accuracy: number | null = null
  private _failureValue: number | null = null

  /**
   * creates an instance from another object
   *
   * @static
   * @param {IDeviceProperty} someObject - the object from which the new instance is to be created
   * @return {DeviceProperty} the newly created instance
   */
  static createFromObject (someObject: IDeviceProperty) : DeviceProperty {
    const newObject = new DeviceProperty()

    newObject.id = someObject.id
    newObject.label = someObject.label
    newObject.compartmentUri = someObject.compartmentUri
    newObject.compartmentName = someObject.compartmentName
    newObject.unitUri = someObject.unitUri
    newObject.unitName = someObject.unitName
    newObject.samplingMediaUri = someObject.samplingMediaUri
    newObject.samplingMediaName = someObject.samplingMediaName
    newObject.propertyUri = someObject.propertyUri
    newObject.propertyName = someObject.propertyName
    newObject.measuringRange = MeasuringRange.createFromObject(someObject.measuringRange)
    newObject.accuracy = someObject.accuracy
    newObject.failureValue = someObject.failureValue

    return newObject
  }

  get id (): string | null {
    return this._id
  }

  set id (id: string | null) {
    this._id = id
  }

  get label (): string {
    return this._label
  }

  set label (label: string) {
    this._label = label
  }

  get compartmentUri (): string {
    return this._compartmentUri
  }

  set compartmentUri (compartmentUri: string) {
    this._compartmentUri = compartmentUri
  }

  get compartmentName (): string {
    return this._compartmentName
  }

  set compartmentName (compartmentName: string) {
    this._compartmentName = compartmentName
  }

  get unitUri (): string {
    return this._unitUri
  }

  set unitUri (unitUri: string) {
    this._unitUri = unitUri
  }

  get unitName (): string {
    return this._unitName
  }

  set unitName (unitName: string) {
    this._unitName = unitName
  }

  get samplingMediaUri (): string {
    return this._samplingMediaUri
  }

  set samplingMediaUri (samplingMediaUri: string) {
    this._samplingMediaUri = samplingMediaUri
  }

  get samplingMediaName (): string {
    return this._samplingMediaName
  }

  set samplingMediaName (samplingMediaName: string) {
    this._samplingMediaName = samplingMediaName
  }

  get propertyUri (): string {
    return this._propertyUri
  }

  set propertyUri (propertyUri: string) {
    this._propertyUri = propertyUri
  }

  get propertyName (): string {
    return this._propertyName
  }

  set propertyName (propertyName: string) {
    this._propertyName = propertyName
  }

  get measuringRange (): MeasuringRange {
    return this._measuringRange
  }

  set measuringRange (measuringRange: MeasuringRange) {
    this._measuringRange = measuringRange
  }

  get accuracy (): number | null {
    return this._accuracy
  }

  set accuracy (accuracy: number | null) {
    this._accuracy = accuracy
  }

  get failureValue (): number | null {
    return this._failureValue
  }

  set failureValue (failureValue: number | null) {
    this._failureValue = failureValue
  }

  toString (): string {
    return this.propertyName
  }
}
