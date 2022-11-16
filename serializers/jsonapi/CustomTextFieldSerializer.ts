/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020 - 2022
 * - Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
 * - Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
 * - Tim Eder (UFZ, tim.eder@ufz.de)
 * - Tobias Kuhnert (UFZ, tobias.kuhnert@ufz.de)
 * - Helmholtz Centre for Environmental Research GmbH - UFZ
 * (UFZ, https://www.ufz.de)
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
import { CustomTextField, ICustomTextField } from '@/models/CustomTextField'
import {
  IJsonApiEntityWithoutDetails,
  IJsonApiEntityWithOptionalId,
  IJsonApiEntityListEnvelope,
  IJsonApiEntityEnvelope,
  IJsonApiRelationships,
  IJsonApiTypedEntityWithoutDetailsDataDictList,
  IJsonApiEntityWithoutDetailsDataDictList,
  IJsonApiAttributes,
  IJsonApiEntityWithOptionalAttributes
} from '@/serializers/jsonapi/JsonApiTypes'

export interface IMissingCustomTextFieldData {
  ids: string[]
}

export interface ICustomTextFieldsAndMissing {
  customFields: CustomTextField[]
  missing: IMissingCustomTextFieldData
}

export enum CustomTextFieldEntityType {
  DEVICE = 'customfield',
  CONFIGURATION = 'configuration_customfield'
}

export enum CustomTextFieldRelationEntityType {
  DEVICE = 'device',
  CONFIGURATION = 'configuration'
}

export interface ICustomTextFieldRelation {
  entityType: CustomTextFieldRelationEntityType
  id: string
}

export class CustomTextFieldSerializer {
  private entityType: CustomTextFieldEntityType

  constructor (entityType: CustomTextFieldEntityType = CustomTextFieldEntityType.DEVICE) {
    this.entityType = entityType
  }

  convertJsonApiElementToModel (customfield: IJsonApiAttributes): CustomTextField {
    const result = new CustomTextField()
    result.id = customfield.id.toString()
    result.key = customfield.key || ''
    result.value = customfield.value || ''

    return result
  }

  convertNestedJsonApiToModelList (customfields: IJsonApiAttributes[]): CustomTextField[] {
    return customfields.map(this.convertJsonApiElementToModel)
  }

  convertModelListToNestedJsonApiArray (customfields: CustomTextField[]): IJsonApiAttributes[] {
    const result = []
    for (const customField of customfields) {
      const customFieldToSave: IJsonApiAttributes = {}

      if (customField.id != null) {
        customFieldToSave.id = customField.id
      }

      customFieldToSave.key = customField.key
      customFieldToSave.value = customField.value

      result.push(customFieldToSave)
    }
    return result
  }

  convertJsonApiObjectToModel (jsonApiObject: IJsonApiEntityEnvelope): CustomTextField {
    const data = jsonApiObject.data
    return this.convertJsonApiDataToModel(data)
  }

  convertJsonApiDataToModel (jsonApiData: IJsonApiEntityWithOptionalAttributes): CustomTextField {
    const attributes = jsonApiData.attributes

    const newEntry = new CustomTextField()

    newEntry.id = jsonApiData.id.toString()

    if (attributes) {
      newEntry.key = attributes.key || ''
      newEntry.value = attributes.value || ''
    }

    return newEntry
  }

  convertJsonApiObjectListToModelList (jsonApiObjectList: IJsonApiEntityListEnvelope): CustomTextField[] {
    return jsonApiObjectList.data.map(this.convertJsonApiDataToModel)
  }

  convertJsonApiRelationshipsModelList (relationships: IJsonApiRelationships, included: IJsonApiEntityWithOptionalAttributes[]): ICustomTextFieldsAndMissing {
    const customFieldsIds = []
    if (relationships.customfields) {
      const customFieldObject = relationships.customfields as IJsonApiEntityWithoutDetailsDataDictList
      if (customFieldObject.data && customFieldObject.data.length > 0) {
        for (const relationShipCustomFieldData of customFieldObject.data) {
          const customFieldsId = relationShipCustomFieldData.id
          customFieldsIds.push(customFieldsId)
        }
      }
    }

    const possibleCustomFields: {[key: string]: CustomTextField} = {}
    if (included && included.length > 0) {
      for (const includedEntry of included) {
        if (includedEntry.type === this.entityType) {
          const customFieldId = includedEntry.id
          if (customFieldsIds.includes(customFieldId)) {
            const customTextField = this.convertJsonApiDataToModel(includedEntry)
            possibleCustomFields[customFieldId] = customTextField
          }
        }
      }
    }

    const customFields = []
    const missingDataForCustomFieldIds = []

    for (const customFieldId of customFieldsIds) {
      if (possibleCustomFields[customFieldId]) {
        customFields.push(possibleCustomFields[customFieldId])
      } else {
        missingDataForCustomFieldIds.push(customFieldId)
      }
    }

    return {
      customFields,
      missing: {
        ids: missingDataForCustomFieldIds
      }
    }
  }

  convertModelListToJsonApiRelationshipObject (customFields: CustomTextField[]): IJsonApiTypedEntityWithoutDetailsDataDictList {
    return {
      customfields: {
        data: this.convertModelListToTupleListWithIdAndType(customFields)
      }
    }
  }

  convertModelListToTupleListWithIdAndType (customfields: CustomTextField[]): IJsonApiEntityWithoutDetails[] {
    const result: IJsonApiEntityWithoutDetails[] = []
    for (const customfield of customfields) {
      if (customfield.id !== null) {
        result.push({
          id: customfield.id,
          type: this.entityType
        })
      }
    }
    return result
  }

  convertModelToJsonApiData (customField: ICustomTextField, relation: ICustomTextFieldRelation): IJsonApiEntityWithOptionalId {
    const data: IJsonApiEntityWithOptionalId = {
      type: this.entityType,
      attributes: {
        key: customField.key,
        value: customField.value
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
    if (customField.id) {
      data.id = customField.id
    }
    return data
  }
}
