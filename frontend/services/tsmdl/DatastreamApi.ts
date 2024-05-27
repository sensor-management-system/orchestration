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
import { TsmdlDatastreamSerializer } from '@/serializers/jsonapi/TsmdlDatastreamSerializer'
import { TsmdlDatastream } from '@/models/TsmdlDatastream'
import { TsmdlThing } from '@/models/TsmdlThing'
import { TsmdlDatasource } from '@/models/TsmdlDatasource'
import { TsmEndpoint } from '@/models/TsmEndpoint'

export class TsmdlDatastreamApi {
  private axiosApi: AxiosInstance
  readonly basePath: string
  private serializer: TsmdlDatastreamSerializer

  constructor (axiosApi: AxiosInstance, basePath: string) {
    this.axiosApi = axiosApi
    this.basePath = basePath
    this.serializer = new TsmdlDatastreamSerializer()
  }

  async findAllByDatasourceAndThing (endpoint: TsmEndpoint, datasource: TsmdlDatasource, thing: TsmdlThing): Promise<TsmdlDatastream[]> {
    try {
      return await this.axiosApi.get(this.getQueryString(endpoint, datasource, thing)).then((rawResponse) => {
        const rawData = rawResponse.data.value
        return this.serializer.convertJsonApiObjectListToModelList(rawData)
      })
    } catch (_e) {
      return []
    }
  }

  async findOneByDatasourceAndThingAndId (endpoint: TsmEndpoint, datasource: TsmdlDatasource, thing: TsmdlThing, id: string): Promise<TsmdlDatastream | null> {
    return await this.axiosApi.get(this.getQueryString(endpoint, datasource, thing, id)).then((rawResponse) => {
      const rawData = rawResponse.data
      if (!rawData) {
        return null
      }
      return this.serializer.convertJsonApiEntityToModel(rawData)
    })
  }

  private getQueryString (endpoint: TsmEndpoint, datasource: TsmdlDatasource, thing: TsmdlThing, id: string | null = null): string {
    const basePath = `${endpoint.url}/Datasources(${datasource.id})/Things(${thing.id})/Datastreams`
    return !id ? basePath : basePath + `(${id})`
  }
}
