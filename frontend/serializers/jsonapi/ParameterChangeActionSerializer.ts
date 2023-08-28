/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2023
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

import { DateTime } from 'luxon'

import { IContact, Contact } from '@/models/Contact'
import { IParameterChangeAction, ParameterChangeAction } from '@/models/ParameterChangeAction'
import { Parameter } from '@/models/Parameter'

import {
  IJsonApiEntityListEnvelope,
  IJsonApiEntityEnvelope,
  IJsonApiEntity,
  IJsonApiEntityWithOptionalId,
  IJsonApiEntityWithoutDetails,
  IJsonApiEntityWithOptionalAttributes,
  IJsonApiEntityWithoutDetailsDataDictList,
  IJsonApiTypedEntityWithoutDetailsDataDictList,
  IJsonApiRelationships
} from '@/serializers/jsonapi/JsonApiTypes'

import { ContactSerializer } from '@/serializers/jsonapi/ContactSerializer'
import { ParameterSerializer, ParameterEntityType } from '@/serializers/jsonapi/ParameterSerializer'

export enum ParameterChangeActionEntityType {
  DEVICE_PARAMETER_VALUE_CHANGE = 'device_parameter_value_change_action',
  PLATFORM_PARAMETER_VALUE_CHANGE = 'platform_parameter_value_change_action',
  CONFIGURATION_PARAMETER_VALUE_CHANGE = 'configuration_parameter_value_change_action'
}

export enum ParameterChangeActionRelationEntityType {
  DEVICE_PARAMETER = 'device_parameter',
  PLATFORM_PARAMETER = 'platform_parameter',
  CONFIGURATION_PARAMETER = 'configuration_parameter'
}

export interface IParameterChangeActionRelation {
  entityType: ParameterChangeActionRelationEntityType
  id: string
}

const parameterSerializerEntityLookup = {
  [ParameterChangeActionEntityType.DEVICE_PARAMETER_VALUE_CHANGE]: ParameterEntityType.DEVICE,
  [ParameterChangeActionEntityType.PLATFORM_PARAMETER_VALUE_CHANGE]: ParameterEntityType.PLATFORM,
  [ParameterChangeActionEntityType.CONFIGURATION_PARAMETER_VALUE_CHANGE]: ParameterEntityType.CONFIGURATION
}

const parameterRelationshipEntityLookup = {
  [ParameterChangeActionEntityType.DEVICE_PARAMETER_VALUE_CHANGE]: ParameterChangeActionRelationEntityType.DEVICE_PARAMETER,
  [ParameterChangeActionEntityType.PLATFORM_PARAMETER_VALUE_CHANGE]: ParameterChangeActionRelationEntityType.PLATFORM_PARAMETER,
  [ParameterChangeActionEntityType.CONFIGURATION_PARAMETER_VALUE_CHANGE]: ParameterChangeActionRelationEntityType.CONFIGURATION_PARAMETER
}

export class ParameterChangeActionSerializer {
  private _contactSerializer: ContactSerializer = new ContactSerializer()
  private _parameterSerializer: ParameterSerializer
  private _entityType: ParameterChangeActionEntityType

  constructor (entityType: ParameterChangeActionEntityType) {
    this._entityType = entityType
    const serializerEntityType = parameterSerializerEntityLookup[entityType]
    this._parameterSerializer = new ParameterSerializer(serializerEntityType)
  }

  /**
   * converts a JSONAPI response with multiple parameterChangeAction objects into a list of ParameterChangeAction instances
   *
   * @param {IJsonApiEntityListEnvelope} jsonApiObjectList - the JSONAPI response object
   * @returns {ParameterChangeAction[]} a list of Paramter instances
   */
  convertJsonApiObjectListToModelList (jsonApiObjectList: IJsonApiEntityListEnvelope): ParameterChangeAction[] {
    const included = jsonApiObjectList.included || []
    return jsonApiObjectList.data.map((data: IJsonApiEntity) => {
      return this.convertJsonApiDataToModel(data, included)
    })
  }

  /**
   * converts a JSONAPI response for a single parameterChangeAction into a ParameterChangeAction instance
   *
   * @param {IJsonApiEntityEnvelope} jsonApiObject - the JSONAPI response object
   * @returns {ParameterChangeAction} a ParameterChangeAction instance
   */
  convertJsonApiObjectToModel (jsonApiObject: IJsonApiEntityEnvelope): ParameterChangeAction {
    const included = jsonApiObject.included || []
    return this.convertJsonApiDataToModel(jsonApiObject.data, included)
  }

