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

export interface IContactBasicData {
  id: string | null
  email: string
  givenName: string
  familyName: string
  website: string
  organization: string
  orcid: string
  createdAt: DateTime | null
  updatedAt: DateTime | null
  createdByUserId: string | null
}

export class ContactBasicData implements IContactBasicData {
  private _id: string | null = null
  private _email: string = ''
  private _givenName: string = ''
  private _familyName: string = ''
  private _website: string = ''
  private _organization: string = ''
  private _orcid: string = ''

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

  get website (): string {
    return this._website
  }

  set website (newWebsite: string) {
    this._website = newWebsite
  }

  get organization (): string {
    return this._organization
  }

  set organization (newOrganization: string) {
    this._organization = newOrganization
  }

  get orcid (): string {
    return this._orcid
  }

  set orcid (newOrcid: string) {
    this._orcid = newOrcid
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

  static createWithIdEMailAndNames (id: string, email: string, givenName: string, familyName: string, website: string): ContactBasicData {
    const result = new ContactBasicData()
    result.id = id
    result.email = email
    result.givenName = givenName
    result.familyName = familyName
    result.website = website
    return result
  }

  static createEmpty (): ContactBasicData {
    return new ContactBasicData()
  }

  /**
   * creates an instance from another object
   *
   * @static
   * @param {IContact} someObject - the object from which the new instance is to be created
   * @return {Contact} the newly created instance
   */
  static createFromObject (someObject: IContactBasicData): ContactBasicData {
    const newObject = new ContactBasicData()
    newObject.id = someObject.id
    newObject.email = someObject.email
    newObject.givenName = someObject.givenName
    newObject.familyName = someObject.familyName
    newObject.website = someObject.website
    newObject.organization = someObject.organization
    newObject.orcid = someObject.orcid
    newObject.createdAt = someObject.createdAt
    newObject.updatedAt = someObject.updatedAt
    newObject.createdByUserId = someObject.createdByUserId
    return newObject
  }
}
