/**
 * @license
 * Web client of the Sensor Management System software developed within the
 * Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020, 2021
 * - Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
 * - Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
 * - Tobias Kuhnert (UFZ, tobias.kuhnert@ufz.de)
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
