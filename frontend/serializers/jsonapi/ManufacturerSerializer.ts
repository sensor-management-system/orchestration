/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2022
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
import { Manufacturer } from '@/models/Manufacturer'

import {
  IJsonApiEntityListEnvelope,
  IJsonApiEntity,
  IJsonApiEntityWithoutDetails
} from '@/serializers/jsonapi/JsonApiTypes'

export class ManufacturerSerializer {
  convertJsonApiObjectListToModelList (jsonApiObjectList: IJsonApiEntityListEnvelope): Manufacturer[] {
    return jsonApiObjectList.data.map(this.convertJsonApiDataToModel.bind(this))
  }

  convertJsonApiDataToModel (jsonApiData: IJsonApiEntity): Manufacturer {
    const id = jsonApiData.id.toString()
    const name = jsonApiData.attributes.term
    const definition = jsonApiData.attributes.definition || ''
    const provenance = jsonApiData.attributes.provenance || ''
    const provenanceUri = jsonApiData.attributes.provenance_uri || ''
    const category = jsonApiData.attributes.category || ''
    const note = jsonApiData.attributes.note || ''
    const url = jsonApiData.links?.self || ''
    let globalProvenanceId = null

    if (jsonApiData.relationships?.global_provenance?.data) {
      const data = jsonApiData.relationships.global_provenance.data as IJsonApiEntityWithoutDetails
      if (data.id) {
        globalProvenanceId = data.id
      }
    }

    return Manufacturer.createFromObject({
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

  convertModelToJsonApiData (manufacturer: Manufacturer) {
    const attributes = {
      term: manufacturer.name,
      definition: manufacturer.definition,
      provenance: manufacturer.provenance,
      provenance_uri: manufacturer.provenanceUri,
      category: manufacturer.category,
      note: manufacturer.note
    }

    const relationships: any = {}

    if (manufacturer.globalProvenanceId) {
      relationships.global_provenance = {
        data: {
          id: manufacturer.globalProvenanceId,
          type: 'GlobalProvenance'
        }
      }
    }

    const wrapper: any = {
      type: 'Manufacturer',
      attributes,
      relationships
    }

    if (manufacturer.id) {
      wrapper.id = manufacturer.id
    }

    return wrapper
  }
}
