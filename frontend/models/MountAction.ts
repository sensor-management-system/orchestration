/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020-2022
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

import { IContact, Contact } from '@/models/Contact'
import { IPlatform, Platform } from '@/models/Platform'

export interface IMountAction {
  TYPE: string
  id: string
  parentPlatform: IPlatform | null
  beginDate: DateTime
  endDate: DateTime | null
  offsetX: number
  offsetY: number
  offsetZ: number
  epsgCode: string
  x: number | null
  y: number | null
  z: number | null
  elevationDatumName: string
  elevationDatumUri: string
  beginContact: IContact
  endContact: IContact | null
  beginDescription: string
  endDescription: string | null
}

/**
 * Class to define the common properties of a MountAction.
 *
 * Although not abstract, this class does not define what is mounted.  Should be
 * only used to help to build corresponding Device- and PlatformMountActions
 * and as a helper class.
 *
 * @implements IMountAction
 */
export class MountAction implements IMountAction {
  private _id: string = ''
  private _parentPlatform: Platform | null = null
  private _beginDate: DateTime
  private _endDate: DateTime | null = null
  private _offsetX: number = 0
  private _offsetY: number = 0
  private _offsetZ: number = 0
  private _epsgCode: string = ''
  private _x: number | null = null
  private _y: number | null = null
  private _z: number | null = null
  private _elevationDatumName: string = ''
  private _elevationDatumUri: string = ''
  private _beginContact: Contact
  private _endContact: Contact | null = null
  private _beginDescription: string = ''
  private _endDescription: string | null = null

  constructor (
    id: string,
    parentPlatform: Platform | null,
    beginDate: DateTime,
    endDate: DateTime | null,
    offsetX: number,
    offsetY: number,
    offsetZ: number,
    epsgCode: string,
    x: number | null,
    y: number | null,
    z: number | null,
    elevationDatumName: string,
    elevationDatumUri: string,
    beginContact: Contact,
    endContact: Contact | null,
    beginDescription: string,
    endDescription: string | null
  ) {
    this._id = id
    this._parentPlatform = parentPlatform
    this._beginDate = beginDate
    this._endDate = endDate
    this._offsetX = offsetX
    this._offsetY = offsetY
    this._offsetZ = offsetZ
    this._epsgCode = epsgCode
    this._x = x
    this._y = y
    this._z = z
    this._elevationDatumName = elevationDatumName
    this._elevationDatumUri = elevationDatumUri
    this._beginContact = beginContact
    this._endContact = endContact
    this._beginDescription = beginDescription
    this._endDescription = endDescription
  }

  get TYPE (): string {
    return 'MOUNT_ACTION'
  }

  get id (): string {
    return this._id
  }

  set id (newId: string) {
    this._id = newId
  }

  get parentPlatform (): Platform | null {
    return this._parentPlatform
  }

  get beginDate (): DateTime {
    return this._beginDate
  }

  set beginDate (newDate: DateTime) {
    this._beginDate = newDate
  }

  get endDate (): DateTime | null {
    return this._endDate
  }

  set endDate (newDate: DateTime | null) {
    this._endDate = newDate
  }

  get offsetX (): number {
    return this._offsetX
  }

  set offsetX (newOffsetX: number) {
    this._offsetX = newOffsetX
  }

  get offsetY (): number {
    return this._offsetY
  }

  set offsetY (newOffsetY: number) {
    this._offsetY = newOffsetY
  }

  get offsetZ (): number {
    return this._offsetZ
  }

  set offsetZ (newOffsetZ: number) {
    this._offsetZ = newOffsetZ
  }

  get epsgCode (): string {
    return this._epsgCode
  }

  set epsgCode (newEpsgCode: string) {
    this._epsgCode = newEpsgCode
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

  get elevationDatumName (): string {
    return this._elevationDatumName
  }

  set elevationDatumName (newElevationDatumName: string) {
    this._elevationDatumName = newElevationDatumName
  }

  get elevationDatumUri (): string {
    return this._elevationDatumUri
  }

  set elevationDatumUri (newElevationDatumUri: string) {
    this._elevationDatumUri = newElevationDatumUri
  }

  get beginContact (): Contact {
    return this._beginContact
  }

  set beginContact (newContact: Contact) {
    this._beginContact = newContact
  }

  get endContact (): Contact | null {
    return this._endContact
  }

  set endContact (newContact: Contact | null) {
    this._endContact = newContact
  }

  get beginDescription (): string {
    return this._beginDescription
  }

  set beginDescription (newDescription: string) {
    this._beginDescription = newDescription
  }

  set endDescription (newDescription: string | null) {
    this._endDescription = newDescription
  }

  get endDescription (): string | null {
    return this._endDescription
  }

  equals (action: IMountAction): boolean {
    return this.id === action.id && this.TYPE === action.TYPE
  }

  static createFromObject (otherAction: Omit<IMountAction, 'TYPE'>): MountAction {
    return new MountAction(
      otherAction.id,
      otherAction.parentPlatform ? Platform.createFromObject(otherAction.parentPlatform) : null,
      otherAction.beginDate,
      otherAction.endDate,
      otherAction.offsetX,
      otherAction.offsetY,
      otherAction.offsetZ,
      otherAction.epsgCode,
      otherAction.x,
      otherAction.y,
      otherAction.z,
      otherAction.elevationDatumName,
      otherAction.elevationDatumUri,
      Contact.createFromObject(otherAction.beginContact),
      otherAction.endContact ? Contact.createFromObject(otherAction.endContact) : null,
      otherAction.beginDescription,
      otherAction.endDescription
    )
  }
}
