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

import { GlobalProvenance } from '@/models/GlobalProvenance'
import { GlobalProvenanceSerializer } from '@/serializers/jsonapi/GlobalProvenanceSerializer'
import { CVApi } from '@/services/cv/CVApi'

export class GlobalProvenanceApi extends CVApi<GlobalProvenance> {
  private serializer: GlobalProvenanceSerializer
  readonly basePath: string

  constructor (axiosInstance: AxiosInstance, basePath: string) {
    super(axiosInstance)
    this.basePath = basePath
    this.serializer = new GlobalProvenanceSerializer()
  }

  newSearchBuilder (): GlobalProvenanceSearchBuilder {
    return new GlobalProvenanceSearchBuilder(this.axiosApi, this.basePath, this.serializer)
  }

  findAll (): Promise<GlobalProvenance[]> {
    return this.newSearchBuilder().build().findMatchingAsList()
  }
}

export class GlobalProvenanceSearchBuilder {
  private axiosApi: AxiosInstance
  readonly basePath: string
  private serializer: GlobalProvenanceSerializer

  constructor (axiosApi: AxiosInstance, basePath: string, serializer: GlobalProvenanceSerializer) {
    this.axiosApi = axiosApi
    this.basePath = basePath
    this.serializer = serializer
  }

  build (): GlobalProvenanceSearcher {
    return new GlobalProvenanceSearcher(this.axiosApi, this.basePath, this.serializer)
  }
}

export class GlobalProvenanceSearcher {
  private axiosApi: AxiosInstance
  readonly basePath: string
  private serializer: GlobalProvenanceSerializer

  constructor (axiosApi: AxiosInstance, basePath: string, serializer: GlobalProvenanceSerializer) {
    this.axiosApi = axiosApi
    this.basePath = basePath
    this.serializer = serializer
  }

  findMatchingAsList (): Promise<GlobalProvenance[]> {
    return this.axiosApi.get(
      this.basePath,
      {
        params: {
          'page[size]': 10000,
          sort: 'name'
        }
      }
    ).then((rawResponse) => {
      const response = rawResponse.data
      return this.serializer.convertJsonApiObjectListToModelList(response)
    })
  }
}
