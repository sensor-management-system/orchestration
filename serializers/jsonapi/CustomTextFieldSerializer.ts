/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020
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
import { ICustomTextField, CustomTextField } from '@/models/CustomTextField'
import {
  IJsonApiDataWithOptionalIdWithoutRelationships,
  IJsonApiNestedElement,
  IJsonApiObject,
  IJsonApiObjectList,
  IJsonApiTypeId,
  IJsonApiTypeIdAttributes,
  IJsonApiTypeIdDataListDict
} from '@/serializers/jsonapi/JsonApiTypes'

export class CustomTextFieldSerializer {
  convertJsonApiElementToModel (customfield: IJsonApiNestedElement): CustomTextField {
    const result = new CustomTextField()
    result.id = customfield.id.toString()
    result.key = customfield.key || ''
    result.value = customfield.value || ''

    return result
  }

  convertNestedJsonApiToModelList (customfields: IJsonApiNestedElement[]): CustomTextField[] {
    return customfields.map(this.convertJsonApiElementToModel)
  }

  convertModelListToNestedJsonApiArray (customfields: CustomTextField[]): IJsonApiNestedElement[] {
    const result = []
    for (const customField of customfields) {
      const customFieldToSave: IJsonApiNestedElement = {}

      if (customField.id != null) {
        customFieldToSave.id = customField.id
      }

      customFieldToSave.key = customField.key
      customFieldToSave.value = customField.value

      result.push(customFieldToSave)
    }
    return result
  }

  convertJsonApiObjectToModel (jsonApiObject: IJsonApiObject): CustomTextField {
    const data = jsonApiObject.data
    return this.convertJsonApiDataToModel(data)
  }

  convertJsonApiDataToModel (jsonApiData: IJsonApiTypeIdAttributes): CustomTextField {
    const attributes = jsonApiData.attributes

    const newEntry = new CustomTextField()

    newEntry.id = jsonApiData.id.toString()
    newEntry.key = attributes.key || ''
    newEntry.value = attributes.value || ''

    return newEntry
  }

  convertJsonApiObjectListToModelList (jsonApiObjectList: IJsonApiObjectList): CustomTextField[] {
    return jsonApiObjectList.data.map(this.convertJsonApiDataToModel)
  }

  convertModelListToJsonApiRelationshipObject (customFields: ICustomTextField[]): IJsonApiTypeIdDataListDict {
    return {
      customfields: {
        data: this.convertModelListToTupleListWithIdAndType(customFields)
      }
    }
  }

  convertModelToJsonApiData (customField: ICustomTextField): IJsonApiDataWithOptionalIdWithoutRelationships {
    const data: any = {
      type: 'customfield',
      attributes: {
        key: customField.key,
        value: customField.value
      }
    }
    if (customField.id) {
      data.id = customField.id
    }
    return data
  }

  convertModelListToTupleListWithIdAndType (customFields: ICustomTextField[]): IJsonApiTypeId[] {
    const result: IJsonApiTypeId[] = []
    for (const field of customFields) {
      if (field.id !== null) {
        result.push({
          id: field.id,
          type: 'customfield'
        })
      }
    }
    return result
  }
}
