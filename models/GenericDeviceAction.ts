/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020, 2021
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
import { IAction } from '@/models/Action'

export interface IGenericDeviceAction extends IAction {
  actionTypeName: string
  actionTypeUrl: string
  beginDate: DateTime | null
  endDate: DateTime | null
  isGenericDeviceAction: boolean
}

export class GenericDeviceAction implements IGenericDeviceAction {
  private _id: string | null = null
  private _description: string = ''
  private _actionTypeName: string = ''
  private _actionTypeUrl: string = ''
  private _beginDate: DateTime | null = null
  private _endDate: DateTime | null = null
  private _contact: Contact | null = null

  /**
   * returns an empty instance
   *
   * @static
   * @return {GenericDeviceAction} an empty instance
   */
  static createEmpty (): GenericDeviceAction {
    return new GenericDeviceAction()
  }

  /**
   * creates an instance from an existing IGenericDeviceAction-like object
   *
   * @static
   * @param {IGenericDeviceAction} someObject - an IGenericDeviceAction like object
   * @return {GenericDeviceAction} a cloned instance of the original object
   */
  static createFromObject (someObject: IGenericDeviceAction) : GenericDeviceAction {
    const action = new GenericDeviceAction()
    action.id = someObject.id
    action.description = someObject.description
    action.actionTypeName = someObject.actionTypeName
    action.actionTypeUrl = someObject.actionTypeUrl
    // TODO: find the proper way to create new DateTime instances from other DateTime-ish instances
    action.beginDate = someObject.beginDate ? someObject.beginDate : null
    // TODO: find the proper way to create new DateTime instances from other DateTime-ish instances
    action.endDate = someObject.endDate ? someObject.endDate : null
    action.contact = someObject.contact ? Contact.createFromObject(someObject.contact) : null
    return action
  }

  get id (): string | null {
    return this._id
  }

  set id (id: string | null) {
    this._id = id
  }

  get description (): string {
    return this._description
  }

  set description (description: string) {
    this._description = description
  }

  get actionTypeUrl (): string {
    return this._actionTypeUrl
  }

  set actionTypeUrl (actionTypeUrl: string) {
    this._actionTypeUrl = actionTypeUrl
  }

  get actionTypeName (): string {
    return this._actionTypeName
  }

  set actionTypeName (actionTypeName: string) {
    this._actionTypeName = actionTypeName
  }

  get beginDate (): DateTime | null {
    return this._beginDate
  }

  set beginDate (date: DateTime | null) {
    this._beginDate = date
  }

  get endDate (): DateTime | null {
    return this._endDate
  }

  set endDate (date: DateTime | null) {
    this._endDate = date
  }

  get contact (): Contact | null {
    return this._contact
  }

  set contact (contact: Contact | null) {
    this._contact = contact
  }

  get isGenericDeviceAction (): boolean {
    return true
  }
}
