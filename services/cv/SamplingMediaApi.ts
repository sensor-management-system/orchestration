/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020
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

import { SamplingMedia } from '@/models/SamplingMedia'
import { SamplingMediaSerializer } from '@/serializers/jsonapi/SamplingMediaSerializer'

export class SamplingMediaApi {
  private axiosApi: AxiosInstance
  private serializer: SamplingMediaSerializer

  constructor (axiosInstance: AxiosInstance) {
    this.axiosApi = axiosInstance
    this.serializer = new SamplingMediaSerializer()
  }

  newSearchBuilder (): SamplingMediaSearchBuilder {
    return new SamplingMediaSearchBuilder(this.axiosApi, this.serializer)
  }

  findAll (): Promise<SamplingMedia[]> {
    return this.newSearchBuilder().build().findMatchingAsList()
  }
}

export class SamplingMediaSearchBuilder {
  private axiosApi: AxiosInstance
  private serializer: SamplingMediaSerializer

  constructor (axiosApi: AxiosInstance, serializer: SamplingMediaSerializer) {
    this.axiosApi = axiosApi
    this.serializer = serializer
  }

  build (): SamplingMediaSearcher {
    return new SamplingMediaSearcher(this.axiosApi, this.serializer)
  }
}

export class SamplingMediaSearcher {
  private axiosApi: AxiosInstance
  private serializer: SamplingMediaSerializer

  constructor (axiosApi: AxiosInstance, serializer: SamplingMediaSerializer) {
    this.axiosApi = axiosApi
    this.serializer = serializer
  }

  findMatchingAsList (): Promise<SamplingMedia[]> {
    return this.axiosApi.get(
      '',
      {
        params: {
          'page[size]': 10000,
          'filter[status.iexact]': 'ACCEPTED',
          sort: 'term'
        }
      }
    ).then((rawResponse) => {
      const response = rawResponse.data
      return this.serializer.convertJsonApiObjectListToModelList(response)
    })
  }
}
