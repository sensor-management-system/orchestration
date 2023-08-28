/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020 - 2022
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
