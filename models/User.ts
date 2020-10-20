/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020
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

  static createFromObjet (someObject: IUser): User {
    const newObject = new User()

    newObject.id = someObject.id
    newObject.subject = someObject.subject
    if (someObject.contact !== null) {
      newObject.contact = Contact.createFromObject(someObject.contact)
    }

    return newObject
  }
}
