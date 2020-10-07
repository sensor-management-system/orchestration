import { CustomTextField } from '@/models/CustomTextField'

export default class CustomTextFieldSerializer {
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
}
