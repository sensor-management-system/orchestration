/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020-2024
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

/** Basically those classes and interfaces here
 *  define the "basic" view of the device mount action data.
 *  This means this are the data explicitly for the entity
 *  without the need to make another joins or to include more
 *  data.
 */
export interface IDeviceMountActionBasicData {
  id: string
  beginDate: DateTime
  endDate: DateTime | null
  offsetX: number
  offsetY: number
  offsetZ: number
  beginDescription: string
  endDescription: string
  epsgCode: string
  x: number | null
  y: number | null
  z: number | null
  elevationDatumName: string
  elevationDatumUri: string
}

export class DeviceMountActionBasicData implements IDeviceMountActionBasicData {
  private _id: string = ''
  private _beginDate: DateTime
  private _endDate: DateTime | null
  private _offsetX: number
  private _offsetY: number
  private _offsetZ: number
  private _beginDescription: string
  private _endDescription: string
  private _epsgCode: string = ''
  private _x: number | null = null
  private _y: number | null = null
  private _z: number | null = null
  private _elevationDatumName: string = ''
  private _elevationDatumUri: string = ''

  constructor (
    id: string,
    beginDate: DateTime,
    endDate: DateTime | null,
    offsetX: number,
    offsetY: number,
    offsetZ: number,
    beginDescription: string,
    endDescription: string,
    epsgCode: string,
    x: number | null,
    y: number | null,
    z: number | null,
    elevationDatumName: string,
    elevationDatumUri: string
  ) {
    this._id = id
    this._beginDate = beginDate
    this._endDate = endDate
    this._offsetX = offsetX
    this._offsetY = offsetY
    this._offsetZ = offsetZ
    this._beginDescription = beginDescription
    this._endDescription = endDescription
    this._epsgCode = epsgCode
    this._x = x
    this._y = y
    this._z = z
    this._elevationDatumName = elevationDatumName
    this._elevationDatumUri = elevationDatumUri
  }

  get id (): string {
    return this._id
  }

  set id (newId: string) {
    this._id = newId
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

  get beginDescription (): string {
    return this._beginDescription
  }

  set beginDescription (newDescription: string) {
    this._beginDescription = newDescription
  }

  get endDescription (): string {
    return this._endDescription
  }

  set endDescription (newDescription: string) {
    this._endDescription = newDescription
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

  static createFromObject (otherAction: IDeviceMountActionBasicData): DeviceMountActionBasicData {
    return new DeviceMountActionBasicData(
      otherAction.id,
      otherAction.beginDate,
      otherAction.endDate,
      otherAction.offsetX,
      otherAction.offsetY,
      otherAction.offsetZ,
      otherAction.beginDescription,
      otherAction.endDescription,
      otherAction.epsgCode,
      otherAction.x,
      otherAction.y,
      otherAction.z,
      otherAction.elevationDatumName,
      otherAction.elevationDatumUri
    )
  }
}
