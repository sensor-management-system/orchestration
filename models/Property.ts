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
export interface IProperty {
  id: string
  name: string
  uri: string
  samplingMediaId: string
}

export class Property implements IProperty {
  private _id: string = ''
  private _name: string = ''
  private _uri: string = ''
  private _samplingMediaId: string = ''

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

  get samplingMediaId (): string {
    return this._samplingMediaId
  }

  set samplingMediaId (newSamplingMediaId: string) {
    this._samplingMediaId = newSamplingMediaId
  }

  toString (): string {
    return this._name
  }

  static createWithData (id: string, name: string, uri: string, samplingMediaId: string): Property {
    const result = new Property()
    result.id = id
    result.name = name
    result.uri = uri
    result.samplingMediaId = samplingMediaId
    return result
  }

  static createFromObject (someObject: IProperty): Property {
    const newObject = new Property()

    newObject.id = someObject.id
    newObject.name = someObject.name
    newObject.uri = someObject.uri
    newObject.samplingMediaId = someObject.samplingMediaId

    return newObject
  }
}
