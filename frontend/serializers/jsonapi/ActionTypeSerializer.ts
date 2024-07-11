/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2022
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
import { ActionType } from '@/models/ActionType'

import {
  IJsonApiEntityListEnvelope,
  IJsonApiEntity,
  IJsonApiEntityWithoutDetails,
  IJsonApiEntityWithoutDetailsDataDict
} from '@/serializers/jsonapi/JsonApiTypes'

export class ActionTypeSerializer {
  convertJsonApiObjectListToModelList (jsonApiObjectList: IJsonApiEntityListEnvelope): ActionType[] {
    return jsonApiObjectList.data.map(this.convertJsonApiDataToModel.bind(this))
  }

  convertJsonApiDataToModel (jsonApiData: IJsonApiEntity): ActionType {
    const id = jsonApiData.id.toString()
    const name = jsonApiData.attributes.term
    const url = jsonApiData.links?.self || ''
    const definition = jsonApiData.attributes.definition
    const provenance = jsonApiData.attributes.provenance || ''
    const provenanceUri = jsonApiData.attributes.provenance_uri || ''
    const category = jsonApiData.attributes.category || ''
    const note = jsonApiData.attributes.note || ''
    const actionCategoryId = (jsonApiData.relationships && jsonApiData.relationships.action_category && (jsonApiData.relationships.action_category as IJsonApiEntityWithoutDetailsDataDict).data.id) || null

    let globalProvenanceId = null

    if (jsonApiData.relationships?.global_provenance?.data) {
      const data = jsonApiData.relationships.global_provenance.data as IJsonApiEntityWithoutDetails
      if (data.id) {
        globalProvenanceId = data.id
      }
    }

    return ActionType.createFromObject({
      id,
      name,
      uri: url,
      definition,
      provenance,
      provenanceUri,
      note,
      category,
      actionCategoryId,
      globalProvenanceId
    })
  }

  convertModelToJsonApiData (actionType: ActionType) {
    const attributes = {
      term: actionType.name,
      definition: actionType.definition,
      provenance: actionType.provenance,
      provenance_uri: actionType.provenanceUri,
      category: actionType.category,
      note: actionType.note
    }

    const relationships: any = {}

    if (actionType.globalProvenanceId) {
      relationships.global_provenance = {
        data: {
          id: actionType.globalProvenanceId,
          type: 'GlobalProvenance'
        }
      }
    }
    if (actionType.actionCategoryId) {
      relationships.action_category = {
        data: {
          id: actionType.actionCategoryId,
          type: 'ActionCategory'
        }
      }
    }

    const wrapper: any = {
      type: 'ActionType',
      attributes,
      relationships
    }

    if (actionType.id) {
      wrapper.id = actionType.id
    }

    return wrapper
  }
}
