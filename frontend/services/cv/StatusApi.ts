/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2022
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
import { AxiosInstance } from 'axios'

import { Status } from '@/models/Status'
import { StatusSerializer } from '@/serializers/jsonapi/StatusSerializer'
import { CVApi } from '@/services/cv/CVApi'

import { IPaginationLoader } from '@/utils/PaginatedLoader'

export class StatusApi extends CVApi<Status> {
  private serializer: StatusSerializer
  readonly basePath: string

  constructor (axiosInstance: AxiosInstance, basePath: string) {
    super(axiosInstance)
    this.basePath = basePath
    this.serializer = new StatusSerializer()
  }

  newSearchBuilder (): StatusSearchBuilder {
    return new StatusSearchBuilder(this.axiosApi, this.basePath, this.serializer)
  }

  findAll (): Promise<Status[]> {
    return this.newSearchBuilder().build().findMatchingAsList()
  }

  findAllPaginated (pageSize: number = 100): Promise<Status[]> {
    return this.newSearchBuilder().build().findMatchingAsPaginationLoader(pageSize).then(loader => this.loadPaginated(loader))
  }

  add (status: Status): Promise<Status> {
    const data = this.serializer.convertModelToJsonApiData(status)

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

export class StatusSearchBuilder {
  private axiosApi: AxiosInstance
  readonly basePath: string
  private serializer: StatusSerializer

  constructor (axiosApi: AxiosInstance, basePath: string, serializer: StatusSerializer) {
    this.axiosApi = axiosApi
    this.basePath = basePath
    this.serializer = serializer
  }

  build (): StatusSearcher {
    return new StatusSearcher(this.axiosApi, this.basePath, this.serializer)
  }
}

export class StatusSearcher {
  private axiosApi: AxiosInstance
  readonly basePath: string
  private serializer: StatusSerializer

  constructor (axiosApi: AxiosInstance, basePath: string, serializer: StatusSerializer) {
    this.axiosApi = axiosApi
    this.basePath = basePath
    this.serializer = serializer
  }

  private findAllOnPage (page: number, pageSize: number): Promise<IPaginationLoader<Status>> {
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
      const elements: Status[] = this.serializer.convertJsonApiObjectListToModelList(response)
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

  findMatchingAsList (): Promise<Status[]> {
    return this.axiosApi.get(
      this.basePath,
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

  findMatchingAsPaginationLoader (pageSize: number): Promise<IPaginationLoader<Status>> {
    return this.findAllOnPage(1, pageSize)
  }
}
