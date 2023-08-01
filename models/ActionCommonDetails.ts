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
import { Attachment } from '@/models/Attachment'
import { Contact } from '@/models/Contact'

export interface IActionCommonDetails {
  id: string | null
  description: string
  contact: Contact | null
  attachments: Attachment[]
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
}
