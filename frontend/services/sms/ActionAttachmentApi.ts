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
import { IActionAttachmentSerializer } from '@/serializers/jsonapi/ActionAttachmentSerializer'

export interface IActionAttachmentApi {
  serializer: IActionAttachmentSerializer
  add (actionId: string, attachment: Attachment): Promise<any>
  delete (id: string): Promise<void>
}

export abstract class AbstractActionAttachmentApi implements IActionAttachmentApi {
  private axiosApi: AxiosInstance
  readonly basePath: string

  abstract get serializer (): IActionAttachmentSerializer

  constructor (axiosInstance: AxiosInstance, basePath: string) {
    this.axiosApi = axiosInstance
    this.basePath = basePath
  }

  async add (actionId: string, attachment: Attachment): Promise<any> {
    const data = this.serializer.convertModelToJsonApiData(attachment, actionId)
    await this.axiosApi.post(this.basePath, { data })
  }

  async delete (id: string): Promise<void> {
    return await this.axiosApi.delete<string, void>(this.basePath + '/' + id)
  }
}
