/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2022 - 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */

import { CvContactRole } from '@/models/CvContactRole'

import {
  IJsonApiEntityListEnvelope,
  IJsonApiEntity,
  IJsonApiEntityWithoutDetails
} from '@/serializers/jsonapi/JsonApiTypes'

export class CvContactRoleSerializer {
  convertJsonApiObjectListToModelList (jsonApiObjectList: IJsonApiEntityListEnvelope): CvContactRole[] {
    return jsonApiObjectList.data.map(this.convertJsonApiDataToModel.bind(this))
  }

  convertJsonApiDataToModel (jsonApiData: IJsonApiEntity): CvContactRole {
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

    return CvContactRole.createFromObject({
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

  convertModelToJsonApiData (contactRole: CvContactRole) {
    const attributes = {
      term: contactRole.name,
      definition: contactRole.definition,
      provenance: contactRole.provenance,
      provenance_uri: contactRole.provenanceUri,
      category: contactRole.category,
      note: contactRole.note
    }

    const relationships: any = {}

    if (contactRole.globalProvenanceId) {
      relationships.global_provenance = {
        data: {
          id: contactRole.globalProvenanceId,
          type: 'GlobalProvenance'
        }
      }
    }

    const wrapper: any = {
      type: 'ContactRole',
      attributes,
      relationships
    }

    if (contactRole.id) {
      wrapper.id = contactRole.id
    }

    return wrapper
  }
}
