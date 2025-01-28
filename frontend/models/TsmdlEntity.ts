/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Maximilian Schaldach <maximilian.schaldach@ufz.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
export interface ITsmdlEntity{
  id: string
  name: string
  description: string
  properties: Object
  staLink: string
}

export class TsmdlEntity implements ITsmdlEntity {
  private _description: string = ''
  private _id: string = ''
  private _name: string = ''
  private _properties: Object = {}
  private _staLink: string = ''

  constructor (
    id: string = ''
  ) {
    this._id = id
  }

  get description (): string {
    return this._description
  }

  set description (value: string) {
    this._description = value
  }

  get id (): string {
    return this._id
  }

  set id (value: string) {
    this._id = value
  }

  get name (): string {
    return this._name
  }

  set name (value: string) {
    this._name = value
  }

  get properties (): Object {
    return this._properties
  }

  set properties (value: Object) {
    this._properties = value
  }

  get staLink (): string {
    return this._staLink
  }

  set staLink (value: string) {
    this._staLink = value
  }

  static createFromObject (someObject: ITsmdlEntity): TsmdlEntity {
    const result = new TsmdlEntity()
    result.id = someObject.id ?? ''
    result.name = someObject.name ?? ''
    result.description = someObject.description ?? ''
    result.properties = someObject.properties ?? {}
    result.staLink = someObject.staLink ?? ''
    return result
  }
}
