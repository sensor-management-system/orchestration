/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020 - 2022
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

export interface IContact {
  id: string | null
  email: string
  givenName: string
  familyName: string
  website: string
  createdAt: DateTime | null
  updatedAt: DateTime | null
  createdByUserId: string | null
}

export class Contact implements IContact {
  private _id: string | null = null
  private _email: string = ''
  private _givenName: string = ''
  private _familyName: string = ''
  private _website: string = ''

  private _createdAt: DateTime | null = null
  private _updatedAt: DateTime | null = null
  private _createdByUserId: string | null = null

  get id (): string | null {
    return this._id
  }

  set id (newId: string | null) {
    this._id = newId
  }

  get email (): string {
    return this._email
  }

  set email (newEmail: string) {
    this._email = newEmail
  }

  get givenName (): string {
    return this._givenName
  }

  set givenName (newGivenName: string) {
    this._givenName = newGivenName
  }

  get familyName (): string {
    return this._familyName
  }

  set familyName (newFamilyName: string) {
    this._familyName = newFamilyName
  }

  get fullName (): string {
    return this.givenName + ' ' + this.familyName
  }

  get website (): string {
    return this._website
  }

  set website (newWebsite: string) {
    this._website = newWebsite
  }

  get createdAt (): DateTime | null {
    return this._createdAt
  }

  set createdAt (newCreatedAt: DateTime | null) {
    this._createdAt = newCreatedAt
  }

  get updatedAt (): DateTime | null {
    return this._updatedAt
  }

  set updatedAt (newUpdatedAt: DateTime | null) {
    this._updatedAt = newUpdatedAt
  }

  get createdByUserId (): string | null {
    return this._createdByUserId
  }

  set createdByUserId (newId: string | null) {
    this._createdByUserId = newId
  }

  toString (): string {
    if (this._givenName && this._familyName) {
      return this._givenName + ' ' + this._familyName
    }
    if (this._email) {
      return this._email
    }
    return 'Contact ' + this._id
  }

  static createWithIdEMailAndNames (id: string, email: string, givenName: string, familyName: string, website: string): Contact {
    const result = new Contact()
    result.id = id
    result.email = email
    result.givenName = givenName
    result.familyName = familyName
    result.website = website
    return result
  }

  static createEmpty (): Contact {
    return new Contact()
  }

  /**
   * creates an instance from another object
   *
   * @static
   * @param {IContact} someObject - the object from which the new instance is to be created
   * @return {Contact} the newly created instance
   */
  static createFromObject (someObject: IContact): Contact {
    const newObject = new Contact()
    newObject.id = someObject.id
    newObject.email = someObject.email
    newObject.givenName = someObject.givenName
    newObject.familyName = someObject.familyName
    newObject.website = someObject.website
    newObject.createdAt = someObject.createdAt
    newObject.updatedAt = someObject.updatedAt
    newObject.createdByUserId = someObject.createdByUserId
    return newObject
  }
}
