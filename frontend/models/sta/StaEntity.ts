/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2024
 * - Maximilian Schaldach <maximilian.schaldach@ufz.de>
 * - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
export interface StaApiEntity {
  '@iot.id': string
  '@iot.selfLink': string
  'name': string
  'properties': {
    'jsonld.id': string
  }
}

export interface IStaEntity {
  selfLink: string
  id: string | null;
  name: string;
  properties: object
}

export class StaEntity implements IStaEntity {
  private _id: string | null = null
  private _name: string = ''
  private _properties: object = {}
  private _selfLink: string = ''

  get selfLink (): string {
    return this._selfLink
  }

  set selfLink (value: string) {
    this._selfLink = value
  }

  get id (): string | null {
    return this._id
  }

  set id (value: string | null) {
    this._id = value
  }

  get name (): string {
    return this._name
  }

  set name (value: string) {
    this._name = value
  }

  get properties (): object {
    return this._properties
  }

  set properties (value: object) {
    this._properties = value
  }

  static createFromObject (someObject: IStaEntity): StaEntity {
    const result = new StaEntity()
    result.id = someObject.id ?? ''
    result.name = someObject.name ?? ''
    result.selfLink = someObject.selfLink ?? ''
    return result
  }
}
