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
import { IContact, Contact } from '@/models/Contact'

export interface IParameter {
  id: string | null
  label: string
  description: string

  unitUri: string
  unitName: string

  createdAt: DateTime | null
  updatedAt: DateTime | null

  createdBy: IContact | null
  updatedBy: IContact | null
}

export type IParameterLike = Partial<IParameter>

export class Parameter implements IParameter {
  private _id: string | null = null
  private _label: string = ''
  private _description: string = ''

  private _unitUri: string = ''
  private _unitName: string = ''

  private _createdAt: DateTime | null = null
  private _updatedAt: DateTime | null = null

  private _createdBy: IContact | null = null
  private _updatedBy: IContact | null = null

  get id (): string | null {
    return this._id
  }

  set id (id: string | null) {
    this._id = id
  }

  get label (): string {
    return this._label
  }

  set label (label: string) {
    this._label = label
  }

  get description (): string {
    return this._description
  }

  set description (description: string) {
    this._description = description
  }

  get unitUri (): string {
    return this._unitUri
  }

  set unitUri (unitUri: string) {
    this._unitUri = unitUri
  }

  get unitName (): string {
    return this._unitName
  }

  set unitName (unitName: string) {
    this._unitName = unitName
  }

  get createdAt (): DateTime | null {
    return this._createdAt
  }

  set createdAt (createdAt: DateTime | null) {
    this._createdAt = createdAt
  }

  get updatedAt (): DateTime | null {
    return this._updatedAt
  }

  set updatedAt (updatedAt: DateTime | null) {
    this._updatedAt = updatedAt
  }

  get createdBy (): IContact | null {
    return this._createdBy
  }

  set createdBy (user: IContact | null) {
    this._createdBy = user
  }

  get updatedBy (): IContact | null {
    return this._updatedBy
  }

  set updatedBy (user: IContact | null) {
    this._updatedBy = user
  }

  /**
   * creates a Parameter instance from a IParameterLike object
   *
   * @static
   * @param {IParameter} someObject - an ParameterLike object
   * @returns {Parameter} a Parameter instance
   */
  static createFromObject (someObject: IParameterLike): Parameter {
    const newObject = new Parameter()

    newObject.id = someObject.id || null
    newObject.label = someObject.label || ''
    newObject.description = someObject.description || ''

    newObject.unitUri = someObject.unitUri || ''
    newObject.unitName = someObject.unitName || ''

    newObject.createdAt = someObject.createdAt || null
    newObject.updatedAt = someObject.updatedAt || null

    newObject.createdBy = someObject.createdBy ? Contact.createFromObject(someObject.createdBy) : null
    newObject.updatedBy = someObject.updatedBy ? Contact.createFromObject(someObject.updatedBy) : null

    return newObject
  }
}
