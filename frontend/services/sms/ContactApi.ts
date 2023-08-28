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
import { AxiosInstance, Method } from 'axios'

import { Contact } from '@/models/Contact'
import { ContactSerializer } from '@/serializers/jsonapi/ContactSerializer'
import { IPaginationLoader } from '@/utils/PaginatedLoader'

export class ContactApi {
  private axiosApi: AxiosInstance
  readonly basePath: string
  private serializer: ContactSerializer

  constructor (axiosInstance: AxiosInstance, basePath: string) {
    this.axiosApi = axiosInstance
    this.basePath = basePath
    this.serializer = new ContactSerializer()
  }

  searchPaginated (pageNumber: number, pageSize: number, search: string = '') {
    const queryParams = {
      params: {
        'page[number]': pageNumber,
        'page[size]': pageSize,
        sort: 'family_name'
      }
    }
    if (search !== '') {
      // @ts-ignore
      queryParams.params.q = search
    }

    return this.axiosApi.get(
      this.basePath,
      queryParams
    ).then((rawResponse) => {
      const rawData = rawResponse.data
      const elements: Contact[] = this.serializer.convertJsonApiObjectListToModelList(rawData)
      const totalCount = rawData.meta.count

      return {
        elements,
        totalCount
      }
    })
  }

  findById (id: string): Promise<Contact> {
    return this.axiosApi.get(this.basePath + '/' + id, {
      params: {
        // maybe add something later
      }
    }).then((rawResponse) => {
      const rawData = rawResponse.data
      return this.serializer.convertJsonApiDataToModel(rawData.data)
    })
  }

  deleteById (id: string): Promise<void> {
    return this.axiosApi.delete<string, void>(this.basePath + '/' + id)
  }

  save (contact: Contact): Promise<Contact> {
    const data: any = this.serializer.convertModelToJsonApiData(contact)
    let method: Method = 'patch'
    let url = this.basePath

    if (contact.id === null) {
      // new -> post
      method = 'post'
    } else {
      // old -> patch
      url += '/' + String(contact.id)
    }

    return this.axiosApi.request({
      url,
      method,
      data: {
        data
      }
    }).then((serverAnswer) => {
      return this.findById(serverAnswer.data.data.id)
    })
  }

  newSearchBuilder (): ContactSearchBuilder {
    return new ContactSearchBuilder(this.axiosApi, this.basePath, this.serializer)
  }

  findAll (): Promise<Contact[]> {
    return this.newSearchBuilder().build().findMatchingAsList()
  }
}

export function serverResponseToEntity (entry: any): Contact {
  const attributes = entry.attributes
  const newEntry = Contact.createEmpty()

  newEntry.id = entry.id
  newEntry.givenName = attributes.given_name || ''
  newEntry.familyName = attributes.family_name || ''
  newEntry.website = attributes.website || ''
  newEntry.email = attributes.email

  // todo: Check list of platforms, list of devices and the user

  return newEntry
}

export class ContactSearchBuilder {
  private axiosApi: AxiosInstance
  readonly basePath: string
  private serializer: ContactSerializer
  private esTextFilter: string | null = null

  constructor (axiosApi: AxiosInstance, basePath: string, serializer: ContactSerializer) {
    this.axiosApi = axiosApi
    this.basePath = basePath
    this.serializer = serializer
  }

  withText (text: string) {
    if (text) {
      this.esTextFilter = text
    }
    return this
  }

  build (): ContactSearcher {
    return new ContactSearcher(this.axiosApi, this.basePath, this.serializer, this.esTextFilter)
  }
}

export class ContactSearcher {
  private axiosApi: AxiosInstance
  readonly basePath: string
  private serializer: ContactSerializer
  private esTextFilter: string | null

  constructor (axiosApi: AxiosInstance, basePath: string, serializer: ContactSerializer, esTextFilter: string | null) {
    this.axiosApi = axiosApi
    this.basePath = basePath
    this.serializer = serializer
    this.esTextFilter = esTextFilter
  }

  private get commonParams (): any {
    const result: any = {}
    if (this.esTextFilter) {
      result.q = this.esTextFilter
    } else {
      result.sort = 'family_name'
    }
    return result
  }

  findMatchingAsList (): Promise<Contact[]> {
    return this.axiosApi.get(
      // we use the base path
      this.basePath,
      {
        params: {
          'page[size]': 10000,
          ...this.commonParams
        }
      }).then((rawResponse: any) => {
      return this.serializer.convertJsonApiObjectListToModelList(rawResponse.data)
    })
  }

  findMatchingAsPaginationLoaderOnPage (page: number, pageSize: number): Promise<IPaginationLoader<Contact>> {
    return this.findAllOnPage(page, pageSize)
  }

  private findAllOnPage (page: number, pageSize: number): Promise<IPaginationLoader<Contact>> {
    return this.axiosApi.get(
      this.basePath,
      {
        params: {
          'page[size]': pageSize,
          'page[number]': page,
          ...this.commonParams
        }
      }
    ).then((rawResponse) => {
      const rawData = rawResponse.data
      const elements: Contact[] = this.serializer.convertJsonApiObjectListToModelList(rawData)

      const totalCount = rawData.meta.count

      // check if the provided page param is valid
      if (totalCount > 0 && elements.length === 0) {
        throw new RangeError('page is out of bounds')
      }

      let funToLoadNext = null
      if (elements.length > 0) {
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
}
