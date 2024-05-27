/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2023
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Tim Eder <tim.eder@ufz.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 * - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
import { AxiosInstance } from 'axios'

import { SiteUsage } from '@/models/SiteUsage'
import { SiteUsageSerializer } from '@/serializers/jsonapi/SiteUsageSerializer'
import { CVApi } from '@/services/cv/CVApi'

import { IPaginationLoader } from '@/utils/PaginatedLoader'

export class SiteUsageApi extends CVApi<SiteUsage> {
  private serializer: SiteUsageSerializer
  readonly basePath: string

  constructor (axiosInstance: AxiosInstance, basePath: string) {
    super(axiosInstance)
    this.basePath = basePath
    this.serializer = new SiteUsageSerializer()
  }

  newSearchBuilder (): SiteUsageSearchBuilder {
    return new SiteUsageSearchBuilder(this.axiosApi, this.basePath, this.serializer)
  }

  findAll (): Promise<SiteUsage[]> {
    return this.newSearchBuilder().build().findMatchingAsList()
  }

  findAllPaginated (pageSize: number = 100): Promise<SiteUsage[]> {
    return this.newSearchBuilder().build().findMatchingAsPaginationLoader(pageSize).then(loader => this.loadPaginated(loader))
  }

  add (siteUsage: SiteUsage): Promise<SiteUsage> {
    const data = this.serializer.convertModelToJsonApiData(siteUsage)

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

export class SiteUsageSearchBuilder {
  private axiosApi: AxiosInstance
  readonly basePath: string
  private serializer: SiteUsageSerializer

  constructor (axiosApi: AxiosInstance, basePath: string, serializer: SiteUsageSerializer) {
    this.axiosApi = axiosApi
    this.basePath = basePath
    this.serializer = serializer
  }

  build (): SiteUsageSearcher {
    return new SiteUsageSearcher(this.axiosApi, this.basePath, this.serializer)
  }
}

export class SiteUsageSearcher {
  private axiosApi: AxiosInstance
  readonly basePath: string
  private serializer: SiteUsageSerializer

  constructor (axiosApi: AxiosInstance, basePath: string, serializer: SiteUsageSerializer) {
    this.axiosApi = axiosApi
    this.basePath = basePath
    this.serializer = serializer
  }

  private findAllOnPage (page: number, pageSize: number): Promise<IPaginationLoader<SiteUsage>> {
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
      const elements: SiteUsage[] = this.serializer.convertJsonApiObjectListToModelList(response)
      const totalCount = response.meta.count

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

  findMatchingAsList (): Promise<SiteUsage[]> {
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

  findMatchingAsPaginationLoader (pageSize: number): Promise<IPaginationLoader<SiteUsage>> {
    return this.findAllOnPage(1, pageSize)
  }
}
