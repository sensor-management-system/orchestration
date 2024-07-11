/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Tobias Kuhnert <tobias.kuhnert@ufz.de>
 * - Maximilian Schaldach <maximilian.schaldach@ufz.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */

import { AxiosInstance } from 'axios'
import { TsmLinkingSerializer } from '@/serializers/jsonapi/TsmLinkingSerializer'
import { TsmLinking } from '@/models/TsmLinking'

export class TsmLinkingApi {
  private axiosApi: AxiosInstance
  readonly basePath: string
  private serializer: TsmLinkingSerializer

  constructor (axiosApi: AxiosInstance, basePath: string) {
    this.axiosApi = axiosApi
    this.basePath = basePath
    this.serializer = new TsmLinkingSerializer()
  }

  getRelatedTsmLinkings (configurationId: string): Promise<TsmLinking[]> {
    const url = '/configurations/' + configurationId + '/datastream-links'
    const params = {
      'page[size]': 10000,
      include: [
        'device_mount_action',
        'device_mount_action.device',
        'device_property',
        'tsm_endpoint'
      ].join(',')
    }
    return this.axiosApi.get(url, { params }).then((rawResponse) => {
      const rawData = rawResponse.data
      return this.serializer.convertJsonApiObjectListToModelList(rawData)
    })
  }

  findById (id: string): Promise<TsmLinking> {
    const url = this.basePath + '/' + id

    const params = {
      include: [
        'device_mount_action',
        'device_mount_action.device',
        'device_property',
        'tsm_endpoint'
      ].join(',')
    }

    return this.axiosApi.get(url, { params }).then((rawServerResponse) => {
      return this.serializer.convertJsonApiObjectToModel(rawServerResponse.data)
    })
  }

  deleteById (id: string): Promise<void> {
    return this.axiosApi.delete<string, void>(this.basePath + '/' + id)
  }

  async add (tsmLinking: TsmLinking): Promise<string> {
    const url = this.basePath
    const data = this.serializer.convertModelToJsonApiData(tsmLinking)
    const response = await this.axiosApi.post(url, { data })
    return response.data.data.id
  }

  async update (tsmLinking: TsmLinking): Promise<string> {
    if (!tsmLinking.id) {
      throw new Error('no id for the TsmLinking')
    }
    const url = this.basePath + '/' + tsmLinking.id
    const data = this.serializer.convertModelToJsonApiData(tsmLinking)
    const response = await this.axiosApi.patch(url, { data })
    return response.data.data.id
  }

  async delete (tsmLinking: TsmLinking): Promise<void> {
    if (!tsmLinking.id) {
      throw new Error('no id for the TsmLinking')
    }
    const url = this.basePath + '/' + tsmLinking.id
    return await this.axiosApi.delete<string, void>(url)
  }
}
