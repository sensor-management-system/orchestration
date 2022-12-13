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
