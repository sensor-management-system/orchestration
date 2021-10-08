/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020, 2021
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

import { DateTime } from 'luxon'

import { Contact } from '@/models/Contact'
import { DeviceProperty } from '@/models/DeviceProperty'

export interface IDynamicLocationBeginAction {
  id: string
  beginDate: DateTime | null
  description: string
  contact: Contact | null
  epsgCode: string
  x: DeviceProperty | null
  y: DeviceProperty | null
  z: DeviceProperty | null
  elevationDatumName: string
  elevationDatumUri: string

}

export class DynamicLocationBeginAction implements IDynamicLocationBeginAction {
  private _id: string = ''
  private _beginDate: DateTime | null = null
  private _description: string = ''
  private _contact: Contact | null = null
  private _x: DeviceProperty | null = null
  private _y: DeviceProperty | null = null
  private _z: DeviceProperty | null = null
  private _epsgCode: string = '4326'
  private _elevationDatumName: string = 'MSL'
  private _elevationDatumUri: string = ''

  get id (): string {
    return this._id
  }

  set id (newId: string) {
    this._id = newId
  }

  get beginDate (): DateTime | null {
    return this._beginDate
  }

  set beginDate (newDate: DateTime | null) {
    this._beginDate = newDate
  }

  get description (): string {
    return this._description
  }

  set description (newDescription: string) {
    this._description = newDescription
  }

  get contact (): Contact | null {
    return this._contact
  }

  set contact (newContact: Contact | null) {
    this._contact = newContact
  }

  get x (): DeviceProperty | null {
    return this._x
  }

  set x (newX: DeviceProperty | null) {
    this._x = newX
  }

  get y (): DeviceProperty | null {
    return this._y
  }

  set y (newY: DeviceProperty | null) {
    this._y = newY
  }

  get z (): DeviceProperty | null {
    return this._z
  }

  set z (newZ: DeviceProperty | null) {
    this._z = newZ
  }

  get epsgCode (): string {
    return this._epsgCode
  }

  set epsgCode (newEpsgCode: string) {
    this._epsgCode = newEpsgCode
  }

  get elevationDatumName (): string {
    return this._elevationDatumName
  }

  set elevationDatumName (newName: string) {
    this._elevationDatumName = newName
  }

  get elevationDatumUri (): string {
    return this._elevationDatumUri
  }

  set elevationDatumUri (newUri: string) {
    this._elevationDatumUri = newUri
  }

  static createFromObject (someObject: IDynamicLocationBeginAction): DynamicLocationBeginAction {
    const result = new DynamicLocationBeginAction()
    result.id = someObject.id
    result.beginDate = someObject.beginDate
    result.contact = someObject.contact
    result.description = someObject.description
    result.elevationDatumName = someObject.elevationDatumName
    result.elevationDatumUri = someObject.elevationDatumUri
    result.epsgCode = someObject.epsgCode
    result.x = someObject.x
    result.y = someObject.y
    result.z = someObject.z
    return result
  }
}
