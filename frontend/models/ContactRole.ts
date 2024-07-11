/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2022 - 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
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
