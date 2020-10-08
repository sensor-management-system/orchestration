import {
  Attachment
} from '@/models/Attachment'

export default class AttachmentSerializer {
  convertJsonApiElementToModel (attachment: any): Attachment {
    const result = new Attachment()
    result.id = attachment.id
    result.label = attachment.label || ''
    result.url = attachment.url || ''

    return result
  }

  convertNestedJsonApiToModelList (attachments: any[]): Attachment[] {
    return attachments.map(this.convertJsonApiElementToModel)
  }
}
