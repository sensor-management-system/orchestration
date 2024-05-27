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

import { Compartment } from '@/models/Compartment'
import { CompartmentSerializer } from '@/serializers/jsonapi/CompartmentSerializer'
import { CVApi } from '@/services/cv/CVApi'

import { IPaginationLoader } from '@/utils/PaginatedLoader'

export class CompartmentApi extends CVApi<Compartment> {
  private serializer: CompartmentSerializer
  readonly basePath: string

  constructor (axiosInstance: AxiosInstance, basePath: string) {
    super(axiosInstance)
    this.basePath = basePath
    this.serializer = new CompartmentSerializer()
  }

  newSearchBuilder (): CompartmentSearchBuilder {
    return new CompartmentSearchBuilder(this.axiosApi, this.basePath, this.serializer)
  }

  findAll (): Promise<Compartment[]> {
    return this.newSearchBuilder().build().findMatchingAsList()
  }

  findAllPaginated (pageSize: number = 100): Promise<Compartment[]> {
    return this.newSearchBuilder().build().findMatchingAsPaginationLoader(pageSize).then(loader => this.loadPaginated(loader))
  }

  add (compartment: Compartment): Promise<Compartment> {
    const data = this.serializer.convertModelToJsonApiData(compartment)

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

export class CompartmentSearchBuilder {
  private axiosApi: AxiosInstance
  readonly basePath: string
  private serializer: CompartmentSerializer

  constructor (axiosApi: AxiosInstance, basePath: string, serializer: CompartmentSerializer) {
    this.axiosApi = axiosApi
    this.basePath = basePath
    this.serializer = serializer
  }

  build (): CompartmentSearcher {
    return new CompartmentSearcher(this.axiosApi, this.basePath, this.serializer)
  }
}

export class CompartmentSearcher {
  private axiosApi: AxiosInstance
  readonly basePath: string
  private serializer: CompartmentSerializer

  constructor (axiosApi: AxiosInstance, basePath: string, serializer: CompartmentSerializer) {
    this.axiosApi = axiosApi
    this.basePath = basePath
    this.serializer = serializer
  }

  private findAllOnPage (page: number, pageSize: number): Promise<IPaginationLoader<Compartment>> {
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
      const elements: Compartment[] = this.serializer.convertJsonApiObjectListToModelList(response)
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

  findMatchingAsList (): Promise<Compartment[]> {
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

  findMatchingAsPaginationLoader (pageSize: number): Promise<IPaginationLoader<Compartment>> {
    return this.findAllOnPage(1, pageSize)
  }
}
