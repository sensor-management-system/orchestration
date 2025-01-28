/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Maximilian Schaldach <maximilian.schaldach@ufz.de>
 * - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */

import { AxiosInstance, AxiosResponse } from 'axios'
import { StaEntitySerializer } from '@/serializers/sta/StaEntitySerializer'
import { StaApiEntity, StaEntity } from '@/models/sta/StaEntity'
import { StaThingSerializer } from '@/serializers/sta/StaThingSerializer'
import { StaDatastreamSerializer } from '@/serializers/sta/StaDatastreamSerializer'
import { getStaQueryStringByQueryParams, STA_QUERY_PARAMS_COLLECTION, StaQueryParams } from '@/utils/staQueryHelper'
import { StaApiThing, StaThing } from '@/models/sta/StaThing'
import { StaApiDatastream, StaDatastream } from '@/models/sta/StaDatastream'

export class GenericStaApi<StaEntityType extends StaEntity, StaApiEntityType extends StaApiEntity> {
  private axiosApi: AxiosInstance
  private serializer: StaEntitySerializer
  private staPath: string

  constructor (axiosApi: AxiosInstance, serializer: StaEntitySerializer, staPath: string) {
    this.axiosApi = axiosApi
    this.serializer = serializer
    this.staPath = staPath
  }

  async findAll (baseUrl: string, params: string | StaQueryParams<StaApiEntityType>): Promise<StaEntityType[]> {
    return await this.axiosApi.get(this.getCollectionQueryString(baseUrl, params)).then((rawResponse: AxiosResponse) => {
      if (!rawResponse.data.value) {
        throw new Error('Invalid STA API response')
      }
      return this.serializer.convertStaApiObjectListToModelList(rawResponse.data.value) as StaEntityType[]
    })
  }

  async findOneById (baseUrl: string, id: string, params: string | StaQueryParams<StaApiEntityType>): Promise<StaEntityType|null> {
    return await this.axiosApi.get(this.getSingleQueryString(baseUrl, id, params)).then((rawResponse: AxiosResponse) => {
      if (!rawResponse.data) {
        throw new Error('Invalid STA API response')
      }
      return this.serializer.convertStaApiObjectToModel(rawResponse.data) as StaEntityType
    }).catch((e) => {
      if (e.response.status === 404) { return null }
      throw e
    })
  }

  private getCollectionQueryString (baseUrl: string, params: string | StaQueryParams<StaApiEntityType>): string {
    return `${baseUrl}/${this.staPath}${this.getParamsString(params)}`
  }

  private getSingleQueryString (baseUrl: string, id: string, params: string | StaQueryParams<StaApiEntityType>): string {
    return `${baseUrl}/${this.staPath}(${id})${this.getParamsString(params)}`
  }

  private getParamsString (params: string | StaQueryParams<StaApiEntityType>): string {
    if (typeof params === 'object') {
      return getStaQueryStringByQueryParams(params)
    }
    return params
  }
}

export class StaThingApi extends GenericStaApi<StaThing, StaApiThing> {
  constructor (axiosApi: AxiosInstance) {
    super(axiosApi, new StaThingSerializer(), 'Things')
  }

  async findeSelfLinkByConfigurationId (baseUrl: string, configurationId: string): Promise<string> {
    const params = STA_QUERY_PARAMS_COLLECTION.findThingStaLinkByConfigurationId(configurationId)
    const matchingThings = await this.findAll(baseUrl, params)

    if (matchingThings?.length === 1 && matchingThings[0].selfLink) {
      return matchingThings[0].selfLink
    }
    return ''
  }
}

export class StaDatastreamApi extends GenericStaApi<StaDatastream, StaApiDatastream> {
  constructor (axiosApi: AxiosInstance) {
    super(axiosApi, new StaDatastreamSerializer(), 'Datastreams')
  }

  async findSelfLinkByLinkingId (baseUrl: string, linkingId: string): Promise<string> {
    const params = STA_QUERY_PARAMS_COLLECTION.findDatastreamStaLinkByTsmLinkingId(linkingId)
    const matchingDatastreams = await this.findAll(baseUrl, params)

    if (matchingDatastreams?.length === 1 && matchingDatastreams[0].selfLink) {
      return matchingDatastreams[0].selfLink
    }

    return ''
  }
}
