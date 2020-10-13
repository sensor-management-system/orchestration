import {
  Attachment
} from '@/models/Attachment'

import { IJsonApiNestedElement } from '@/serializers/jsonapi/JsonApiTypes'

export class AttachmentSerializer {
  convertJsonApiElementToModel (attachment: IJsonApiNestedElement): Attachment {
    const result = new Attachment()
    result.id = attachment.id
    result.label = attachment.label || ''
    result.url = attachment.url || ''

    return result
  }

  convertNestedJsonApiToModelList (attachments: IJsonApiNestedElement[]): Attachment[] {
    return attachments.map(this.convertJsonApiElementToModel)
  }

  convertModelListToNestedJsonApiArray (attachments: Attachment[]): IJsonApiNestedElement[] {
    const result = []
    for (const attachment of attachments) {
      const attachmentToSave: any = {}
      if (attachment.id != null) {
        attachmentToSave.id = attachment.id
      }
      attachmentToSave.label = attachment.label
      attachmentToSave.url = attachment.url

      result.push(attachmentToSave)
    }

    return result
  }
}
