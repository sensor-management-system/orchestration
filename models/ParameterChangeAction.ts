/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020 - 2023
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

import { Parameter } from '@/models/Parameter'
import { IContact, Contact } from '@/models/Contact'
import { IDateCompareable } from '@/modelUtils/Compareables'

export interface IParameterChangeAction {
  id: string | null
  date: DateTime | null
  value: string
  description: string
  contact: Contact | null
  parameter: Parameter | null

  createdAt: DateTime | null
  updatedAt: DateTime | null

  createdBy: IContact | null
  updatedBy: IContact | null
}

export type IParameterChangeActionLike = Partial<IParameterChangeAction>

export class ParameterChangeAction implements IParameterChangeAction, IDateCompareable {
  private _id: string | null = null
  private _date: DateTime | null = null
  private _value: string = ''
  private _description: string = ''
  private _contact: Contact | null = null
  private _parameter: Parameter | null = null

  private _createdAt: DateTime | null = null
  private _updatedAt: DateTime | null = null

  private _createdBy: IContact | null = null
  private _updatedBy: IContact | null = null

  get id (): string | null {
    return this._id
  }

  set id (value: string | null) {
    this._id = value
  }

  get date (): DateTime | null {
    return this._date
  }

  set date (value: DateTime | null) {
    this._date = value
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

  set description (description: string) {
    this._description = description
  }

  get contact (): Contact | null {
    return this._contact
  }

  set contact (value: Contact | null) {
    this._contact = value
  }

  get parameter (): Parameter | null {
    return this._parameter
  }

  set parameter (value: Parameter | null) {
    this._parameter = value
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

  get isParameterChangeAction (): boolean {
    return true
  }

  /**
   * creates an instance from an existing IParameterChangeAction-like object
   *
   * @static
   * @param {IParameterChangeActionLike} someObject - an IParameterChangeAction like object
   * @return {ParameterChangeAction} a cloned instance of the original object
   */
  static createFromObject (someObject: IParameterChangeActionLike): ParameterChangeAction {
    const action = new ParameterChangeAction()
    action.id = typeof someObject.id !== 'undefined' && someObject.id !== null ? someObject.id : null
    action.date = someObject.date || null
    action.value = someObject.value || ''
    action.description = someObject.description || ''
    action.contact = someObject.contact ? Contact.createFromObject(someObject.contact) : null
    action.parameter = someObject.parameter ? Parameter.createFromObject(someObject.parameter) : null

    action.createdAt = someObject.createdAt || null
    action.updatedAt = someObject.updatedAt || null

    action.createdBy = someObject.createdBy ? Contact.createFromObject(someObject.createdBy) : null
    action.updatedBy = someObject.updatedBy ? Contact.createFromObject(someObject.updatedBy) : null

    return action
  }
}
