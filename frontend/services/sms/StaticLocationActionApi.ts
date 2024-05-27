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

import { StaticLocationAction } from '@/models/StaticLocationAction'
import { StaticLocationActionSerializer } from '@/serializers/jsonapi/StaticLocationActionSerializer'

export class StaticLocationActionApi {
  private axiosApi: AxiosInstance
  readonly basePath: string
  private serializer: StaticLocationActionSerializer

  constructor (axiosApi: AxiosInstance, basePath: string) {
    this.axiosApi = axiosApi
    this.basePath = basePath
    this.serializer = new StaticLocationActionSerializer()
  }

  findById (id: string): Promise<StaticLocationAction> {
    const url = this.basePath + '/' + id
    const params = {
      include: [
        'begin_contact',
        'end_contact'
      ].join(',')
    }

    return this.axiosApi.get(url, { params }).then((rawServerResponse) => {
      return this.serializer.convertJsonApiObjectToModel(rawServerResponse.data)
    })
  }

  deleteById (id: string): Promise<void> {
    return this.axiosApi.delete<string, void>(this.basePath + '/' + id)
  }

  async add (configurationId: string, action: StaticLocationAction): Promise<string> {
    const url = this.basePath
    const data = this.serializer.convertModelToJsonApiData(configurationId, action)
    const response = await this.axiosApi.post(url, { data })
    return response.data.data.id
  }

  async update (configurationId: string, action: StaticLocationAction): Promise<string> {
    if (!action.id) {
      throw new Error('no id for the StaticLocationAction')
    }
    const url = this.basePath + '/' + action.id
    const data = this.serializer.convertModelToJsonApiData(configurationId, action)
    const response = await this.axiosApi.patch(url, { data })
    return response.data.data.id
  }

  getRelatedActions (configurationId: string): Promise<StaticLocationAction[]> {
    const url = '/configurations/' + configurationId + '/static-location-actions'
    const params = {
      'page[size]': 10000,
      include: [
        'begin_contact',
        'end_contact'
      ].join(',')
    }
    return this.axiosApi.get(url, { params }).then((rawResponse) => {
      const rawData = rawResponse.data
      return this.serializer.convertJsonApiObjectListToModelList(rawData)
    })
  }

  getRelatedActionsForSite (siteId: string): Promise<StaticLocationAction[]> {
    const url = '/sites/' + siteId + '/static-location-actions'
    const params = {
      'page[size]': 10000,
      include: [
        'begin_contact',
        'end_contact'
      ].join(',')
    }
    return this.axiosApi.get(url, { params }).then((rawResponse) => {
      const rawData = rawResponse.data
      return this.serializer.convertJsonApiObjectListToModelList(rawData)
    })
  }
}
