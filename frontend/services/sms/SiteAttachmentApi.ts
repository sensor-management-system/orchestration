/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2023 - 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
import { AxiosInstance } from 'axios'

import { Attachment } from '@/models/Attachment'
import { SiteAttachmentSerializer } from '@/serializers/jsonapi/SiteAttachmentSerializer'

export class SiteAttachmentApi {
  private axiosApi: AxiosInstance
  readonly basePath: string
  private serializer: SiteAttachmentSerializer

  constructor (axiosInstance: AxiosInstance, basePath: string) {
    this.axiosApi = axiosInstance
    this.basePath = basePath
    this.serializer = new SiteAttachmentSerializer()
  }

  findById (id: string): Promise<Attachment> {
    return this.axiosApi.get(this.basePath + '/' + id).then((rawRespmse) => {
      const rawData = rawRespmse.data
      return this.serializer.convertJsonApiObjectToModel(rawData)
    })
  }

  deleteById (id: string): Promise<void> {
    return this.axiosApi.delete<string, void>(this.basePath + '/' + id)
  }

  add (siteId: string, attachment: Attachment): Promise<Attachment> {
    const url = this.basePath
    const data = this.serializer.convertModelToJsonApiData(attachment, siteId)
    return this.axiosApi.post(url, { data }).then((serverResponse) => {
      return this.serializer.convertJsonApiObjectToModel(serverResponse.data)
    })
  }

  update (siteId: string, attachment: Attachment): Promise<Attachment> {
    return new Promise<string>((resolve, reject) => {
      if (attachment.id) {
        resolve(attachment.id)
      } else {
        reject(new Error('no id for the Attachment'))
      }
    }).then((attachmentId) => {
      const data = this.serializer.convertModelToJsonApiData(attachment, siteId)
      return this.axiosApi.patch(this.basePath + '/' + attachmentId, { data }).then((serverResponse) => {
        return this.serializer.convertJsonApiObjectToModel(serverResponse.data)
      })
    })
  }

  async getFile (url: string): Promise<Blob> {
    const response = await this.axiosApi.get(url,
      { responseType: 'blob' }
    )
    const contentType = response.headers['content-type']
    return new Blob([response.data], { type: contentType })
  }
}
