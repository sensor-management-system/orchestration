/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2022 - 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
import { DateTime } from 'luxon'
import { UserInfo } from '@/models/UserInfo'

import {
  IJsonApiEntityEnvelope,
  IJsonApiEntityWithOptionalAttributes,
  IJsonApiEntityWithoutDetails
} from '@/serializers/jsonapi/JsonApiTypes'

export class UserInfoSerializer {
  convertJsonApiObjectToModel (jsonApiObject: IJsonApiEntityEnvelope): UserInfo {
    const data = jsonApiObject.data
    return this.convertJsonApiDataToModel(data)
  }

  convertJsonApiDataToModel (jsonApiData: IJsonApiEntityWithOptionalAttributes): UserInfo {
    const attributes = jsonApiData.attributes

    const newEntry = new UserInfo()

    newEntry.id = jsonApiData.id.toString()

    if (attributes) {
      newEntry.active = attributes.active || false
      newEntry.isSuperUser = attributes.is_superuser || false
      newEntry.isExportControl = attributes.is_export_control || false
      if (Array.isArray(attributes?.member) && attributes?.member?.length) {
        newEntry.member = attributes.member.map(e => e.toString())
      }
      if (Array.isArray(attributes?.admin) && attributes?.admin?.length) {
        newEntry.admin = attributes.admin.map(e => e.toString())
      }
      newEntry.apikey = attributes.apikey || null
      newEntry.termsOfUseAgreementDate = null
      if (attributes.terms_of_use_agreement_date) {
        newEntry.termsOfUseAgreementDate = DateTime.fromISO(attributes.terms_of_use_agreement_date, { zone: 'UTC' })
      }
    }
    const relationships = jsonApiData.relationships

    if (relationships && relationships.contact && relationships.contact.data) {
      const data = relationships.contact.data as IJsonApiEntityWithoutDetails
      newEntry.contactId = data.id != null ? String(data.id) : null
    }

    return newEntry
  }
}
