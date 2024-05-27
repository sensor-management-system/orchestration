/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2022 - 2023
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
import { AggregationType } from '@/models/AggregationType'

import {
  IJsonApiEntityListEnvelope,
  IJsonApiEntity,
  IJsonApiEntityWithoutDetails
} from '@/serializers/jsonapi/JsonApiTypes'

export class AggregationTypeSerializer {
  convertJsonApiObjectListToModelList (jsonApiObjectList: IJsonApiEntityListEnvelope): AggregationType[] {
    return jsonApiObjectList.data.map(this.convertJsonApiDataToModel.bind(this))
  }

  convertJsonApiDataToModel (jsonApiData: IJsonApiEntity): AggregationType {
    const id = jsonApiData.id.toString()
    const name = jsonApiData.attributes.term
    const url = jsonApiData.links?.self || ''
    const definition = jsonApiData.attributes.definition
    const provenance = jsonApiData.attributes.provenance || ''
    const provenanceUri = jsonApiData.attributes.provenance_uri || ''
    const category = jsonApiData.attributes.category || ''
    const note = jsonApiData.attributes.note || ''

    let globalProvenanceId = null

    if (jsonApiData.relationships?.global_provenance?.data) {
      const data = jsonApiData.relationships.global_provenance.data as IJsonApiEntityWithoutDetails
      if (data.id) {
        globalProvenanceId = data.id
      }
    }

    return AggregationType.createFromObject({
      id,
      name,
      definition,
      provenance,
      provenanceUri,
      category,
      note,
      uri: url,
      globalProvenanceId
    })
  }

  convertModelToJsonApiData (aggregationType: AggregationType) {
    const attributes = {
      term: aggregationType.name,
      definition: aggregationType.definition,
      provenance: aggregationType.provenance,
      provenance_uri: aggregationType.provenanceUri,
      category: aggregationType.category,
      note: aggregationType.note
    }

    const relationships: any = {}

    if (aggregationType.globalProvenanceId) {
      relationships.global_provenance = {
        data: {
          id: aggregationType.globalProvenanceId,
          type: 'GlobalProvenance'
        }
      }
    }

    const wrapper: any = {
      type: 'AggregationType',
      attributes,
      relationships
    }

    if (aggregationType.id) {
      wrapper.id = aggregationType.id
    }

    return wrapper
  }
}
