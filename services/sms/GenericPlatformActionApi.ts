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
}
