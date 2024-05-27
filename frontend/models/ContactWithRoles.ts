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
import { ContactRole } from '@/models/ContactRole'

export class ContactWithRoles {
  private _contact: Contact
  private _roles: ContactRole[]

  constructor (contact: Contact, roles: ContactRole[]) {
    this._contact = contact
    this._roles = roles
  }

  get contact (): Contact {
    return this._contact
  }

  get roles (): ContactRole[] {
    return this._roles
  }
}
