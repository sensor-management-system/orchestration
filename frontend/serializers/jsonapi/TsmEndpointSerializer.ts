/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2023
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Maximilian Schaldach <maximilian.schaldach@ufz.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
import { TsmEndpoint } from '@/models/TsmEndpoint'
import { IJsonApiEntityListEnvelope, IJsonApiEntityWithOptionalAttributes } from '@/serializers/jsonapi/JsonApiTypes'

export class TsmEndpointSerializer {
  convertJsonApiObjectListToModelList (jsonApiObjectList: IJsonApiEntityListEnvelope): TsmEndpoint[] {
    return jsonApiObjectList.data.map((jsonApiEntity) => {
      return this.convertJsonApiEntityToModel(jsonApiEntity)
    })
  }

  convertJsonApiEntityToModel (jsonApiData: IJsonApiEntityWithOptionalAttributes): TsmEndpoint {
    const tsmEndpoint = new TsmEndpoint()

    tsmEndpoint.id = jsonApiData.id.toString()
    tsmEndpoint.name = jsonApiData.attributes?.name || ''
    tsmEndpoint.url = jsonApiData.attributes?.url || ''

    return tsmEndpoint
  }
}
