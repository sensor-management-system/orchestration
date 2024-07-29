/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
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
  beginContact: IContact | null
  endContact: IContact | null
  beginDescription: string
  endDescription: string | null
  label: string
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
  private _beginContact: Contact | null = null
  private _endContact: Contact | null = null
  private _beginDescription: string = ''
  private _endDescription: string | null = null
  private _label: string = ''

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
    beginContact: Contact | null,
    endContact: Contact | null,
    beginDescription: string,
    endDescription: string | null,
    label: string
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
    this._label = label
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

  get label (): string {
    return this._label
  }

  set label (newValue: string) {
    this._label = newValue
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
      otherAction.beginContact ? Contact.createFromObject(otherAction.beginContact) : null,
      otherAction.endContact ? Contact.createFromObject(otherAction.endContact) : null,
      otherAction.beginDescription,
      otherAction.endDescription,
      otherAction.label
    )
  }
}
