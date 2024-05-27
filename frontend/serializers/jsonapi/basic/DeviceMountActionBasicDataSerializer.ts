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
import { DeviceMountActionBasicData } from '@/models/basic/DeviceMountActionBasicData'

import {
  IJsonApiEntityWithOptionalAttributes
} from '@/serializers/jsonapi/JsonApiTypes'

export class DeviceMountActionBasicDataSerializer {
  convertJsonApiDataToModel (jsonApiData: IJsonApiEntityWithOptionalAttributes): DeviceMountActionBasicData {
    const attributes = jsonApiData.attributes

    return DeviceMountActionBasicData.createFromObject({
      id: jsonApiData.id || '',
      offsetX: attributes?.offset_x || 0,
      offsetY: attributes?.offset_y || 0,
      offsetZ: attributes?.offset_z || 0,
      beginDescription: attributes?.begin_description || '',
      endDescription: attributes?.end_description || '',
      beginDate: DateTime.fromISO(attributes?.begin_date, { zone: 'UTC' }),
      endDate: attributes?.end_date ? DateTime.fromISO(attributes?.end_date, { zone: 'UTC' }) : null,
      epsgCode: attributes?.epsg_code || '',
      x: !isNaN(attributes?.x) ? attributes?.x : null,
      y: !isNaN(attributes?.y) ? attributes?.y : null,
      z: !isNaN(attributes?.z) ? attributes?.z : null,
      elevationDatumName: attributes?.elevation_datum_name || '',
      elevationDatumUri: attributes?.elevation_datum_uri || ''
    })
  }
}
