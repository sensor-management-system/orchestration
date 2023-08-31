/**
 * @license
 * Web client of the Sensor Management System software developed within the
 * Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020-2023
 * - Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
 * - Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
 * - Maximilian Schaldach (UFZ, maximilian.schaldach@ufz.de)
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