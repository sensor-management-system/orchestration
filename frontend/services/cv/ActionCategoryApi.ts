/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2022
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

import { ActionCategory } from '@/models/ActionCategory'
import { ActionCategorySerializer } from '@/serializers/jsonapi/ActionCategorySerializer'
import { CVApi } from '@/services/cv/CVApi'

import { IPaginationLoader } from '@/utils/PaginatedLoader'

export class ActionCategoryApi extends CVApi<ActionCategory> {
  private serializer: ActionCategorySerializer
  readonly basePath: string

  constructor (axiosInstance: AxiosInstance, basePath: string) {
    super(axiosInstance)
    this.basePath = basePath
    this.serializer = new ActionCategorySerializer()
  }

  newSearchBuilder (): ActionCategorySearchBuilder {
    return new ActionCategorySearchBuilder(this.axiosApi, this.basePath, this.serializer)
  }

  findAll (): Promise<ActionCategory[]> {
    return this.newSearchBuilder().build().findMatchingAsList()
  }

  findAllPaginated (pageSize: number = 100): Promise<ActionCategory[]> {
    return this.newSearchBuilder().build().findMatchingAsPaginationLoader(pageSize).then(loader => this.loadPaginated(loader))
  }
}

export class ActionCategorySearchBuilder {
  private axiosApi: AxiosInstance
  readonly basePath: string
  private serializer: ActionCategorySerializer

  constructor (axiosApi: AxiosInstance, basePath: string, serializer: ActionCategorySerializer) {
    this.axiosApi = axiosApi
    this.basePath = basePath
    this.serializer = serializer
  }

  build (): ActionCategorySearcher {
    return new ActionCategorySearcher(this.axiosApi, this.basePath, this.serializer)
  }
}

export class ActionCategorySearcher {
  private axiosApi: AxiosInstance
  readonly basePath: string
  private serializer: ActionCategorySerializer

  constructor (axiosApi: AxiosInstance, basePath: string, serializer: ActionCategorySerializer) {
    this.axiosApi = axiosApi
    this.basePath = basePath
    this.serializer = serializer
  }

  private findAllOnPage (page: number, pageSize: number): Promise<IPaginationLoader<ActionCategory>> {
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
      const elements: ActionCategory[] = this.serializer.convertJsonApiObjectListToModelList(response)
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

  findMatchingAsList (): Promise<ActionCategory[]> {
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

  findMatchingAsPaginationLoader (pageSize: number): Promise<IPaginationLoader<ActionCategory>> {
    return this.findAllOnPage(1, pageSize)
  }
}