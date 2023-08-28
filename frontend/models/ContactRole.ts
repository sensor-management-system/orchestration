/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2022
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
import { Contact } from '@/models/Contact'

export interface IContactRole {
  id: string | null
  contact: Contact | null
  roleName: string
  roleUri: string
}

export class ContactRole implements IContactRole {
  private _id: string | null = null
  private _contact: Contact | null = null
  private _roleName: string = ''
  private _roleUri: string = ''

  get id (): string | null {
    return this._id
  }

  set id (newId: string | null) {
    this._id = newId
  }

  get contact (): Contact | null {
    return this._contact
  }

  set contact (newContact: Contact | null) {
    this._contact = newContact
  }

  get roleName (): string {
    return this._roleName
  }

  set roleName (newRoleName: string) {
    this._roleName = newRoleName
  }

  get roleUri (): string {
    return this._roleUri
  }

  set roleUri (newRoleUri: string) {
    this._roleUri = newRoleUri
  }

  static createFromObject (someObject: IContactRole): ContactRole {
    const newObject = new ContactRole()
    newObject.id = someObject.id
    newObject.contact = someObject.contact ? Contact.createFromObject(someObject.contact) : null
    newObject.roleName = someObject.roleName
    newObject.roleUri = someObject.roleUri
    return newObject
  }
}
