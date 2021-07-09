import {AxiosInstance} from "axios";
import {
  GenericPlatformActionSerializer,
  IGenericActionSerializer
} from "@/serializers/jsonapi/GenericActionSerializer";
import {GenericAction} from '@/models/GenericAction';
import {Attachment} from "@/models/Attachment";
import {
  GenericPlatformActionAttachmentApi
} from "@/services/sms/GenericActionAttachmentApi";

export class GenericPlatformActionApi {
  private axiosApi: AxiosInstance
  private serializer: IGenericActionSerializer
  private attachmentApi: GenericPlatformActionAttachmentApi

  constructor (axiosInstance: AxiosInstance, attachmentApi: GenericPlatformActionAttachmentApi) {
    this.axiosApi = axiosInstance
    this.serializer = new GenericPlatformActionSerializer()
    this.attachmentApi = attachmentApi
  }

  async findById (id: string): Promise<GenericAction> {
    const response = await this.axiosApi.get(id, {
      params: {
        include: [
          'contact',
          'generic_platform_action_attachments.attachment'
        ].join(',')
      }
    })
    const data = response.data
    return this.serializer.convertJsonApiObjectToModel(data)
  }

  deleteById (id: string): Promise<void> {
    return this.axiosApi.delete<string, void>(id)
  }

  async add (platformId: string, action: GenericAction): Promise<GenericAction> {
    const url = ''
    const data = this.serializer.convertModelToJsonApiData(action, platformId)
    const response = await this.axiosApi.post(url, { data })
    const savedAction = this.serializer.convertJsonApiObjectToModel(response.data)
    // save every attachment as an GenericActionAttachment
    if (savedAction.id) {
      const promises = action.attachments.map((attachment: Attachment) => this.attachmentApi.add(savedAction.id as string, attachment))
      await Promise.all(promises)
    }
    return savedAction
  }

  async update (platformId: string, action: GenericAction): Promise<GenericAction> {
    if (!action.id) {
      throw new Error('no id for the GenericAction')
    }
    // load the stored action to get a list of the generic platform action attachments before the update
    const attRawResponse = await this.axiosApi.get(action.id, {
      params: {
        include: [
          'generic_platform_action_attachments.attachment'
        ].join(',')
      }
    })
    const attResponseData = attRawResponse.data
    const included = attResponseData.included

    // get the relations between attachments and generic platform action attachments
    const linkedAttachments: { [attachmentId: string]: string } = {}
    if (included) {
      const relations = this.serializer.convertJsonApiIncludedActionAttachmentsToIdList(included)
      // convert to object to gain faster access to its members
      relations.forEach((rel) => {
        linkedAttachments[rel.attachmentId] = rel.genericActionAttachmentId
      })
    }

    // update the action
    const data = this.serializer.convertModelToJsonApiData(action, platformId)
    const actionResponse = await this.axiosApi.patch(action.id, { data })

    // find new attachments
    const newAttachments: Attachment[] = []
    action.attachments.forEach((attachment: Attachment) => {
      if (attachment.id && linkedAttachments[attachment.id]) {
        return
      }
      newAttachments.push(attachment)
    })

    // find deleted attachments
    const genericPlatformActionAttachmentsToDelete: string[] = []
    for (const attachmentId in linkedAttachments) {
      if (action.attachments.find((i: Attachment) => i.id === attachmentId)) {
        continue
      }
      genericPlatformActionAttachmentsToDelete.push(linkedAttachments[attachmentId])
    }

    // when there are no new attachments, newPromises is empty, which is okay
    const newPromises = newAttachments.map((attachment: Attachment) => this.attachmentApi.add(action.id as string, attachment))
    // when there are no deleted attachments, deletedPromises is empty, which is okay
    const deletedPromises = genericPlatformActionAttachmentsToDelete.map((id: string) => this.attachmentApi.delete(id))
    await Promise.all([...deletedPromises, ...newPromises])

    return this.serializer.convertJsonApiObjectToModel(actionResponse.data)
  }
}
