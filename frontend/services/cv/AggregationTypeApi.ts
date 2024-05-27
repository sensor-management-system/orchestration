/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2022 - 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
import { AxiosInstance } from 'axios'

import { AggregationType } from '@/models/AggregationType'
import { AggregationTypeSerializer } from '@/serializers/jsonapi/AggregationTypeSerializer'
import { CVApi } from '@/services/cv/CVApi'

export class AggregationTypeApi extends CVApi<AggregationType> {
  private serializer: AggregationTypeSerializer
  readonly basePath: string

  constructor (axiosInstance: AxiosInstance, basePath: string) {
    super(axiosInstance)
    this.basePath = basePath
    this.serializer = new AggregationTypeSerializer()
  }

  newSearchBuilder (): AggregationTypeSearchBuilder {
    return new AggregationTypeSearchBuilder(this.axiosApi, this.basePath, this.serializer)
  }

  findAll (): Promise<AggregationType[]> {
    return this.newSearchBuilder().build().findMatchingAsList()
  }

  add (aggregationType: AggregationType): Promise<AggregationType> {
    const data = this.serializer.convertModelToJsonApiData(aggregationType)

    return this.axiosApi.post(
      this.basePath,
      {
        data
      },
      {
        headers: {
          'Content-Type': 'application/vnd.api+json'
        }
      }
    ).then((rawResponse) => {
      const response = rawResponse.data
      return this.serializer.convertJsonApiDataToModel(response.data)
    })
  }
}

export class AggregationTypeSearchBuilder {
  private axiosApi: AxiosInstance
  readonly basePath: string
  private serializer: AggregationTypeSerializer

  constructor (axiosApi: AxiosInstance, basePath: string, serializer: AggregationTypeSerializer) {
    this.axiosApi = axiosApi
    this.basePath = basePath
    this.serializer = serializer
  }

  build (): AggregationTypeSearcher {
    return new AggregationTypeSearcher(this.axiosApi, this.basePath, this.serializer)
  }
}

export class AggregationTypeSearcher {
  private axiosApi: AxiosInstance
  readonly basePath: string
  private serializer: AggregationTypeSerializer

  constructor (axiosApi: AxiosInstance, basePath: string, serializer: AggregationTypeSerializer) {
    this.axiosApi = axiosApi
    this.basePath = basePath
    this.serializer = serializer
  }

  findMatchingAsList (): Promise<AggregationType[]> {
    return this.axiosApi.get(
      this.basePath,
      {
        params: {
          'page[size]': 10000,
          sort: 'term'
        }
      }
    ).then((rawResponse) => {
      const response = rawResponse.data
      return this.serializer.convertJsonApiObjectListToModelList(response)
    })
  }
}
