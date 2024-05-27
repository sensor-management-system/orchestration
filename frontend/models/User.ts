/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
import { IContact, Contact } from '@/models/Contact'

export interface IUser {
  id: string | null
  subject: string
  contact: IContact | null
}

export class User implements IUser {
  private _id: string | null = null
  private _subject: string = ''
  private _contact: Contact | null = null

  get id (): string | null {
    return this._id
  }

  set id (newId: string | null) {
    this._id = newId
  }

  get subject (): string {
    return this._subject
  }

  set subject (newSubject: string) {
    this._subject = newSubject
  }

  get contact (): Contact | null {
    return this._contact
  }

  set contact (newContact: Contact | null) {
    this._contact = newContact
  }

  static createFromObject (someObject: IUser): User {
    const newObject = new User()

    newObject.id = someObject.id
    newObject.subject = someObject.subject
    if (someObject.contact !== null) {
      newObject.contact = Contact.createFromObject(someObject.contact)
    }

    return newObject
  }
}
