/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2023 - 2024
 * - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
import { DateTime } from 'luxon'

import { DeviceBasicData } from '@/models/basic/DeviceBasicData'

import {
  IJsonApiEntityWithOptionalAttributes
} from '@/serializers/jsonapi/JsonApiTypes'

export class DeviceBasicDataSerializer {
  convertJsonApiDataToModel (jsonApiData: IJsonApiEntityWithOptionalAttributes): DeviceBasicData {
    const result = DeviceBasicData.createEmpty()

    const attributes = jsonApiData.attributes

    result.id = jsonApiData.id.toString()

    if (attributes) {
      result.description = attributes.description || ''
      result.shortName = attributes.short_name || ''
      result.longName = attributes.long_name || ''
      result.manufacturerUri = attributes.manufacturer_uri || ''
      result.manufacturerName = attributes.manufacturer_name || ''
      result.model = attributes.model || ''
      result.deviceTypeUri = attributes.device_type_uri || ''
      result.deviceTypeName = attributes.device_type_name || ''
      result.statusUri = attributes.status_uri || ''
      result.statusName = attributes.status_name || ''
      result.website = attributes.website || ''
      result.createdAt = attributes.created_at != null ? DateTime.fromISO(attributes.created_at, { zone: 'UTC' }) : null
      result.updatedAt = attributes.updated_at != null ? DateTime.fromISO(attributes.updated_at, { zone: 'UTC' }) : null

      result.inventoryNumber = attributes.inventory_number || ''
      result.serialNumber = attributes.serial_number || ''
      result.persistentIdentifier = attributes.persistent_identifier || ''

      result.archived = attributes.archived || false
    }

    return result
  }
}
