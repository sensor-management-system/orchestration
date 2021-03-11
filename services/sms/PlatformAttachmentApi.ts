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
import { PlatformAttachmentSerializer } from '@/serializers/jsonapi/PlatformAttachmentSerializer'

export class PlatformAttachmentApi {
  private axiosApi: AxiosInstance
  private serializer: PlatformAttachmentSerializer

  constructor (axiosInstance: AxiosInstance) {
    this.axiosApi = axiosInstance
    this.serializer = new PlatformAttachmentSerializer()
  }

  findById (id: string): Promise<Attachment> {
    return this.axiosApi.get(id).then((rawRespmse) => {
      const rawData = rawRespmse.data
      return this.serializer.convertJsonApiObjectToModel(rawData)
    })
  }

  deleteById (id: string): Promise<void> {
    return this.axiosApi.delete<string, void>(id)
  }

  add (platformId: string, attachment: Attachment) {
    const url = ''
    const data = this.serializer.convertModelToJsonApiData(attachment, platformId)
    return this.axiosApi.post(url, { data })
  }

  update (platformId: string, attachment: Attachment) {
    return new Promise<string>((resolve, reject) => {
      if (attachment.id) {
        resolve(attachment.id)
      } else {
        reject(new Error('no id for the Attachment'))
      }
    }).then((attachmentId) => {
      const data = this.serializer.convertModelToJsonApiData(attachment, platformId)
      return this.axiosApi.patch(attachmentId, { data })
    })
  }
}
