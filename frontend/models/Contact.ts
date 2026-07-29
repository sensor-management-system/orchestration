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

export interface IContact {
  id: string | null
  email: string
  givenName: string
  familyName: string
  website: string
  organization: string
  orcid: string
  telephone: string
  faxNumber: string
  street: string
  streetNumber: string
  city: string
  zipCode: string
  administrativeArea: string
  country: string
  building: string
  room: string
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
  private _organization: string = ''
  private _orcid: string = ''
  private _telephone: string = ''
  private _faxNumber: string = ''
  private _street: string = ''
  private _streetNumber: string = ''
  private _city: string = ''
  private _zipCode: string = ''
  private _administrativeArea: string = ''
  private _country: string = ''
  private _building: string = ''
  private _room: string = ''

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

  get telephone (): string {
    return this._telephone
  }

  set telephone (newTelephone: string) {
    this._telephone = newTelephone
  }

  get faxNumber (): string {
    return this._faxNumber
  }

  set faxNumber (newFaxNumber: string) {
    this._faxNumber = newFaxNumber
  }

  get street (): string {
    return this._street
  }

  set street (newStreet: string) {
    this._street = newStreet
  }

  get streetNumber (): string {
    return this._streetNumber
  }

  set streetNumber (newStreetNumber: string) {
    this._streetNumber = newStreetNumber
  }

  get city (): string {
    return this._city
  }

  set city (newCity: string) {
    this._city = newCity
  }

  get zipCode (): string {
    return this._zipCode
  }

  set zipCode (newZipCode: string) {
    this._zipCode = newZipCode
  }

  get administrativeArea (): string {
    return this._administrativeArea
  }

  set administrativeArea (newAdministrativeArea: string) {
    this._administrativeArea = newAdministrativeArea
  }

  get country (): string {
    return this._country
  }

  set country (newCountry: string) {
    this._country = newCountry
  }

  get building (): string {
    return this._building
  }

  set building (newBuilding: string) {
    this._building = newBuilding
  }

  get room (): string {
    return this._room
  }

  set room (newRoom) {
    this._room = newRoom
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
    newObject.organization = someObject.organization
    newObject.orcid = someObject.orcid
    newObject.telephone = someObject.telephone
    newObject.faxNumber = someObject.faxNumber
    newObject.street = someObject.street
    newObject.streetNumber = someObject.streetNumber
    newObject.city = someObject.city
    newObject.zipCode = someObject.zipCode
    newObject.administrativeArea = someObject.administrativeArea
    newObject.country = someObject.country
    newObject.building = someObject.building
    newObject.room = someObject.room
    newObject.createdAt = someObject.createdAt
    newObject.updatedAt = someObject.updatedAt
    newObject.createdByUserId = someObject.createdByUserId
    return newObject
  }

  get composedCity (): string {
    // This should result in something like 14473 Potsdam, Brandenburg
    const cityPart = [this.zipCode, this.city].filter(x => x).join(' ')
    const result = [cityPart, this.administrativeArea].filter(x => x).join(', ')
    return result
  }
}
