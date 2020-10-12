import { CustomTextField } from '@/models/CustomTextField'

export class CustomTextFieldSerializer {
  convertJsonApiElementToModel (customfield: any): CustomTextField {
    const result = new CustomTextField()
    result.id = customfield.id
    result.key = customfield.key || ''
    result.value = customfield.value || ''

    return result
  }

  convertNestedJsonApiToModelList (customfields: any[]): CustomTextField[] {
    return customfields.map(this.convertJsonApiElementToModel)
  }

  convertModelListToNestedJsonApiArray (customfields: CustomTextField[]): any[] {
    const result = []
    for (const customField of customfields) {
      const customFieldToSave: any = {}

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
