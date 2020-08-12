import { IMeasuringRange, MeasuringRange } from './MeasuringRange'
import IPathSetter from './IPathSetter'

export interface IDeviceProperty {
  id: number | null
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

export class DeviceProperty implements IDeviceProperty, IPathSetter {
  private _id: number | null = null
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

  setPath (path: string, value: any): void {
    const properties = path.split('.')
    const property = properties.splice(0, 1)[0]
    let mrProperty

    switch (property) {
      case 'id':
        this.id = value === null || isNaN(value) ? null : parseFloat(value)
        break
      case 'label':
        this.label = String(value)
        break
      case 'compartmentUri':
        this.compartmentUri = String(value)
        break
      case 'compartmentName':
        this.compartmentName = String(value)
        break
      case 'unitUri':
        this.unitUri = String(value)
        break
      case 'unitName':
        this.unitName = String(value)
        break
      case 'samplingMediaUri':
        this.samplingMediaUri = String(value)
        break
      case 'samplingMediaName':
        this.samplingMediaName = String(value)
        break
      case 'propertyUri':
        this.propertyUri = String(value)
        break
      case 'propertyName':
        this.propertyName = String(value)
        break
      case 'measuringRange':
        if (properties.length < 1) {
          throw new TypeError('missing second level in path')
        }
        mrProperty = properties.splice(0, 1)[0]
        this.measuringRange.setPath(mrProperty, value)
        break
      case 'accuracy':
        this.accuracy = parseFloat(value)
        break
      case 'failureValue':
        this.failureValue = parseFloat(value)
        break
      default:
        throw new TypeError('path ' + path + ' is not valid')
    }
  }

  get id (): number | null {
    return this._id
  }

  set id (id: number | null) {
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
}
