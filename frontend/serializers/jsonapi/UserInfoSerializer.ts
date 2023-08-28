/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2022 - 2023
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
