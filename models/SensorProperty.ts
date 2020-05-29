import { IMeasuringRange, MeasuringRange } from './MeasuringRange'
import IPathSetter from './IPathSetter'

export interface ISensorProperty {
  compartment: string
  unit: string
  accuracy: number | null
  samplingMedia: string
  measuringRange: IMeasuringRange
  label: string
  variable: string
  failureValue: number | null
}

export class SensorProperty implements ISensorProperty, IPathSetter {
  private _compartment: string = ''
  private _unit: string = ''
  private _accuracy: number | null = null
  private _samplingMedia: string = ''
  private _measuringRange: MeasuringRange = new MeasuringRange()
  private _label: string = ''
  private _variable: string = ''
  private _failureValue: number | null = null

  /**
   * creates an instance from another object
   *
   * @static
   * @param {ISensorProperty} someObject - the object from which the new instance is to be created
   * @return {SensorProperty} the newly created instance
   */
  static createFromObject (someObject: ISensorProperty) : SensorProperty {
    const newObject = new SensorProperty()

    newObject.accuracy = someObject.accuracy
    newObject.compartment = someObject.compartment
    newObject.failureValue = someObject.failureValue
    newObject.label = someObject.label
    newObject.measuringRange = MeasuringRange.createFromObject(someObject.measuringRange)
    newObject.samplingMedia = someObject.samplingMedia
    newObject.unit = someObject.unit
    newObject.variable = someObject.variable

    return newObject
  }

  setPath (path: string, value: any): void {
    const properties = path.split('.')
    const property = properties.splice(0, 1)[0]
    let mrProperty

    switch (property) {
      case 'accuracy':
        this.accuracy = parseFloat(value)
        break
      case 'failureValue':
        this.failureValue = parseFloat(value)
        break
      case 'compartment':
        this.compartment = String(value)
        break
      case 'label':
        this.label = String(value)
        break
      case 'samplingMedia':
        this.samplingMedia = String(value)
        break
      case 'unit':
        this.unit = String(value)
        break
      case 'variable':
        this.variable = String(value)
        break
      case 'measuringRange':
        if (properties.length < 1) {
          throw new TypeError('missing second level in path')
        }
        mrProperty = properties.splice(0, 1)[0]
        this.measuringRange.setPath(mrProperty, value)
        break
      default:
        throw new TypeError('path ' + path + ' is not valid')
    }
  }

  get compartment (): string {
    return this._compartment
  }

  set compartment (compartment: string) {
    this._compartment = compartment
  }

  get unit (): string {
    return this._unit
  }

  set unit (unit: string) {
    this._unit = unit
  }

  get accuracy (): number | null {
    return this._accuracy
  }

  set accuracy (accuracy: number | null) {
    this._accuracy = accuracy
  }

  get samplingMedia (): string {
    return this._samplingMedia
  }

  set samplingMedia (samplingMedia: string) {
    this._samplingMedia = samplingMedia
  }

  get measuringRange (): MeasuringRange {
    return this._measuringRange
  }

  set measuringRange (measuringRange: MeasuringRange) {
    this._measuringRange = measuringRange
  }

  get label (): string {
    return this._label
  }

  set label (label: string) {
    this._label = label
  }

  get variable (): string {
    return this._variable
  }

  set variable (variable: string) {
    this._variable = variable
  }

  get failureValue (): number | null {
    return this._failureValue
  }

  set failureValue (failureValue: number | null) {
    this._failureValue = failureValue
  }
}
