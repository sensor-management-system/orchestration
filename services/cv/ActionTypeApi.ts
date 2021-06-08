/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020
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

import { ActionType } from '@/models/ActionType'
import { ActionTypeSerializer } from '@/serializers/jsonapi/ActionTypeSerializer'
import { CVApi } from '@/services/cv/CVApi'

import { IPaginationLoader } from '@/utils/PaginatedLoader'

export class ActionTypeApi extends CVApi<ActionType> {
  private serializer: ActionTypeSerializer

  constructor (axiosInstance: AxiosInstance) {
    super(axiosInstance)
    this.serializer = new ActionTypeSerializer()
  }

  newSearchBuilder (): ActionTypeSearchBuilder {
    return new ActionTypeSearchBuilder(this.axiosApi, this.serializer)
  }

  findAll (): Promise<ActionType[]> {
    return this.newSearchBuilder().build().findMatchingAsList()
  }

  findAllPaginated (pageSize: number = 100): Promise<ActionType[]> {
    return this.newSearchBuilder().build().findMatchingAsPaginationLoader(pageSize).then(loader => this.loadPaginated(loader))
  }
}

export const ACTION_TYPE_API_FILTER_DEVICE = 'Device'
export const ACTION_TYPE_API_FILTER_PLATFORM = 'Platform'
export const ACTION_TYPE_API_FILTER_CONFIGURATION = 'Configuration'
export type ActionTypeApiFilterType = typeof ACTION_TYPE_API_FILTER_DEVICE | typeof ACTION_TYPE_API_FILTER_PLATFORM | typeof ACTION_TYPE_API_FILTER_CONFIGURATION

export class ActionTypeSearchBuilder {
  private axiosApi: AxiosInstance
  private serializer: ActionTypeSerializer
  private actionTypeFilter: ActionTypeApiFilterType | undefined

  constructor (axiosApi: AxiosInstance, serializer: ActionTypeSerializer) {
    this.axiosApi = axiosApi
    this.serializer = serializer
  }

  onlyType (actionType: ActionTypeApiFilterType): ActionTypeSearchBuilder {
    this.actionTypeFilter = actionType
    return this
  }

  build (): ActionTypeSearcher {
    return new ActionTypeSearcher(this.axiosApi, this.serializer, this.actionTypeFilter)
  }
}

export class ActionTypeSearcher {
  private axiosApi: AxiosInstance
  private serializer: ActionTypeSerializer
  private actionTypeFilter: ActionTypeApiFilterType | undefined

  constructor (axiosApi: AxiosInstance, serializer: ActionTypeSerializer, actionType?: ActionTypeApiFilterType) {
    this.axiosApi = axiosApi
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
      '',
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

      return {
        elements,
        totalCount,
        funToLoadNext
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
      '',
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
