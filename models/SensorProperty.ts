export interface IMeasuringRange {
  min: number | null
  max: number | null
}

export class MeasuringRange implements IMeasuringRange {
  private _min: number | null = null
  private _max: number | null = null

  constructor (min: number | null = null, max: number | null = null) {
    this.min = min
    this.max = max
  }

  static createFromObject (someObject: IMeasuringRange) : MeasuringRange {
    return new MeasuringRange(someObject.min, someObject.max)
  }

  get min (): number | null {
    return this._min
  }

  set min (min: number | null) {
    this._min = min
  }

  get max (): number | null {
    return this._max
  }

  set max (max: number | null) {
    this._max = max
  }
}

export default class SensorProperty {
  private _compartment: string = ''
  private _unit: string = ''
  private _accuracy: number | null = null
  private _samplingMedia: string = ''
  private _measuringRange: MeasuringRange = new MeasuringRange()
  private _label: string = ''
  private _variable: string = ''
  private _failureValue: number | null = null

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
