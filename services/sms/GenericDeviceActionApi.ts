/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2021
 * - Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
 * - Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
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
import { GenericDeviceAction } from '@/models/GenericDeviceAction'
import { GenericDeviceActionAttachmentApi } from '@/services/sms/GenericDeviceActionAttachmentApi'
import { GenericDeviceActionSerializer } from '@/serializers/jsonapi/GenericDeviceActionSerializer'

export class GenericDeviceActionApi {
  private axiosApi: AxiosInstance
  private serializer: GenericDeviceActionSerializer
  private attachmentApi: GenericDeviceActionAttachmentApi

  constructor (axiosInstance: AxiosInstance, attachmentApi: GenericDeviceActionAttachmentApi) {
    this.axiosApi = axiosInstance
    this.serializer = new GenericDeviceActionSerializer()
    this.attachmentApi = attachmentApi
  }

  async findById (id: string): Promise<GenericDeviceAction> {
    const response = await this.axiosApi.get(id, {
      params: {
        include: [
          'contact',
          'generic_device_action_attachments.device_attachment'
        ].join(',')
      }
    })
    const data = response.data
    return this.serializer.convertJsonApiObjectToModel(data)
  }

  deleteById (id: string): Promise<void> {
    return this.axiosApi.delete<string, void>(id)
  }

  async add (deviceId: string, action: GenericDeviceAction): Promise<GenericDeviceAction> {
    const url = ''
    const data = this.serializer.convertModelToJsonApiData(action, deviceId)
    const response = await this.axiosApi.post(url, { data })
    const savedAction = this.serializer.convertJsonApiObjectToModel(response.data)
    // save every attachment as an GenericDeviceActionAttachment
    if (savedAction.id) {
      const promises = action.attachments.map((attachment: Attachment) => this.attachmentApi.add(savedAction.id as string, attachment))
      await Promise.all(promises)
    }
    return savedAction
  }

  async update (deviceId: string, action: GenericDeviceAction): Promise<GenericDeviceAction> {
    if (!action.id) {
      throw new Error('no id for the GenericDeviceAction')
    }
    // load the stored action to get a list of the attachments before the update
    await this.findRelatedGenericDeviceActionAttachments(action.id)

    const data = this.serializer.convertModelToJsonApiData(action, deviceId)
    const response = await this.axiosApi.patch(action.id, { data })
    return this.serializer.convertJsonApiObjectToModel(response.data)
  }

  findRelatedGenericDeviceActionAttachments (actionId: string): Promise<GenericDeviceAction[]> {
    const url = actionId + '/generic-device-action-attachments'
    const params = {
      'page[size]': 10000,
      include: 'attachment'
    }
    return this.axiosApi.get(url, { params }).then((rawServerResponse) => {
      console.log(rawServerResponse)
      //return new GenericDeviceActionSerializer().convertJsonApiObjectListToModelList(rawServerResponse.data)
    })
  }
}
