/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
export interface IMeasuredQuantityUnit {
  id: string
  name: string
  uri: string
  definition: string
  defaultLimitMin: string | null
  defaultLimitMax: string | null
  unitId: string
  measuredQuantityId: string
}

export class MeasuredQuantityUnit implements IMeasuredQuantityUnit {
  private _id: string = ''
  private _name: string = ''
  private _uri: string = ''
  private _definition: string = ''
  private _defaultLimitMin: string | null = null
  private _defaultLimitMax: string | null = null
  private _unitId: string = ''
  private _measuredQuantityId: string = ''

  get id (): string {
    return this._id
  }

  set id (newId: string) {
    this._id = newId
  }

  get name (): string {
    return this._name
  }

  set name (newName: string) {
    this._name = newName
  }

  get uri (): string {
    return this._uri
  }

  set uri (newUri: string) {
    this._uri = newUri
  }

  get definition (): string {
    return this._definition
  }

  set definition (newDefinition: string) {
    this._definition = newDefinition
  }

  get defaultLimitMin (): string | null {
    return this._defaultLimitMin
  }

  set defaultLimitMin (newDefaultLimitMin: string | null) {
    this._defaultLimitMin = newDefaultLimitMin
  }

  get defaultLimitMax (): string | null {
    return this._defaultLimitMax
  }

  set defaultLimitMax (newDefaultLimitMax: string | null) {
    this._defaultLimitMax = newDefaultLimitMax
  }

  get unitId (): string {
    return this._unitId
  }

  set unitId (newUnitId: string) {
    this._unitId = newUnitId
  }

  get measuredQuantityId (): string {
    return this._measuredQuantityId
  }

  set measuredQuantityId (newUnitId: string) {
    this._measuredQuantityId = newUnitId
  }

  static createWithData (id: string, name: string, uri: string, definition: string, defaultLimitMin: string, defaultLimitMax: string, unitId: string, measuredQuantityId: string): MeasuredQuantityUnit {
    const result = new MeasuredQuantityUnit()
    result.id = id
    result.name = name
    result.uri = uri
    result.definition = definition
    result.defaultLimitMin = defaultLimitMin
    result.defaultLimitMax = defaultLimitMax
    result.unitId = unitId
    result.measuredQuantityId = measuredQuantityId
    return result
  }

  static createFromObject (someObject: IMeasuredQuantityUnit): MeasuredQuantityUnit {
    const newObject = new MeasuredQuantityUnit()

    newObject.id = someObject.id
    newObject.name = someObject.name
    newObject.uri = someObject.uri
    newObject.definition = someObject.definition
    newObject.defaultLimitMin = someObject.defaultLimitMin
    newObject.defaultLimitMax = someObject.defaultLimitMax
    newObject.unitId = someObject.unitId
    newObject.measuredQuantityId = someObject.measuredQuantityId

    return newObject
  }
}
