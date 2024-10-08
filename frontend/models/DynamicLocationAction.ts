/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2023
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */

import { DateTime } from 'luxon'

import { Contact } from '@/models/Contact'
import { DeviceProperty } from '@/models/DeviceProperty'

export interface IDynamicLocationAction {
  id: string
  label: string
  beginDate: DateTime | null
  endDate: DateTime | null
  beginDescription: string
  endDescription: string
  beginContact: Contact | null
  endContact: Contact | null
  epsgCode: string
  x: DeviceProperty | null
  y: DeviceProperty | null
  z: DeviceProperty | null
  elevationDatumName: string
  elevationDatumUri: string

}

export class DynamicLocationAction implements IDynamicLocationAction {
  private _id: string = ''
  private _label: string = ''
  private _beginDate: DateTime | null = null
  private _endDate: DateTime | null = null
  private _beginDescription: string = ''
  private _endDescription: string = ''
  private _beginContact: Contact | null = null
  private _endContact: Contact | null = null
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

  get label (): string {
    return this._label
  }

  set label (newLabel: string) {
    this._label = newLabel
  }

  get beginDate (): DateTime | null {
    return this._beginDate
  }

  set beginDate (newDate: DateTime | null) {
    this._beginDate = newDate
  }

  get endDate (): DateTime | null {
    return this._endDate
  }

  set endDate (value: DateTime | null) {
    this._endDate = value
  }

  get beginDescription (): string {
    return this._beginDescription
  }

  set beginDescription (value: string) {
    this._beginDescription = value
  }

  get endDescription (): string {
    return this._endDescription
  }

  set endDescription (value: string) {
    this._endDescription = value
  }

  get beginContact (): Contact | null {
    return this._beginContact
  }

  set beginContact (value: Contact | null) {
    this._beginContact = value
  }

  get endContact (): Contact | null {
    return this._endContact
  }

  set endContact (value: Contact | null) {
    this._endContact = value
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

  static createFromObject (someObject: IDynamicLocationAction): DynamicLocationAction {
    const result = new DynamicLocationAction()
    result.id = someObject.id
    result.label = someObject.label
    result.beginDate = someObject.beginDate
    result.beginContact = someObject.beginContact
    result.beginDescription = someObject.beginDescription
    result.endDate = someObject.endDate
    result.endContact = someObject.endContact
    result.endDescription = someObject.endDescription
    result.elevationDatumName = someObject.elevationDatumName
    result.elevationDatumUri = someObject.elevationDatumUri
    result.epsgCode = someObject.epsgCode
    result.x = someObject.x
    result.y = someObject.y
    result.z = someObject.z
    return result
  }
}
