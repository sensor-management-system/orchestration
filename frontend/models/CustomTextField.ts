/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2023
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
export interface ICustomTextField {
  id: string | null,
  key: string,
  value: string
  description: string
}

export class CustomTextField implements ICustomTextField {
  private _id: string | null = null
  private _key: string = ''
  private _value: string = ''
  private _description: string = ''

  /**
   * creates an instance from another object
   *
   * @static
   * @param {ICustomTextField} someObject - the object from which the new instance is to be created
   * @return {CustomTextField} the newly created instance
   */
  static createFromObject (someObject: ICustomTextField): CustomTextField {
    const newObject = new CustomTextField()

    newObject.id = someObject.id

    newObject.key = someObject.key
    newObject.value = someObject.value
    newObject.description = someObject.description

    return newObject
  }

  get id (): string | null {
    return this._id
  }

  set id (newId: string | null) {
    this._id = newId
  }

  get key (): string {
    return this._key
  }

  set key (key: string) {
    this._key = key
  }

  get value (): string {
    return this._value
  }

  set value (value: string) {
    this._value = value
  }

  get description (): string {
    return this._description
  }

  set description (newDescription: string) {
    this._description = newDescription
  }
}
