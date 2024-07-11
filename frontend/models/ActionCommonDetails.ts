/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2023
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
import { Attachment } from '@/models/Attachment'
import { Contact } from '@/models/Contact'

export interface IActionCommonDetails {
  id: string | null
  description: string
  contact: Contact | null
  attachments: Attachment[]
  icon: string
  color: string
}

export type IActionCommonDetailsLike = Partial<IActionCommonDetails>

/**
 * a very unspecific Action class
 *
 * this class in mainly used for inheritance in derived classes
 *
 * @implements IActionCommonDetails
 */
export class ActionCommonDetails implements IActionCommonDetails {
  private _id: string | null = null
  private _description: string = ''
  private _contact: Contact | null = null
  private _attachments: Attachment[] = []
  private _color: string = ''
  private _icon: string = ''

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

  get contact (): Contact | null {
    return this._contact
  }

  set contact (contact: Contact | null) {
    this._contact = contact
  }

  get attachments (): Attachment[] {
    return this._attachments
  }

  set attachments (attachments: Attachment[]) {
    this._attachments = attachments
  }

  static createFromObject (value: IActionCommonDetailsLike): ActionCommonDetails {
    const action = new ActionCommonDetails()
    action.id = value.id || null
    action.description = value.description || ''
    action.contact = value.contact ? Contact.createFromObject(value.contact) : null
    action.attachments = value.attachments ? value.attachments.map(a => Attachment.createFromObject(a)) : []
    return action
  }

  get color (): string {
    return this._color
  }

  get icon (): string {
    return this._icon
  }
}
