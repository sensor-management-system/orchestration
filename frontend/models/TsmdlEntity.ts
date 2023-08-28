/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020-2023
 * - Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
 * - Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
 * - Maximilian Schaldach (UFZ, maximilian.schaldach@ufz.de)
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
export interface ITsmdlEntity{
  id: string
  name: string
  description: string
  properties: Object
}

export class TsmdlEntity implements ITsmdlEntity {
  private _description: string = ''
  private _id: string = ''
  private _name: string = ''
  private _properties: Object = {}

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

  static createFromObject (someObject: ITsmdlEntity): TsmdlEntity {
    const result = new TsmdlEntity()
    result.id = someObject.id ?? ''
    result.name = someObject.name ?? ''
    result.description = someObject.description ?? ''
    result.properties = someObject.properties ?? {}
    return result
  }
}
