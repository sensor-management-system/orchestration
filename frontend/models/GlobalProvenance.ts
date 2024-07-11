/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2022
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
export interface IGlobalProvenance {
  id: string
  name: string
  description: string
}

export class GlobalProvenance implements IGlobalProvenance {
  private _id: string = ''
  private _name: string = ''
  private _description: string = ''

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

  get description (): string {
    return this._description
  }

  set description (newDescription: string) {
    this._description = newDescription
  }

  toString (): string {
    return this._name
  }

  static createFromObject (someObject: IGlobalProvenance): GlobalProvenance {
    const newObject = new GlobalProvenance()

    newObject.id = someObject.id
    newObject.name = someObject.name
    newObject.description = someObject.description

    return newObject
  }
}
