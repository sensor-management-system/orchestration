import { IMeasuringRange, MeasuringRange } from './MeasuringRange'

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

export class SensorProperty implements ISensorProperty {
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
