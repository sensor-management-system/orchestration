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
import { TsmdlDatasourceSerializer } from '@/serializers/jsonapi/TsmdlDatasourceSerializer'
import { TsmdlDatasource } from '@/models/TsmdlDatasource'
import { TsmEndpoint } from '@/models/TsmEndpoint'

export class TsmdlDatasourceApi {
  private axiosApi: AxiosInstance
  readonly basePath: string
  private serializer: TsmdlDatasourceSerializer

  constructor (axiosApi: AxiosInstance, basePath: string) {
    this.axiosApi = axiosApi
    this.basePath = basePath
    this.serializer = new TsmdlDatasourceSerializer()
  }

  async findAll (endpoint: TsmEndpoint): Promise<TsmdlDatasource[]> {
    try {
      return await this.axiosApi.get(this.getQueryString(endpoint)).then((rawResponse) => {
        const rawData = rawResponse.data.value
        return this.serializer.convertJsonApiObjectListToModelList(rawData)
      })
    } catch (_e) {
      return []
    }
  }

  async findOneById (endpoint: TsmEndpoint, id: string): Promise<TsmdlDatasource | null> {
    return await this.axiosApi.get(this.getQueryString(endpoint, id)).then((rawResponse) => {
      const rawData = rawResponse.data
      if (!rawData) {
        return null
      }
      return this.serializer.convertJsonApiEntityToModel(rawData)
    })
  }

  private getQueryString (endpoint: TsmEndpoint, id: string | null = null): string {
    const basePath = `${endpoint.url}/Datasources`
    return !id ? basePath : basePath + `(${id})`
  }
}
