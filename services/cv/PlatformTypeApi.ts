/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020 - 2022
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

import { PlatformType } from '@/models/PlatformType'
import { PlatformTypeSerializer } from '@/serializers/jsonapi/PlatformTypeSerializer'
import { CVApi } from '@/services/cv/CVApi'

import { IPaginationLoader } from '@/utils/PaginatedLoader'

export class PlatformTypeApi extends CVApi<PlatformType> {
  private serializer: PlatformTypeSerializer
  readonly basePath: string

  constructor (axiosInstance: AxiosInstance, basePath: string) {
    super(axiosInstance)
    this.basePath = basePath
    this.serializer = new PlatformTypeSerializer()
  }

  newSearchBuilder (): PlatformTypeSearchBuilder {
    return new PlatformTypeSearchBuilder(this.axiosApi, this.basePath, this.serializer)
  }

  findAll (): Promise<PlatformType[]> {
    return this.newSearchBuilder().build().findMatchingAsList()
  }

  findAllPaginated (pageSize: number = 100): Promise<PlatformType[]> {
    return this.newSearchBuilder().build().findMatchingAsPaginationLoader(pageSize).then(loader => this.loadPaginated(loader))
  }

  add (platformType: PlatformType): Promise<PlatformType> {
    const data = this.serializer.convertModelToJsonApiData(platformType)

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

export class PlatformTypeSearchBuilder {
  private axiosApi: AxiosInstance
  readonly basePath: string
  private serializer: PlatformTypeSerializer

  constructor (axiosApi: AxiosInstance, basePath: string, serializer: PlatformTypeSerializer) {
    this.axiosApi = axiosApi
    this.basePath = basePath
    this.serializer = serializer
  }

  build (): PlatformTypeSearcher {
    return new PlatformTypeSearcher(this.axiosApi, this.basePath, this.serializer)
  }
}

export class PlatformTypeSearcher {
  private axiosApi: AxiosInstance
  readonly basePath: string
  private serializer: PlatformTypeSerializer

  constructor (axiosApi: AxiosInstance, basePath: string, serializer: PlatformTypeSerializer) {
    this.axiosApi = axiosApi
    this.basePath = basePath
    this.serializer = serializer
  }

  private findAllOnPage (page: number, pageSize: number): Promise<IPaginationLoader<PlatformType>> {
    return this.axiosApi.get(
      this.basePath,
      {
        params: {
          'page[size]': pageSize,
          'page[number]': page,
          'filter[status.iexact]': 'ACCEPTED',
          sort: 'term'
        }
      }
    ).then((rawResponse) => {
      const response = rawResponse.data
      const elements: PlatformType[] = this.serializer.convertJsonApiObjectListToModelList(response)
      const totalCount = response.meta.pagination.count

      let funToLoadNext = null
      if (response.meta.pagination.page < response.meta.pagination.pages) {
        funToLoadNext = () => this.findAllOnPage(page + 1, pageSize)
      }

      let funToLoadPage = null
      if (elements.length > 0) {
        funToLoadPage = (pageNr: number) => this.findAllOnPage(pageNr, pageSize)
      }

      return {
        elements,
        totalCount,
        page,
        funToLoadNext,
        funToLoadPage
      }
    })
  }

  findMatchingAsList (): Promise<PlatformType[]> {
    return this.axiosApi.get(
      this.basePath,
      {
        params: {
          'page[limit]': 10000,
          'filter[status.iexact]': 'ACCEPTED',
          sort: 'term'
        }
      }
    ).then((rawResponse) => {
      const response = rawResponse.data
      return this.serializer.convertJsonApiObjectListToModelList(response)
    })
  }

  findMatchingAsPaginationLoader (pageSize: number): Promise<IPaginationLoader<PlatformType>> {
    return this.findAllOnPage(1, pageSize)
  }
}
