/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2026
 * - Nils Brinckmann <nils.brinckmann@gfz.de>
 * - GFZ Helmholtz for Geosciences (GFZ, https://www.gfz.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
import { AxiosInstance, Method } from 'axios'

import { Organization } from '@/models/Organization'
import { IOrganizationSearchParams } from '@/modelUtils/OrganizationSearchParams'
import { OrganizationSerializer } from '@/serializers/jsonapi/OrganizationSerializer'

export interface SearchResult {
  elements: Organization[]
  totalCount: number
}

export class OrganizationApi {
  private axiosApi: AxiosInstance
  private readonly basePath: string
  private serializer: OrganizationSerializer

  constructor (axiosInstance: AxiosInstance, basePath: string) {
    this.axiosApi = axiosInstance
    this.basePath = basePath

    this.serializer = new OrganizationSerializer()
  }

  async searchPaginated (
    searchParams: IOrganizationSearchParams,
    pageNumber: number,
    pageSize: number
  ): Promise<SearchResult> {
    const filterParams: {[key: string]: any} = {}
    if (searchParams.searchText) {
      filterParams.q = searchParams.searchText
    }

    const rawResponse = await this.axiosApi.get(this.basePath, {
      params: {
        'page[size]': pageSize,
        'page[number]': pageNumber,
        sort: 'name',
        ...filterParams
      }
    })

    const rawData = rawResponse.data
    const elements: Organization[] = this.serializer.convertJsonApiObjectListToModelList(rawData)
    const totalCount = rawData.meta.count

    return {
      elements,
      totalCount
    }
  }

  async findById (id: string): Promise<Organization> {
    const rawResponse = await this.axiosApi.get(`${this.basePath}/${id}`)
    const rawData = rawResponse.data
    return this.serializer.convertJsonApiObjectToModel(rawData)
  }

  async findByName (name: string): Promise<Organization | null> {
    const rawResponse = await this.axiosApi.get(this.basePath, {
      params: {
        'filter[name]': name
      }
    })
    const rawData = rawResponse.data
    const elements: Organization[] = this.serializer.convertJsonApiObjectListToModelList(rawData)
    if (elements.length > 0) {
      return elements[0]
    }
    return null
  }

  async save (organization: Organization): Promise<Organization> {
    const data: any = this.serializer.convertModelToJsonApiData(organization)
    let method: Method = 'patch'
    let url = this.basePath

    if (!organization.id) {
      method = 'post'
    } else {
      url += '/' + organization.id
    }

    const serverAnswer = await this.axiosApi.request({ url, method, data: { data } })
    return this.serializer.convertJsonApiObjectToModel(serverAnswer.data)
  }

  async deleteById (id: string): Promise<void> {
    const url = `${this.basePath}/${id}`
    await this.axiosApi.delete(url)
  }
}
