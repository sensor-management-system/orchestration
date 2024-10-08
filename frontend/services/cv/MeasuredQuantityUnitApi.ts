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

import { MeasuredQuantityUnit } from '@/models/MeasuredQuantityUnit'
import { MeasuredQuantityUnitSerializer } from '@/serializers/jsonapi/MeasuredQuantityUnitSerializer'
import { CVApi } from '@/services/cv/CVApi'

import { IPaginationLoader } from '@/utils/PaginatedLoader'

export class MeasuredQuantityUnitApi extends CVApi<MeasuredQuantityUnit> {
  private serializer: MeasuredQuantityUnitSerializer
  readonly basePath: string

  constructor (axiosInstance: AxiosInstance, basePath: string) {
    super(axiosInstance)
    this.basePath = basePath
    this.serializer = new MeasuredQuantityUnitSerializer()
  }

  newSearchBuilder (): MeasuredQuantityUnitSearchBuilder {
    return new MeasuredQuantityUnitSearchBuilder(this.axiosApi, this.basePath, this.serializer)
  }

  findAll (): Promise<MeasuredQuantityUnit[]> {
    return this.newSearchBuilder().build().findMatchingAsList()
  }

  findAllPaginated (pageSize: number = 100): Promise<MeasuredQuantityUnit[]> {
    return this.newSearchBuilder().build().findMatchingAsPaginationLoader(pageSize).then(loader => this.loadPaginated(loader))
  }

  async find (id: string): Promise<MeasuredQuantityUnit> {
    const rawResponse = await this.axiosApi.get(this.basePath + id + '?include=unit')
    const response = rawResponse.data
    this.serializer.included = response.included
    return this.serializer.convertJsonApiDataToModel(response.data)
  }

  async add (measuredQuantityUnit: MeasuredQuantityUnit): Promise<MeasuredQuantityUnit> {
    const data = this.serializer.convertModelToJsonApiData(measuredQuantityUnit)

    const rawResponse = await this.axiosApi.post(
      this.basePath,
      {
        data
      },
      {
        headers: {
          'Content-Type': 'application/vnd.api+json'
        }
      }
    )
    const response = rawResponse.data
    const id = response.data.id
    return await this.find(id)
  }
}

export class MeasuredQuantityUnitSearchBuilder {
  private axiosApi: AxiosInstance
  readonly basePath: string
  private serializer: MeasuredQuantityUnitSerializer

  constructor (axiosApi: AxiosInstance, basePath: string, serializer: MeasuredQuantityUnitSerializer) {
    this.axiosApi = axiosApi
    this.basePath = basePath
    this.serializer = serializer
  }

  build (): MeasuredQuantityUnitSearcher {
    return new MeasuredQuantityUnitSearcher(this.axiosApi, this.basePath, this.serializer)
  }
}

export class MeasuredQuantityUnitSearcher {
  private axiosApi: AxiosInstance
  readonly basePath: string
  private serializer: MeasuredQuantityUnitSerializer

  constructor (axiosApi: AxiosInstance, basePath: string, serializer: MeasuredQuantityUnitSerializer) {
    this.axiosApi = axiosApi
    this.basePath = basePath
    this.serializer = serializer
  }

  private findAllOnPage (page: number, pageSize: number): Promise<IPaginationLoader<MeasuredQuantityUnit>> {
    return this.axiosApi.get(
      this.basePath,
      {
        params: {
          'page[size]': pageSize,
          'page[number]': page,
          include: 'unit'
        }
      }
    ).then((rawResponse) => {
      const response = rawResponse.data
      this.serializer.included = response.included
      const elements: MeasuredQuantityUnit[] = this.serializer.convertJsonApiObjectListToModelList(response)
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

  findMatchingAsList (): Promise<MeasuredQuantityUnit[]> {
    return this.axiosApi.get(
      this.basePath,
      {
        params: {
          'page[size]': 10000,
          include: 'unit'
        }
      }
    ).then((rawResponse) => {
      const response = rawResponse.data
      this.serializer.included = response.included
      return this.serializer.convertJsonApiObjectListToModelList(response)
    })
  }

  findMatchingAsPaginationLoader (pageSize: number): Promise<IPaginationLoader<MeasuredQuantityUnit>> {
    return this.findAllOnPage(1, pageSize)
  }
}
