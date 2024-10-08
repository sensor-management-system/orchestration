/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2023 - 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
import { AxiosInstance } from 'axios'

import { License } from '@/models/License'
import { LicenseSerializer } from '@/serializers/jsonapi/LicenseSerializer'
import { CVApi } from '@/services/cv/CVApi'

import { IPaginationLoader } from '@/utils/PaginatedLoader'

export class LicenseApi extends CVApi<License> {
  private serializer: LicenseSerializer
  readonly basePath: string

  constructor (axiosInstance: AxiosInstance, basePath: string) {
    super(axiosInstance)
    this.basePath = basePath
    this.serializer = new LicenseSerializer()
  }

  newSearchBuilder (): LicenseSearchBuilder {
    return new LicenseSearchBuilder(this.axiosApi, this.basePath, this.serializer)
  }

  findAll (): Promise<License[]> {
    return this.newSearchBuilder().build().findMatchingAsList()
  }

  findAllPaginated (pageSize: number = 100): Promise<License[]> {
    return this.newSearchBuilder().build().findMatchingAsPaginationLoader(pageSize).then(loader => this.loadPaginated(loader))
  }

  add (license: License): Promise<License> {
    const data = this.serializer.convertModelToJsonApiData(license)

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

export class LicenseSearchBuilder {
  private axiosApi: AxiosInstance
  readonly basePath: string
  private serializer: LicenseSerializer

  constructor (axiosApi: AxiosInstance, basePath: string, serializer: LicenseSerializer) {
    this.axiosApi = axiosApi
    this.basePath = basePath
    this.serializer = serializer
  }

  build (): LicenseSearcher {
    return new LicenseSearcher(this.axiosApi, this.basePath, this.serializer)
  }
}

export class LicenseSearcher {
  private axiosApi: AxiosInstance
  readonly basePath: string
  private serializer: LicenseSerializer

  constructor (axiosApi: AxiosInstance, basePath: string, serializer: LicenseSerializer) {
    this.axiosApi = axiosApi
    this.basePath = basePath
    this.serializer = serializer
  }

  private findAllOnPage (page: number, pageSize: number): Promise<IPaginationLoader<License>> {
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
      const elements: License[] = this.serializer.convertJsonApiObjectListToModelList(response)
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

  findMatchingAsList (): Promise<License[]> {
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

  findMatchingAsPaginationLoader (pageSize: number): Promise<IPaginationLoader<License>> {
    return this.findAllOnPage(1, pageSize)
  }
}
