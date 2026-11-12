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

export interface ISerializer<T> {
  convertJsonApiObjectListToModelList (jsonApiObjectList: IJsonApiEntityListEnvelope): T[]
  convertJsonApiDataToModel (jsonApiData: IJsonApiEntity): T
  convertModelToJsonApiData (t: T): object
}
