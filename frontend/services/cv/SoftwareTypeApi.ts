/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
import { AxiosInstance } from 'axios'

import { SoftwareType } from '@/models/SoftwareType'
import { SoftwareTypeSerializer } from '@/serializers/jsonapi/SoftwareTypeSerializer'
import { CVApi } from '@/services/cv/CVApi'

import { IPaginationLoader } from '@/utils/PaginatedLoader'

export class SoftwareTypeApi extends CVApi<SoftwareType> {
  private serializer: SoftwareTypeSerializer
  readonly basePath: string

  constructor (axiosInstance: AxiosInstance, basePath: string) {
    super(axiosInstance)
    this.basePath = basePath
    this.serializer = new SoftwareTypeSerializer()
  }

  newSearchBuilder (): SoftwareTypeSearchBuilder {
    return new SoftwareTypeSearchBuilder(this.axiosApi, this.basePath, this.serializer)
  }

  findAll (): Promise<SoftwareType[]> {
    return this.newSearchBuilder().build().findMatchingAsList().then(data => SoftwareTypeApi.sort(data))
  }

  findAllPaginated (pageSize: number = 100): Promise<SoftwareType[]> {
    return this.newSearchBuilder().build().findMatchingAsPaginationLoader(pageSize).then(loader => this.loadPaginated(loader)).then(data => SoftwareTypeApi.sort(data))
  }

  static sort (softwareTypes: SoftwareType[]): SoftwareType[] {
    const softwareTypesCopy: SoftwareType[] = [...softwareTypes]
    // sort alphabetical
    softwareTypesCopy.sort((a, b) => {
      if (a.name < b.name) {
        return -1
      }
      if (a.name > b.name) {
        return 1
      }
      return 0
    })
    // move 'Others' to the end
    const othersIndex: number = softwareTypesCopy.findIndex(i => i.name.toLowerCase() === 'others')
    if (othersIndex > -1) {
      const other: SoftwareType = softwareTypesCopy.splice(othersIndex, 1)[0]
      softwareTypesCopy.push(other)
    }
    return softwareTypesCopy
  }
}

export class SoftwareTypeSearchBuilder {
  private axiosApi: AxiosInstance
  readonly basePath: string
  private serializer: SoftwareTypeSerializer

  constructor (axiosApi: AxiosInstance, basePath: string, serializer: SoftwareTypeSerializer) {
    this.axiosApi = axiosApi
    this.basePath = basePath
    this.serializer = serializer
  }

  build (): SoftwareTypeSearcher {
    return new SoftwareTypeSearcher(this.axiosApi, this.basePath, this.serializer)
  }
}

export class SoftwareTypeSearcher {
  private axiosApi: AxiosInstance
  readonly basePath: string
  private serializer: SoftwareTypeSerializer

  constructor (axiosApi: AxiosInstance, basePath: string, serializer: SoftwareTypeSerializer) {
    this.axiosApi = axiosApi
    this.basePath = basePath
    this.serializer = serializer
  }

  private findAllOnPage (page: number, pageSize: number): Promise<IPaginationLoader<SoftwareType>> {
    const params: { [idx: string]: any } = {
      'page[size]': pageSize,
      'page[number]': page,
      'filter[status.iexact]': 'ACCEPTED',
      sort: 'term'
    }
    return this.axiosApi.get(
      this.basePath,
      {
        params
      }
    ).then((rawResponse) => {
      const response = rawResponse.data
      const elements: SoftwareType[] = this.serializer.convertJsonApiObjectListToModelList(response)
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

  findMatchingAsList (): Promise<SoftwareType[]> {
    const params: { [idx: string]: any } = {
      'page[size]': 10000,
      'filter[status.iexact]': 'ACCEPTED',
      sort: 'term'
    }
    return this.axiosApi.get(
      this.basePath,
      {
        params
      }
    ).then((rawResponse) => {
      const response = rawResponse.data
      return this.serializer.convertJsonApiObjectListToModelList(response)
    })
  }

  findMatchingAsPaginationLoader (pageSize: number): Promise<IPaginationLoader<SoftwareType>> {
    return this.findAllOnPage(1, pageSize)
  }
}
