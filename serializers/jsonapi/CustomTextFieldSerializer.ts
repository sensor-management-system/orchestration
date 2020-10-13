import { CustomTextField } from '@/models/CustomTextField'
import { IJsonApiNestedElement } from '@/serializers/jsonapi/JsonApiTypes'

export class CustomTextFieldSerializer {
  convertJsonApiElementToModel (customfield: IJsonApiNestedElement): CustomTextField {
    const result = new CustomTextField()
    result.id = customfield.id
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
}
