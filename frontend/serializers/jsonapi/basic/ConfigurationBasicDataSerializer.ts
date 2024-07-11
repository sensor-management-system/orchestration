/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */

import { DateTime } from 'luxon'

import { ConfigurationBasicData } from '@/models/basic/ConfigurationBasicData'

import { IJsonApiEntityWithOptionalAttributes } from '@/serializers/jsonapi/JsonApiTypes'

export class ConfigurationBasicDataSerializer {
  convertJsonApiDataToModel (jsonApiData: IJsonApiEntityWithOptionalAttributes): ConfigurationBasicData {
    const configuration = new ConfigurationBasicData()

    const attributes = jsonApiData.attributes

    configuration.id = jsonApiData.id.toString()
    if (attributes) {
      configuration.label = attributes.label || ''
      configuration.description = attributes.description || ''
      configuration.project = attributes.project || ''
      configuration.campaign = attributes.campaign || ''
      configuration.status = attributes.status || ''

      configuration.startDate = attributes.start_date ? DateTime.fromISO(attributes.start_date, { zone: 'UTC' }) : null
      configuration.endDate = attributes.end_date ? DateTime.fromISO(attributes.end_date, { zone: 'UTC' }) : null
      configuration.archived = attributes.archived || false
    }

    return configuration
  }
}
