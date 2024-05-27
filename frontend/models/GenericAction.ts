/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
import { DateTime } from 'luxon'
import { Attachment } from '@/models/Attachment'
import { Contact } from '@/models/Contact'
import { IActionCommonDetails, ActionCommonDetails } from '@/models/ActionCommonDetails'
import { IDateCompareable } from '@/modelUtils/Compareables'
import { IActionKind, KIND_OF_ACTION_TYPE_GENERIC_ACTION } from '@/models/ActionKind'

export interface IGenericAction extends IActionCommonDetails {
  actionTypeName: string
  actionTypeUrl: string
  beginDate: DateTime | null
  endDate: DateTime | null
}

type IconMapping = {
  [key: string]: string;
};

export class GenericAction extends ActionCommonDetails implements IGenericAction, IDateCompareable, IActionKind {
  private _actionTypeName: string = ''
  private _actionTypeUrl: string = ''
  private _beginDate: DateTime | null = null
  private _endDate: DateTime | null = null

  /**
   * returns an empty instance
   *
   * @static
   * @return {GenericAction} an empty instance
   */
  static createEmpty (): GenericAction {
    return new GenericAction()
  }

  /**
   * creates an instance from an existing IGenericAction-like object
   *
   * @static
   * @param {IGenericAction} someObject - an IGenericAction like object
   * @return {GenericAction} a cloned instance of the original object
   */
  static createFromObject (someObject: IGenericAction): GenericAction {
    const action = new GenericAction()
    action.id = someObject.id
    action.description = someObject.description
    action.actionTypeName = someObject.actionTypeName
    action.actionTypeUrl = someObject.actionTypeUrl
    action.beginDate = someObject.beginDate
    action.endDate = someObject.endDate
    action.contact = someObject.contact ? Contact.createFromObject(someObject.contact) : null
    action.attachments = someObject.attachments.map(i => Attachment.createFromObject(i))
    return action
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

  get isGenericAction (): boolean {
    return true
  }

  get date (): DateTime | null {
    return this.beginDate
  }

  get icon (): string {
    const iconMapping: IconMapping = {
      observation: 'mdi-telescope',
      maintenance: 'mdi-wrench',
      rental: 'mdi-hand-heart',
      visit: 'mdi-castle',
      'platform application': 'mdi-crane',
      'manual data retrieval': 'mdi-human-dolly'
    }

    for (const key in iconMapping) {
      if (this.actionTypeName.toLowerCase().includes(key)) {
        return iconMapping[key]
      }
    }
    return 'mdi-card-bulleted'
  }

  get color (): string {
    return 'grey'
  }

  get kind (): string {
    return KIND_OF_ACTION_TYPE_GENERIC_ACTION
  }
}
