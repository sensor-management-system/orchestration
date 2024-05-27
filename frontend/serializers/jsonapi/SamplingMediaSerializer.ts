/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2022
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
import { SamplingMedia } from '@/models/SamplingMedia'

import {
  IJsonApiEntityListEnvelope,
  IJsonApiEntity,
  IJsonApiEntityWithoutDetailsDataDict,
  IJsonApiEntityWithoutDetails
} from '@/serializers/jsonapi/JsonApiTypes'

export class SamplingMediaSerializer {
  convertJsonApiObjectListToModelList (jsonApiObjectList: IJsonApiEntityListEnvelope): SamplingMedia[] {
    return jsonApiObjectList.data.map(this.convertJsonApiDataToModel.bind(this))
  }

  convertJsonApiDataToModel (jsonApiData: IJsonApiEntity): SamplingMedia {
    const id = jsonApiData.id.toString()
    const name = jsonApiData.attributes.term
    const url = jsonApiData.links?.self || ''
    const definition = jsonApiData.attributes.definition
    const provenance = jsonApiData.attributes.provenance || ''
    const provenanceUri = jsonApiData.attributes.provenance_uri || ''
    const category = jsonApiData.attributes.category || ''
    const note = jsonApiData.attributes.note || ''

    const compartmentId = (jsonApiData.relationships && jsonApiData.relationships.compartment && (jsonApiData.relationships.compartment as IJsonApiEntityWithoutDetailsDataDict).data.id) || null

    let globalProvenanceId = null

    if (jsonApiData.relationships?.global_provenance?.data) {
      const data = jsonApiData.relationships.global_provenance.data as IJsonApiEntityWithoutDetails
      if (data.id) {
        globalProvenanceId = data.id
      }
    }

    return SamplingMedia.createFromObject({
      id,
      name,
      definition,
      provenance,
      provenanceUri,
      category,
      note,
      uri: url,
      globalProvenanceId,
      compartmentId
    })
  }

  convertModelToJsonApiData (samplingMedia: SamplingMedia) {
    const attributes = {
      term: samplingMedia.name,
      definition: samplingMedia.definition,
      provenance: samplingMedia.provenance,
      provenance_uri: samplingMedia.provenanceUri,
      category: samplingMedia.category,
      note: samplingMedia.note
    }

    const relationships: any = {}

    if (samplingMedia.globalProvenanceId) {
      relationships.global_provenance = {
        data: {
          id: samplingMedia.globalProvenanceId,
          type: 'GlobalProvenance'
        }
      }
    }

    if (samplingMedia.compartmentId) {
      relationships.compartment = {
        data: {
          id: samplingMedia.compartmentId,
          type: 'Compartment'
        }
      }
    }

    const wrapper: any = {
      type: 'SamplingMedium',
      attributes,
      relationships
    }

    if (samplingMedia.id) {
      wrapper.id = samplingMedia.id
    }

    return wrapper
  }
}
