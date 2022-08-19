/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020-2021
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
import { Device } from '@/models/Device'
import { Platform } from '@/models/Platform'

export interface IDeviceMountAction {
  id: string
  device: Device
  parentPlatform: Platform | null
  beginDate: DateTime
  endDate: DateTime | null
  offsetX: number
  offsetY: number
  offsetZ: number
  beginContact: Contact
  endContact: Contact | null
  beginDescription: string
  endDescription: string | null
}

export class DeviceMountAction implements IDeviceMountAction {
  private _id: string = ''
  private _device: Device
  private _parentPlatform: Platform | null
  private _beginDate: DateTime
  private _endDate: DateTime | null
  private _offsetX: number
  private _offsetY: number
  private _offsetZ: number
  private _beginContact: Contact
  private _endContact: Contact | null
  private _beginDescription: string
  private _endDescription: string | null

  constructor (
    id: string,
    device: Device,
    parentPlatform: Platform | null,
    beginDate: DateTime,
    endDate: DateTime | null,
    offsetX: number,
    offsetY: number,
    offsetZ: number,
    beginContact: Contact,
    endContact: Contact | null,
    beginDescription: string,
    endDescription: string | null
  ) {
    this._id = id
    this._device = device
    this._parentPlatform = parentPlatform
    this._beginDate = beginDate
    this._endDate = endDate
    this._offsetX = offsetX
    this._offsetY = offsetY
    this._offsetZ = offsetZ
    this._beginContact = beginContact
    this._endContact = endContact
    this._beginDescription = beginDescription
    this._endDescription = endDescription
  }

  get id (): string {
    return this._id
  }

  set id (newId: string) {
    this._id = newId
  }

  get device (): Device {
    return this._device
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

  get isMountAction () {
    return true
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

  static createFromObject (otherAction: IDeviceMountAction): DeviceMountAction {
    return new DeviceMountAction(
      otherAction.id,
      Device.createFromObject(otherAction.device),
      otherAction.parentPlatform === null ? null : Platform.createFromObject(otherAction.parentPlatform),
      otherAction.beginDate,
      otherAction.endDate === null ? null : otherAction.endDate,
      otherAction.offsetX,
      otherAction.offsetY,
      otherAction.offsetZ,
      Contact.createFromObject(otherAction.beginContact),
      otherAction.endContact === null ? null : Contact.createFromObject(otherAction.endContact),
      otherAction.beginDescription,
      otherAction.endDescription === null ? null : otherAction.endDescription
    )
  }
}
