/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2021 - 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
import { AxiosInstance } from 'axios'

import { Attachment } from '@/models/Attachment'
import { SoftwareUpdateAction } from '@/models/SoftwareUpdateAction'
import { DeviceSoftwareUpdateActionAttachmentApi } from '@/services/sms/SoftwareUpdateActionAttachmentApi'
import { ISoftwareUpdateActionSerializer, DeviceSoftwareUpdateActionSerializer } from '@/serializers/jsonapi/SoftwareUpdateActionSerializer'

export class DeviceSoftwareUpdateActionApi {
  private axiosApi: AxiosInstance
  readonly basePath: string
  private serializer: ISoftwareUpdateActionSerializer
  private attachmentApi: DeviceSoftwareUpdateActionAttachmentApi

  constructor (axiosInstance: AxiosInstance, basePath: string, attachmentApi: DeviceSoftwareUpdateActionAttachmentApi) {
    this.axiosApi = axiosInstance
    this.basePath = basePath
    this.serializer = new DeviceSoftwareUpdateActionSerializer()
    this.attachmentApi = attachmentApi
  }

  async findById (id: string): Promise<SoftwareUpdateAction> {
    const response = await this.axiosApi.get(this.basePath + '/' + id, {
      params: {
        include: [
          'contact',
          'device_software_update_action_attachments.attachment'
        ].join(',')
      }
    })
    const data = response.data
    return this.serializer.convertJsonApiObjectToModel(data)
  }

  deleteById (id: string): Promise<void> {
    return this.axiosApi.delete<string, void>(this.basePath + '/' + id)
  }

  async add (deviceId: string, action: SoftwareUpdateAction): Promise<SoftwareUpdateAction> {
    const url = this.basePath
    const data = this.serializer.convertModelToJsonApiData(action, deviceId)
    const response = await this.axiosApi.post(url, { data })
    const savedAction = this.serializer.convertJsonApiObjectToModel(response.data)
    // save every attachment as an ActionAttachment
    if (savedAction.id) {
      const promises = action.attachments.map((attachment: Attachment) => this.attachmentApi.add(savedAction.id as string, attachment))
      await Promise.all(promises)
    }
    return savedAction
  }

  async update (deviceId: string, action: SoftwareUpdateAction): Promise<SoftwareUpdateAction> {
    if (!action.id) {
      throw new Error('no id for the SoftwareUpdateAction')
    }
    // load the stored action to get a list of the device action attachments before the update
    const attRawResponse = await this.axiosApi.get(this.basePath + '/' + action.id, {
      params: {
        include: [
          'device_software_update_action_attachments.attachment'
        ].join(',')
      }
    })
    const attResponseData = attRawResponse.data
    const included = attResponseData.included

    // get the relations between attachments and device action attachments
    const linkedAttachments: { [attachmentId: string]: string } = {}
    if (included) {
      const relations = this.serializer.convertJsonApiIncludedActionAttachmentsToIdList(included)
      // convert to object to gain faster access to its members
      relations.forEach((rel) => {
        linkedAttachments[rel.attachmentId] = rel.softwareUpdateActionAttachmentId
      })
    }

    // update the action
    const data = this.serializer.convertModelToJsonApiData(action, deviceId)
    const actionResponse = await this.axiosApi.patch(this.basePath + '/' + action.id, { data })

    // find new attachments
    const newAttachments: Attachment[] = []
    action.attachments.forEach((attachment: Attachment) => {
      if (attachment.id && linkedAttachments[attachment.id]) {
        return
      }
      newAttachments.push(attachment)
    })

    // find deleted attachments
    const deviceActionAttachmentsToDelete: string[] = []
    for (const attachmentId in linkedAttachments) {
      if (action.attachments.find((i: Attachment) => i.id === attachmentId)) {
        continue
      }
      deviceActionAttachmentsToDelete.push(linkedAttachments[attachmentId])
    }

    // when there are no new attachments, newPromises is empty, which is okay
    const newPromises = newAttachments.map((attachment: Attachment) => this.attachmentApi.add(action.id as string, attachment))
    // when there are no deleted attachments, deletedPromises is empty, which is okay
    const deletedPromises = deviceActionAttachmentsToDelete.map((id: string) => this.attachmentApi.delete(id))
    await Promise.all([...deletedPromises, ...newPromises])

    return this.serializer.convertJsonApiObjectToModel(actionResponse.data)
  }
}
