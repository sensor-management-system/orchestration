/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2022
 * - Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
 * - Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
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
