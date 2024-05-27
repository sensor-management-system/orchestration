/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Tobias Kuhnert <tobias.kuhnert@ufz.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */

import { AxiosInstance } from 'axios'

import { DynamicLocationAction } from '@/models/DynamicLocationAction'
import { DynamicLocationActionSerializer } from '@/serializers/jsonapi/DynamicLocationActionSerializer'

export class DynamicLocationActionApi {
  private axiosApi: AxiosInstance
  readonly basePath: string
  private serializer: DynamicLocationActionSerializer

  constructor (axiosApi: AxiosInstance, basePath: string) {
    this.axiosApi = axiosApi
    this.basePath = basePath
    this.serializer = new DynamicLocationActionSerializer()
  }

  findById (id: string): Promise<DynamicLocationAction> {
    const url = this.basePath + '/' + id

    const params = {
      include: [
        'begin_contact',
        'end_contact',
        'x_property',
        'y_property',
        'z_property'
      ].join(',')
    }

    return this.axiosApi.get(url, { params }).then((rawServerResponse) => {
      return this.serializer.convertJsonApiObjectToModel(rawServerResponse.data)
    })
  }

  deleteById (id: string): Promise<void> {
    return this.axiosApi.delete<string, void>(this.basePath + '/' + id)
  }

  async add (configurationId: string, action: DynamicLocationAction): Promise<string> {
    const url = this.basePath
    const data = this.serializer.convertModelToJsonApiData(configurationId, action)
    const response = await this.axiosApi.post(url, { data })
    return response.data.data.id
  }

  async update (configurationId: string, action: DynamicLocationAction): Promise<string> {
    if (!action.id) {
      throw new Error('no id for the DynamicLocationAction')
    }
    const url = this.basePath + '/' + action.id
    const data = this.serializer.convertModelToJsonApiData(configurationId, action)
    const response = await this.axiosApi.patch(url, { data })
    // we can't return a full entity here, as we need to included data about the contacts & the device
    // so we just return the id, and let the client load the full element with the included data
    // once it is necessary
    return response.data.data.id
  }

  getRelatedActions (configurationId: string): Promise<DynamicLocationAction[]> {
    const url = '/configurations/' + configurationId + '/dynamic-location-actions'
    const params = {
      'page[size]': 10000,
      include: [
        'begin_contact',
        'end_contact',
        'x_property',
        'y_property',
        'z_property'
      ].join(',')
    }
    return this.axiosApi.get(url, { params }).then((rawResponse) => {
      const rawData = rawResponse.data
      return this.serializer.convertJsonApiObjectListToModelList(rawData)
    })
  }
}
