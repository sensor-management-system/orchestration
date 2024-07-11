/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2022 - 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
import { PermissionGroup } from '@/models/PermissionGroup'

import {
  IJsonApiEntityListEnvelope,
  IJsonApiEntityEnvelope,
  IJsonApiEntityWithOptionalAttributes
} from '@/serializers/jsonapi/JsonApiTypes'

export class PermissionGroupSerializer {
  convertJsonApiObjectToModel (jsonApiObject: IJsonApiEntityEnvelope): PermissionGroup {
    const data = jsonApiObject.data
    return this.convertJsonApiDataToModel(data)
  }

  convertJsonApiDataToModel (jsonApiData: IJsonApiEntityWithOptionalAttributes): PermissionGroup {
    const attributes = jsonApiData.attributes

    const newEntry = new PermissionGroup()

    newEntry.id = jsonApiData.id.toString()

    if (attributes) {
      newEntry.name = attributes.name || ''
      newEntry.description = attributes.description || ''
    }

    return newEntry
  }

  convertJsonApiObjectListToModelList (jsonApiObjectList: IJsonApiEntityListEnvelope): PermissionGroup[] {
    return jsonApiObjectList.data.map(this.convertJsonApiDataToModel)
  }
}
