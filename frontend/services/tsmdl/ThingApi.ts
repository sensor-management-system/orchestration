/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2023
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Maximilian Schaldach <maximilian.schaldach@ufz.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */

import { AxiosInstance } from 'axios'
import { TsmdlThingSerializer } from '@/serializers/jsonapi/TsmdlThingSerializer'
import { TsmdlThing } from '@/models/TsmdlThing'
import { TsmdlDatasource } from '@/models/TsmdlDatasource'
import { TsmEndpoint } from '@/models/TsmEndpoint'

export class TsmdlThingApi {
  private axiosApi: AxiosInstance
  readonly basePath: string
  private serializer: TsmdlThingSerializer

  constructor (axiosApi: AxiosInstance, basePath: string) {
    this.axiosApi = axiosApi
    this.basePath = basePath
    this.serializer = new TsmdlThingSerializer()
  }

  async findAllByDatasource (endpoint: TsmEndpoint, datasource: TsmdlDatasource): Promise<TsmdlThing[]> {
    try {
      return await this.axiosApi.get(this.getQueryString(endpoint, datasource)).then((rawResponse) => {
        const rawData = rawResponse.data.value
        return this.serializer.convertJsonApiObjectListToModelList(rawData)
      })
    } catch (_e) {
      return []
    }
  }

  async findOneByDatasourceAndId (endpoint: TsmEndpoint, datasource: TsmdlDatasource, id: string): Promise<TsmdlThing | null> {
    return await this.axiosApi.get(this.getQueryString(endpoint, datasource, id)).then((rawResponse) => {
      const rawData = rawResponse.data
      if (!rawData) {
        return null
      }
      return this.serializer.convertJsonApiEntityToModel(rawData)
    })
  }

  private getQueryString (endpoint: TsmEndpoint, datasource: TsmdlDatasource, id: string | null = null): string {
    const basePath = `${endpoint.url}/Datasources(${datasource.id})/Things`
    return !id ? basePath : basePath + `(${id})`
  }
}
