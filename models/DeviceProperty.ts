/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020
 * - Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
 * - Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for
 *   Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * Parts of this program were developed within the context of the
 * following publicly funded projects or measures:
 * - Helmholtz Earth and Environment DataHub
 *   (https://www.helmholtz.de/en/research/earth_and_environment/initiatives/#h51095)
 *
 * Licensed under the HEESIL, Version 1.0 or - as soon they will be
 * approved by the "Community" - subsequent versions of the HEESIL
 * (the "Licence").
 *
 * You may not use this work except in compliance with the Licence.
 *
 * You may obtain a copy of the Licence at:
 * https://gitext.gfz-potsdam.de/software/heesil
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the Licence is distributed on an "AS IS" basis,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
 * implied. See the Licence for the specific language governing
 * permissions and limitations under the Licence.
 */
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
  resolution: number | null
  resolutionUnitUri: string
  resolutionUnitName: string
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
  private _resolution: number | null = null
  private _resolutionUnitUri: string = ''
  private _resolutionUnitName: string = ''

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
    newObject.resolution = someObject.resolution
    newObject.resolutionUnitUri = someObject.resolutionUnitUri
    newObject.resolutionUnitName = someObject.resolutionUnitName

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

  get resolution (): number | null {
    return this._resolution
  }

  set resolution (resolution: number | null) {
    this._resolution = resolution
  }

  get resolutionUnitUri (): string {
    return this._resolutionUnitUri
  }

  set resolutionUnitUri (resolutionUnitUri: string) {
    this._resolutionUnitUri = resolutionUnitUri
  }

  get resolutionUnitName (): string {
    return this._resolutionUnitName
  }

  set resolutionUnitName (resolutionUnitName: string) {
    this._resolutionUnitName = resolutionUnitName
  }

  toString (): string {
    return this.label || this.propertyName
  }
}
