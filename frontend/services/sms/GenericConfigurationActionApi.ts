/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020 - 2022
 * - Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
 * - Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
 * - Tim Eder (UFZ, tim.eder@ufz.de)
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
import { AxiosInstance } from 'axios'

import { Attachment } from '@/models/Attachment'
import { GenericAction } from '@/models/GenericAction'
import { GenericConfigurationActionAttachmentApi } from '@/services/sms/GenericActionAttachmentApi'
import { IGenericActionSerializer, GenericConfigurationActionSerializer } from '@/serializers/jsonapi/GenericActionSerializer'

export class GenericConfigurationActionApi {
  private axiosApi: AxiosInstance
  readonly basePath: string
  private serializer: IGenericActionSerializer
  private attachmentApi: GenericConfigurationActionAttachmentApi

  constructor (axiosInstance: AxiosInstance, basePath: string, attachmentApi: GenericConfigurationActionAttachmentApi) {
    this.axiosApi = axiosInstance
    this.basePath = basePath
    this.serializer = new GenericConfigurationActionSerializer()
    this.attachmentApi = attachmentApi
  }

  async findById (id: string): Promise<GenericAction> {
    const response = await this.axiosApi.get(this.basePath + '/' + id, {
      params: {
        include: [
          'contact',
          'generic_configuration_action_attachments.attachment'
        ].join(',')
      }
    })
    const data = response.data
    return this.serializer.convertJsonApiObjectToModel(data)
  }

  async deleteById (id: string): Promise<void> {
    return await this.axiosApi.delete<string, void>(this.basePath + '/' + id)
  }

  async add (configurationId: string, action: GenericAction): Promise<GenericAction> {
    const url = this.basePath
    const data = this.serializer.convertModelToJsonApiData(action, configurationId)
    const response = await this.axiosApi.post(url, { data })
    const savedAction = this.serializer.convertJsonApiObjectToModel(response.data)
    // save every attachment as an GenericActionAttachment
    if (savedAction.id) {
      const promises = action.attachments.map((attachment: Attachment) => this.attachmentApi.add(savedAction.id as string, attachment))
      await Promise.all(promises)
    }
    return savedAction
  }

  async update (configurationId: string, action: GenericAction): Promise<GenericAction> {
    if (!action.id) {
      throw new Error('no id for the GenericAction')
    }
    // load the stored action to get a list of the generic configuration action attachments before the update
    const attRawResponse = await this.axiosApi.get(this.basePath + '/' + action.id, {
      params: {
        include: [
          'generic_configuration_action_attachments.attachment'
        ].join(',')
      }
    })
    const attResponseData = attRawResponse.data
    const included = attResponseData.included

    // get the relations between attachments and generic configuration action attachments
    const linkedAttachments: { [attachmentId: string]: string } = {}
    if (included) {
      const relations = this.serializer.convertJsonApiIncludedActionAttachmentsToIdList(included)
      // convert to object to gain faster access to its members
      relations.forEach((rel) => {
        linkedAttachments[rel.attachmentId] = rel.genericActionAttachmentId
      })
    }

    // update the action
    const data = this.serializer.convertModelToJsonApiData(action, configurationId)
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
    const genericConfigurationActionAttachmentsToDelete: string[] = []
    for (const attachmentId in linkedAttachments) {
      if (action.attachments.find((i: Attachment) => i.id === attachmentId)) {
        continue
      }
      genericConfigurationActionAttachmentsToDelete.push(linkedAttachments[attachmentId])
    }

    // when there are no new attachments, newPromises is empty, which is okay
    const newPromises = newAttachments.map((attachment: Attachment) => this.attachmentApi.add(action.id as string, attachment))
    // when there are no deleted attachments, deletedPromises is empty, which is okay
    const deletedPromises = genericConfigurationActionAttachmentsToDelete.map((id: string) => this.attachmentApi.delete(id))
    await Promise.all([...deletedPromises, ...newPromises])

    return this.serializer.convertJsonApiObjectToModel(actionResponse.data)
  }
}
