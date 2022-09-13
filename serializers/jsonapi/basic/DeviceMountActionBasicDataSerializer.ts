/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020-2022
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
      endDate: attributes?.end_date ? DateTime.fromISO(attributes?.end_date, { zone: 'UTC' }) : null
    })
  }
}
