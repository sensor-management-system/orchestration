/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2026
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */

import {
  IJsonApiEntityListEnvelope,
  IJsonApiEntity
} from '@/serializers/jsonapi/JsonApiTypes'

import { ISerializer } from '@/serializers/jsonapi/ISerializer'

export abstract class AbstractSerializer<T> implements ISerializer<T> {
  convertJsonApiObjectListToModelList (jsonApiObjectList: IJsonApiEntityListEnvelope): T[] {
    return jsonApiObjectList.data.map(this.convertJsonApiDataToModel.bind(this))
  }

  abstract convertJsonApiDataToModel (jsonApiData: IJsonApiEntity): T
  abstract convertModelToJsonApiData (t: T): object
}
