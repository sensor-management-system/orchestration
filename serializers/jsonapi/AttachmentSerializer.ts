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

  convertModelListToNestedJsonApiArray (attachments: Attachment[]): any[] {
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
