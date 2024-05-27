/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2022 - 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
import { ActionCategory } from '@/models/ActionCategory'

import {
  IJsonApiEntityListEnvelope,
  IJsonApiEntity
} from '@/serializers/jsonapi/JsonApiTypes'

export class ActionCategorySerializer {
  convertJsonApiObjectListToModelList (jsonApiObjectList: IJsonApiEntityListEnvelope): ActionCategory[] {
    return jsonApiObjectList.data.map(this.convertJsonApiDataToModel.bind(this))
  }

  convertJsonApiDataToModel (jsonApiData: IJsonApiEntity): ActionCategory {
    const id = jsonApiData.id.toString()
    const name = jsonApiData.attributes.term
    return ActionCategory.createFromObject({ id, name })
  }
}
