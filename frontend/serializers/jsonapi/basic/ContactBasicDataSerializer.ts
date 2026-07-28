/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2023
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
import { DateTime } from 'luxon'

import { ContactBasicData } from '@/models/basic/ContactBasicData'

import {
  IJsonApiEntityWithOptionalAttributes
} from '@/serializers/jsonapi/JsonApiTypes'

export class ContactBasicDataSerializer {
  convertJsonApiDataToModel (jsonApiData: IJsonApiEntityWithOptionalAttributes): ContactBasicData {
    const attributes = jsonApiData.attributes

    const newEntry = ContactBasicData.createEmpty()

    newEntry.id = jsonApiData.id.toString()

    if (attributes) {
      newEntry.givenName = attributes.given_name || ''
      newEntry.familyName = attributes.family_name || ''
      newEntry.website = attributes.website || ''
      newEntry.email = attributes.email
      newEntry.organization = attributes.organization || ''
      newEntry.orcid = attributes.orcid || ''
      newEntry.createdAt = attributes.created_at != null ? DateTime.fromISO(attributes.created_at, { zone: 'UTC' }) : null
      newEntry.updatedAt = attributes.updated_at != null ? DateTime.fromISO(attributes.updated_at, { zone: 'UTC' }) : null
      newEntry.telephone = attributes.telephone || ''
      newEntry.faxNumber = attributes.fax_number || ''
      newEntry.city = attributes.city || ''
      newEntry.zipCode = attributes.zip_code || ''
      newEntry.administrativeArea = attributes.administrative_area || ''
      newEntry.country = attributes.country || ''
      newEntry.street = attributes.street || ''
      newEntry.streetNumber = attributes.street_number || ''
      newEntry.room = attributes.room || ''
      newEntry.building = attributes.building || ''
    }

    return newEntry
  }
}