  /**
   * converts a JSONAPI object entity into a ParameterChangeAction instance
   *
   * @param {IJsonApiEntityWithOptionalAttributes} jsonApiData - the JSONAPI entity
   * @param {IJsonApiEntityWithOptionalAttributes[]} included - a list of included entities
   * @returns {ParameterChangeAction} a ParameterChangeAction instance
   */
  convertJsonApiDataToModel (jsonApiData: IJsonApiEntityWithOptionalAttributes, included: IJsonApiEntityWithOptionalAttributes[] = []): ParameterChangeAction {
    const id = jsonApiData.id.toString()
    const date = jsonApiData.attributes?.date != null ? DateTime.fromISO(jsonApiData.attributes.date, { zone: 'UTC' }) : null
    const value = jsonApiData.attributes?.value || ''
    const description = jsonApiData.attributes?.description || ''
    const createdAt = jsonApiData.attributes?.created_at != null ? DateTime.fromISO(jsonApiData.attributes.created_at, { zone: 'UTC' }) : null
    const updatedAt = jsonApiData.attributes?.updated_at != null ? DateTime.fromISO(jsonApiData.attributes.updated_at, { zone: 'UTC' }) : null

    const relationships = jsonApiData.relationships || {}
    const relationshipEntityType = parameterRelationshipEntityLookup[this._entityType]

    let parameter: Parameter | null = null
    if (relationshipEntityType in relationships && relationships[relationshipEntityType].data && 'id' in relationships[relationshipEntityType].data!) {
      parameter = this._parameterSerializer.convertJsonApiRelationshipsSingleModel(relationships, included)
    }

    let contact: Contact | null = null
    if (relationships.contact?.data && 'id' in relationships.contact?.data) {
      contact = this._contactSerializer.convertJsonApiRelationshipsSingleModel(relationships, included).contact
    }

    let createdBy: IContact | null = null
    if (relationships.created_by?.data && 'id' in relationships.created_by?.data) {
      const userId = (relationships.created_by.data as IJsonApiEntityWithoutDetails).id
      createdBy = this._contactSerializer.getContactFromIncludedByUserId(userId, included) || null
    }

    let updatedBy: IContact | null = null
    if (relationships.updated_by?.data && 'id' in relationships.updated_by?.data) {
      const userId = (relationships.updated_by.data as IJsonApiEntityWithoutDetails).id
      updatedBy = this._contactSerializer.getContactFromIncludedByUserId(userId, included) || null
    }

    return ParameterChangeAction.createFromObject({
      id,
      date,
      description,
      value,
      contact,
      parameter,
      createdAt,
      updatedAt,
      createdBy,
      updatedBy
    })
  }

  convertJsonApiRelationshipsModelList (relationships: IJsonApiRelationships, included: IJsonApiEntityWithOptionalAttributes[]): ParameterChangeAction[] {
    const entityTypePlural = this._entityType + 's'
    const parameterChangeActionIds = []
    if (relationships[entityTypePlural]) {
      const parameterChangeActionObject = relationships[entityTypePlural] as IJsonApiEntityWithoutDetailsDataDictList
      if (parameterChangeActionObject.data && parameterChangeActionObject.data.length > 0) {
        for (const relationShipParameterData of parameterChangeActionObject.data) {
          const parameterChangeActionId = relationShipParameterData.id
          parameterChangeActionIds.push(parameterChangeActionId)
        }
      }
    }

    const result: ParameterChangeAction[] = []
    if (included && included.length > 0) {
      for (const includedEntry of included) {
        if (includedEntry.type === this._entityType) {
          const parameterChangeActionId = includedEntry.id
          if (parameterChangeActionIds.includes(parameterChangeActionId)) {
            const parameterChangeAction = this.convertJsonApiDataToModel(includedEntry)
            result.push(parameterChangeAction)
          }
        }
      }
    }

    return result
  }

  convertModelListToJsonApiRelationshipObject (parameterChangeActions: ParameterChangeAction[]): IJsonApiTypedEntityWithoutDetailsDataDictList {
    const entityTypePlural = this._entityType + 's'
    return {
      [entityTypePlural]: {
        data: this.convertModelListToTupleListWithIdAndType(parameterChangeActions)
      }
    }
  }

  convertModelListToTupleListWithIdAndType (parameterChangeActions: ParameterChangeAction[]): IJsonApiEntityWithoutDetails[] {
    const result: IJsonApiEntityWithoutDetails[] = []
    for (const parameterChangeAction of parameterChangeActions) {
      if (parameterChangeAction.id !== null) {
        result.push({
          id: parameterChangeAction.id,
          type: this._entityType
        })
      }
    }
    return result
  }

  convertModelToJsonApiData (parameterChangeAction: IParameterChangeAction, relation: IParameterChangeActionRelation): IJsonApiEntityWithOptionalId {
    const data: IJsonApiEntityWithOptionalId = {
      type: this._entityType,
      attributes: {
        date: parameterChangeAction.date,
        value: parameterChangeAction.value,
        description: parameterChangeAction.description
      },
      relationships: {
        [relation.entityType]: {
          data: {
            type: relation.entityType,
            id: relation.id
          }
        }
      }
    }
    if (parameterChangeAction.contact && parameterChangeAction.contact.id) {
      data.relationships!.contact = {
        data: {
          type: 'contact',
          id: parameterChangeAction.contact.id
        }
      }
    }
    if (parameterChangeAction.id) {
      data.id = parameterChangeAction.id
    }
    return data
  }
}
