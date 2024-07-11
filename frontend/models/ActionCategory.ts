/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2022 - 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */

export interface IActionCategory {
  id: string
  name: string
}

export class ActionCategory implements IActionCategory {
  private _id: string = ''
  private _name: string = ''

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

  toString (): string {
    return this._name
  }

  static createFromObject (someObject: IActionCategory): ActionCategory {
    const newObject = new ActionCategory()

    newObject.id = someObject.id
    newObject.name = someObject.name

    return newObject
  }
}
