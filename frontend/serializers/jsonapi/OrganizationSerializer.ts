/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2026
 * - Nils Brinckmann <nils.brinckmann@gfz.de>
 * - GFZ Helmholtz for Geosciences (GFZ, https://www.gfz.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */

import { Organization } from '@/models/Organization'
import { IJsonApiEntity, IJsonApiEntityEnvelope, IJsonApiEntityListEnvelope, IJsonApiEntityWithOptionalId } from '@/serializers/jsonapi/JsonApiTypes'

export class OrganizationSerializer {
  convertJsonApiObjectToModel (jsonApiObject: IJsonApiEntityEnvelope) {
    const result = new Organization()

    const data = jsonApiObject.data
    result.id = data.id || ''
    const attributes = data.attributes

    result.name = attributes.name
    result.ror = attributes.ror || ''
    result.abbreviation = attributes.abbreviation || ''

    return result
  }

  convertJsonApiObjectListToModelList (jsonApiObjectList: IJsonApiEntityListEnvelope): Organization[] {
    return jsonApiObjectList.data.map((model: IJsonApiEntity) => {
      return this.convertJsonApiObjectToModel({ data: model })
    })
  }

  convertModelToJsonApiData (organization: Organization): IJsonApiEntityWithOptionalId {
    const data: IJsonApiEntityWithOptionalId = {
      type: 'organization',
      attributes: {
        name: organization.name,
        ror: organization.ror,
        abbreviation: organization.abbreviation
      }
    }

    if (organization.id) {
      data.id = organization.id
    }

    return data
  }
}
