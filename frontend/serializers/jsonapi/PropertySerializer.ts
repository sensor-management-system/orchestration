/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2022
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
import { Property } from '@/models/Property'

import {
  IJsonApiEntityListEnvelope,
  IJsonApiEntity,
  IJsonApiEntityWithoutDetailsDataDict,
  IJsonApiEntityWithoutDetails
} from '@/serializers/jsonapi/JsonApiTypes'

export class PropertySerializer {
  convertJsonApiObjectListToModelList (jsonApiObjectList: IJsonApiEntityListEnvelope): Property[] {
    return jsonApiObjectList.data.map(this.convertJsonApiDataToModel.bind(this))
  }

  convertJsonApiDataToModel (jsonApiData: IJsonApiEntity): Property {
    const id = jsonApiData.id.toString()
    const name = jsonApiData.attributes.term
    const url = jsonApiData.links?.self || ''
    const definition = jsonApiData.attributes.definition
    const provenance = jsonApiData.attributes.provenance || ''
    const provenanceUri = jsonApiData.attributes.provenance_uri || ''
    const category = jsonApiData.attributes.category || ''
    const note = jsonApiData.attributes.note || ''
    const samplingMediaId = (jsonApiData.relationships && jsonApiData.relationships.sampling_media && (jsonApiData.relationships.sampling_media as IJsonApiEntityWithoutDetailsDataDict).data.id) || null
    const aggregationTypeId = (jsonApiData.relationships && jsonApiData.relationships.aggregation_type && (jsonApiData.relationships.aggregation_type as IJsonApiEntityWithoutDetailsDataDict).data.id) || null

    let globalProvenanceId = null

    if (jsonApiData.relationships?.global_provenance?.data) {
      const data = jsonApiData.relationships.global_provenance.data as IJsonApiEntityWithoutDetails
      if (data.id) {
        globalProvenanceId = data.id
      }
    }

    return Property.createFromObject({
      id,
      name,
      definition,
      provenance,
      provenanceUri,
      category,
      note,
      uri: url,
      globalProvenanceId,
      samplingMediaId,
      aggregationTypeId
    })
  }

  convertModelToJsonApiData (cvProperty: Property) {
    const attributes = {
      term: cvProperty.name,
      definition: cvProperty.definition,
      provenance: cvProperty.provenance,
      provenance_uri: cvProperty.provenanceUri,
      category: cvProperty.category,
      note: cvProperty.note
    }

    const relationships: any = {}

    if (cvProperty.globalProvenanceId) {
      relationships.global_provenance = {
        data: {
          id: cvProperty.globalProvenanceId,
          type: 'GlobalProvenance'
        }
      }
    }

    if (cvProperty.samplingMediaId) {
      relationships.sampling_media = {
        data: {
          id: cvProperty.samplingMediaId,
          type: 'SamplingMedium'
        }
      }
    }

    if (cvProperty.aggregationTypeId) {
      relationships.aggregation_type = {
        data: {
          id: cvProperty.aggregationTypeId,
          type: 'AggregationType'
        }
      }
    }

    const wrapper: any = {
      type: 'MeasuredQuantity',
      attributes,
      relationships
    }

    if (cvProperty.id) {
      wrapper.id = cvProperty.id
    }

    return wrapper
  }
}
