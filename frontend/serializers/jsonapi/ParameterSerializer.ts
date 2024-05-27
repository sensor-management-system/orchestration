/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2023 - 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */

import { DateTime } from 'luxon'

import { IParameter, Parameter } from '@/models/Parameter'
import { IContact } from '@/models/Contact'

import {
  IJsonApiEntityListEnvelope,
  IJsonApiEntityEnvelope,
  IJsonApiEntity,
  IJsonApiEntityWithOptionalId,
  IJsonApiEntityWithoutDetails,
  IJsonApiEntityWithOptionalAttributes,
  IJsonApiEntityWithoutDetailsDataDict,
  IJsonApiEntityWithoutDetailsDataDictList,
  IJsonApiTypedEntityWithoutDetailsDataDictList,
  IJsonApiRelationships
} from '@/serializers/jsonapi/JsonApiTypes'

import { ContactSerializer } from '@/serializers/jsonapi/ContactSerializer'

export enum ParameterEntityType {
  DEVICE = 'device_parameter',
  PLATFORM = 'platform_parameter',
  CONFIGURATION = 'configuration_parameter'
}

export enum ParameterRelationEntityType {
  DEVICE = 'device',
  PLATFORM = 'platform',
  CONFIGURATION = 'configuration'
}

export interface IParameterRelation {
  entityType: ParameterRelationEntityType
  id: string
}

export class ParameterSerializer {
  private _contactSerializer: ContactSerializer = new ContactSerializer()
  private _entityType: ParameterEntityType

  constructor (entityType: ParameterEntityType) {
    this._entityType = entityType
  }

  /**
   * converts a JSONAPI response with multiple parameter objects into a list of Parameter instances
   *
   * @param {IJsonApiEntityListEnvelope} jsonApiObjectList - the JSONAPI response object
   * @returns {Parameter[]} a list of Paramter instances
   */
  convertJsonApiObjectListToModelList (jsonApiObjectList: IJsonApiEntityListEnvelope): Parameter[] {
    const included = jsonApiObjectList.included || []
    return jsonApiObjectList.data.map((data: IJsonApiEntity) => {
      return this.convertJsonApiDataToModel(data, included)
    })
  }

  /**
   * converts a JSONAPI response for a single parameter into a Parameter instance
   *
   * @param {IJsonApiEntityEnvelope} jsonApiObject - the JSONAPI response object
   * @returns {Parameter} a Parameter instance
   */
  convertJsonApiObjectToModel (jsonApiObject: IJsonApiEntityEnvelope): Parameter {
    const included = jsonApiObject.included || []
    return this.convertJsonApiDataToModel(jsonApiObject.data, included)
  }

  /**
   * converts a JSONAPI object entity into a Parameter instance
   *
   * @param {IJsonApiEntityWithOptionalAttributes} jsonApiData - the JSONAPI entity
   * @param {IJsonApiEntityWithOptionalAttributes[]} included - a list of included entities
   * @returns {Parameter} a Parameter instance
   */
  convertJsonApiDataToModel (jsonApiData: IJsonApiEntityWithOptionalAttributes, included: IJsonApiEntityWithOptionalAttributes[] = []): Parameter {
    const id = jsonApiData.id.toString()
    const label = jsonApiData.attributes?.label || ''
    const description = jsonApiData.attributes?.description || ''
    const unitUri = jsonApiData.attributes?.unit_uri || ''
    const unitName = jsonApiData.attributes?.unit_name || ''
    const createdAt = jsonApiData.attributes?.created_at != null ? DateTime.fromISO(jsonApiData.attributes.created_at, { zone: 'UTC' }) : null
    const updatedAt = jsonApiData.attributes?.updated_at != null ? DateTime.fromISO(jsonApiData.attributes.updated_at, { zone: 'UTC' }) : null

    const relationships = jsonApiData.relationships || {}

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

    return Parameter.createFromObject({
      id,
      label,
      description,
      unitUri,
      unitName,
      createdAt,
      updatedAt,
      createdBy,
      updatedBy
    })
  }

  convertJsonApiRelationshipsSingleModel (relationships: IJsonApiRelationships, included: IJsonApiEntityWithOptionalAttributes[]): Parameter | null {
    let parameterId: string = ''
    if (relationships[this._entityType]) {
      const parameterObject = relationships[this._entityType] as IJsonApiEntityWithoutDetailsDataDict
      if (parameterObject.data && parameterObject.data.id) {
        parameterId = parameterObject.data.id
      }
    }

    let parameter: Parameter | null = null
    if (included && included.length > 0) {
      for (const includedEntry of included) {
        if (includedEntry.type !== this._entityType) {
          continue
        }
        if (parameterId === includedEntry.id) {
          parameter = this.convertJsonApiDataToModel(includedEntry)
        }
      }
    }
    return parameter
  }

  convertJsonApiRelationshipsModelList (relationships: IJsonApiRelationships, included: IJsonApiEntityWithOptionalAttributes[]): Parameter[] {
    const entityTypePlural = this._entityType + 's'
    const parametersIds = []
    if (relationships[entityTypePlural]) {
      const parameterObject = relationships[entityTypePlural] as IJsonApiEntityWithoutDetailsDataDictList
      if (parameterObject.data && parameterObject.data.length > 0) {
        for (const relationShipParameterData of parameterObject.data) {
          const parametersId = relationShipParameterData.id
          parametersIds.push(parametersId)
        }
      }
    }

    const result: Parameter[] = []
    if (included && included.length > 0) {
      for (const includedEntry of included) {
        if (includedEntry.type === this._entityType) {
          const parameterId = includedEntry.id
          if (parametersIds.includes(parameterId)) {
            const parameter = this.convertJsonApiDataToModel(includedEntry)
            result.push(parameter)
          }
        }
      }
    }

    return result
  }

  convertModelListToJsonApiRelationshipObject (parameters: Parameter[]): IJsonApiTypedEntityWithoutDetailsDataDictList {
    const entityTypePlural = this._entityType + 's'
    return {
      [entityTypePlural]: {
        data: this.convertModelListToTupleListWithIdAndType(parameters)
      }
    }
  }

  convertModelListToTupleListWithIdAndType (parameters: Parameter[]): IJsonApiEntityWithoutDetails[] {
    const result: IJsonApiEntityWithoutDetails[] = []
    for (const parameter of parameters) {
      if (parameter.id !== null) {
        result.push({
          id: parameter.id,
          type: this._entityType
        })
      }
    }
    return result
  }

  convertModelToJsonApiData (parameter: IParameter, relation: IParameterRelation): IJsonApiEntityWithOptionalId {
    const data: IJsonApiEntityWithOptionalId = {
      type: this._entityType,
      attributes: {
        label: parameter.label,
        description: parameter.description,
        unit_uri: parameter.unitUri,
        unit_name: parameter.unitName
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
    if (parameter.id) {
      data.id = parameter.id
    }
    return data
  }
}
