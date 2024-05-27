/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */

import { AxiosInstance, Method } from 'axios'
import { ExportControl } from '@/models/ExportControl'
import { ExportControlSerializer } from '@/serializers/jsonapi/ExportControlSerializer'

export class ExportControlApi {
  private axiosApi: AxiosInstance
  private readonly basePath: string
  private serializer: ExportControlSerializer

  constructor (axiosInstance: AxiosInstance, basePath: string) {
    this.axiosApi = axiosInstance
    this.basePath = basePath
    this.serializer = new ExportControlSerializer()
  }

  async save (exportControl: ExportControl): Promise<ExportControl> {
    let method: Method = 'patch'
    let url = this.basePath
    if (!exportControl.id) {
      method = 'post'
    } else {
      url += '/' + String(exportControl.id)
    }

    const serverAnswer = await this.axiosApi.request({
      url,
      method,
      data: {
        data: this.serializer.convertModelToJsonApiData(exportControl)
      }
    })
    const answerData = serverAnswer.data
    return this.serializer.convertJsonApiObjectToModel(answerData)
  }

  deleteById (id: string): Promise<void> {
    return this.axiosApi.delete<string, void>(this.basePath + '/' + id)
  }
}
