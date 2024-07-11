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

export interface IStaticLocationAction {
  id: string
  label: string
  beginDate: DateTime | null
  endDate: DateTime | null
  beginDescription: string
  endDescription: string
  beginContact: Contact | null
  endContact: Contact | null
  epsgCode: string
  x: number | null
  y: number | null
  z: number | null
  elevationDatumName: string
  elevationDatumUri: string
  configurationId: string | null

}

export class StaticLocationAction implements IStaticLocationAction {
  private _id: string = ''
  private _label: string = ''
  private _beginDate: DateTime | null = null
  private _endDate: DateTime | null = null
  private _beginDescription: string = ''
  private _endDescription: string = ''
  private _beginContact: Contact | null = null
  private _endContact: Contact | null = null
  private _x: number | null = null
  private _y: number | null = null
  private _z: number | null = null
  private _epsgCode: string = '4326'
  private _elevationDatumName: string = 'MSL'
  private _elevationDatumUri: string = ''
  private _configurationId: string | null = null

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

  get beginDate (): DateTime | null {
    return this._beginDate
  }

  set beginDate (newDate: DateTime | null) {
    this._beginDate = newDate
  }

  get endDate (): DateTime | null {
    return this._endDate
  }

  set endDate (newDate: DateTime | null) {
    this._endDate = newDate
  }

  get beginContact (): Contact | null {
    return this._beginContact
  }

  set beginContact (newContact: Contact | null) {
    this._beginContact = newContact
  }

  get endContact (): Contact | null {
    return this._endContact
  }

  set endContact (newContact: Contact | null) {
    this._endContact = newContact
  }

  get x (): number | null {
    return this._x
  }

  set x (newX: number | null) {
    this._x = newX
  }

  get y (): number | null {
    return this._y
  }

  set y (newY: number | null) {
    this._y = newY
  }

  get z (): number | null {
    return this._z
  }

  set z (newZ: number | null) {
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

  get configurationId (): string | null {
    return this._configurationId
  }

  set configurationId (newConfigurationId: string | null) {
    this._configurationId = newConfigurationId
  }

  static createFromObject (someObject: IStaticLocationAction): StaticLocationAction {
    const result = new StaticLocationAction()
    result.id = someObject.id
    result.label = someObject.label
    result.beginDate = someObject.beginDate
    result.endDate = someObject.endDate
    result.beginContact = someObject.beginContact
    result.endContact = someObject.endContact
    result.beginDescription = someObject.beginDescription
    result.endDescription = someObject.endDescription
    result.elevationDatumName = someObject.elevationDatumName
    result.elevationDatumUri = someObject.elevationDatumUri
    result.epsgCode = someObject.epsgCode
    result.x = someObject.x
    result.y = someObject.y
    result.z = someObject.z
    result.configurationId = someObject.configurationId
    return result
  }
}
