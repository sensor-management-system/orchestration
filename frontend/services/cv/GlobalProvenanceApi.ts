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
