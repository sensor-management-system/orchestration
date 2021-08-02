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
import { Platform } from '@/models/Platform'

export interface IPlatformUnmountAction {
  id: string
  platform: Platform
  date: DateTime
  contact: Contact
  description: string
}

export class PlatformUnmountAction implements IPlatformUnmountAction {
  private _id: string = ''
  private _platform: Platform
  private _date: DateTime
  private _contact: Contact
  private _description: string

  constructor (
    id: string,
    platform: Platform,
    date: DateTime,
    contact: Contact,
    description: string
  ) {
    this._id = id
    this._platform = platform
    this._date = date
    this._contact = contact
    this._description = description
  }

  get id (): string {
    return this._id
  }

  set id (newId: string) {
    this._id = newId
  }

  get platform (): Platform {
    return this._platform
  }

  get date (): DateTime {
    return this._date
  }

  get contact (): Contact {
    return this._contact
  }

  get description (): string {
    return this._description
  }

  get isMountAction (): boolean {
    return false
  }

  static createFromObject (otherAction: IPlatformUnmountAction): PlatformUnmountAction {
    return new PlatformUnmountAction(
      otherAction.id,
      Platform.createFromObject(otherAction.platform),
      otherAction.date,
      Contact.createFromObject(otherAction.contact),
      otherAction.description
    )
  }
}
