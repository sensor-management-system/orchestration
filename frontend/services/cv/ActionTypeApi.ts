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

import { ActionType } from '@/models/ActionType'
import { ActionTypeSerializer } from '@/serializers/jsonapi/ActionTypeSerializer'
import { CVApi } from '@/services/cv/CVApi'

import { IPaginationLoader } from '@/utils/PaginatedLoader'

export class ActionTypeApi extends CVApi<ActionType> {
  private serializer: ActionTypeSerializer
  readonly basePath: string

  constructor (axiosInstance: AxiosInstance, basePath: string) {
    super(axiosInstance)
    this.basePath = basePath
    this.serializer = new ActionTypeSerializer()
  }

  newSearchBuilder (): ActionTypeSearchBuilder {
    return new ActionTypeSearchBuilder(this.axiosApi, this.basePath, this.serializer)
  }

  findAll (): Promise<ActionType[]> {
    return this.newSearchBuilder().build().findMatchingAsList()
  }

  findAllPaginated (pageSize: number = 100): Promise<ActionType[]> {
    return this.newSearchBuilder().build().findMatchingAsPaginationLoader(pageSize).then(loader => this.loadPaginated(loader))
  }

  add (actionType: ActionType): Promise<ActionType> {
    const data = this.serializer.convertModelToJsonApiData(actionType)

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

export const ACTION_TYPE_API_FILTER_DEVICE = 'Device'
export const ACTION_TYPE_API_FILTER_PLATFORM = 'Platform'
export const ACTION_TYPE_API_FILTER_CONFIGURATION = 'Configuration'
export type ActionTypeApiFilterType = typeof ACTION_TYPE_API_FILTER_DEVICE | typeof ACTION_TYPE_API_FILTER_PLATFORM | typeof ACTION_TYPE_API_FILTER_CONFIGURATION

export class ActionTypeSearchBuilder {
  private axiosApi: AxiosInstance
  readonly basePath: string
  private serializer: ActionTypeSerializer
  private actionTypeFilter: ActionTypeApiFilterType | undefined

  constructor (axiosApi: AxiosInstance, basePath: string, serializer: ActionTypeSerializer) {
    this.axiosApi = axiosApi
    this.basePath = basePath
    this.serializer = serializer
  }

  onlyType (actionType: ActionTypeApiFilterType): ActionTypeSearchBuilder {
    this.actionTypeFilter = actionType
    return this
  }

  build (): ActionTypeSearcher {
    return new ActionTypeSearcher(this.axiosApi, this.basePath, this.serializer, this.actionTypeFilter)
  }
}

export class ActionTypeSearcher {
  private axiosApi: AxiosInstance
  readonly basePath: string
  private serializer: ActionTypeSerializer
  private actionTypeFilter: ActionTypeApiFilterType | undefined

  constructor (axiosApi: AxiosInstance, basePath: string, serializer: ActionTypeSerializer, actionType?: ActionTypeApiFilterType) {
    this.axiosApi = axiosApi
    this.basePath = basePath
    this.serializer = serializer
    if (actionType) {
      this.actionTypeFilter = actionType
    }
  }

  private findAllOnPage (page: number, pageSize: number): Promise<IPaginationLoader<ActionType>> {
    const params: { [idx: string]: any } = {
      'page[size]': pageSize,
      'page[number]': page,
      'filter[status.iexact]': 'ACCEPTED',
      sort: 'term'
    }
    if (this.actionTypeFilter) {
      params['filter[action_category__term]'] = this.actionTypeFilter
    }
    return this.axiosApi.get(
      this.basePath,
      {
        params
      }
    ).then((rawResponse) => {
      const response = rawResponse.data
      const elements: ActionType[] = this.serializer.convertJsonApiObjectListToModelList(response)
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

  findMatchingAsList (): Promise<ActionType[]> {
    const params: { [idx: string]: any } = {
      'page[size]': 10000,
      'filter[status.iexact]': 'ACCEPTED',
      sort: 'term'
    }
    if (this.actionTypeFilter) {
      params['filter[action_category__term]'] = this.actionTypeFilter
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

  findMatchingAsPaginationLoader (pageSize: number): Promise<IPaginationLoader<ActionType>> {
    return this.findAllOnPage(1, pageSize)
  }
}
