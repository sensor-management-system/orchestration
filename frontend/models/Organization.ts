/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2026
 * - Nils Brinckmann <nils.brinckmann@gfz.de>
 * - GFZ Helmholtz for Geosciences (GFZ, https://www.gfz.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */

export interface IOrganization {
  id: string
  name: string
  ror: string
  abbreviation: string
}

export class Organization implements IOrganization {
  private _id: string = ''
  private _name: string = ''
  private _ror: string = ''
  private _abbreviation: string = ''

  get id (): string {
    return this._id
  }

  set id (newId: string) {
    this._id = newId
  }

  get name (): string {
    return this._name
  }

  set name (newName: string) {
    this._name = newName
  }

  get ror (): string {
    return this._ror
  }

  set ror (newRor: string) {
    this._ror = newRor
  }

  get abbreviation (): string {
    return this._abbreviation
  }

  set abbreviation (newAbbreviation: string) {
    this._abbreviation = newAbbreviation
  }

  static createFromObject (someObject: IOrganization): Organization {
    const result = new Organization()
    result.id = someObject.id
    result.name = someObject.name
    result.ror = someObject.ror
    result.abbreviation = someObject.abbreviation
    return result
  }
}
