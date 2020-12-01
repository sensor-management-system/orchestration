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

import { Platform } from '@/models/Platform'
import { PlatformType } from '@/models/PlatformType'
import { Manufacturer } from '@/models/Manufacturer'
import { Status } from '@/models/Status'

import {
  PlatformSerializer,
  platformWithMetaToPlatformByThrowingErrorOnMissing,
  platformWithMetaToPlatformByAddingDummyObjects
} from '@/serializers/jsonapi/PlatformSerializer'

import { IFlaskJSONAPIFilter } from '@/utils/JSONApiInterfaces'

import {
  IPaginationLoader, FilteredPaginationedLoader
} from '@/utils/PaginatedLoader'

export class PlatformApi {
  private axiosApi: AxiosInstance
  private serializer: PlatformSerializer

  constructor (axiosInstance: AxiosInstance) {
    this.axiosApi = axiosInstance
    this.serializer = new PlatformSerializer()
  }

  findById (id: string): Promise<Platform> {
    return this.axiosApi.get(id, {
      params: {
        include: 'contacts'
      }
    }).then((rawResponse) => {
      const rawData = rawResponse.data
      // As we ask the api to include all the contacts, we want to have them here
      // if they are missing => throw an error
      return platformWithMetaToPlatformByThrowingErrorOnMissing(this.serializer.convertJsonApiObjectToModel(rawData))
    })
  }

  deleteById (id: string): Promise<void> {
    return this.axiosApi.delete<string, void>(id)
  }

  save (platform: Platform): Promise<Platform> {
    const data: any = this.serializer.convertModelToJsonApiData(platform)
    let method: Method = 'patch'
    let url = ''

    if (platform.id === null) {
      // new -> post
      method = 'post'
    } else {
      // old -> patch
      url = String(platform.id)
    }

    // TODO: links for contacts
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

  newSearchBuilder (): PlatformSearchBuilder {
    return new PlatformSearchBuilder(this.axiosApi, this.serializer)
  }
}

export class PlatformSearchBuilder {
  private axiosApi: AxiosInstance
  private clientSideFilterFunc: (platform: Platform) => boolean
  private serverSideFilterSettings: IFlaskJSONAPIFilter[] = []
  private esTextFilter: string | null = null
  private serializer: PlatformSerializer

  constructor (axiosApi: AxiosInstance, serializer: PlatformSerializer) {
    this.axiosApi = axiosApi
    this.serializer = serializer
    this.clientSideFilterFunc = (_p: Platform) => true
  }

  withTextInName (text: string | null) : PlatformSearchBuilder {
    if (text) {
      this.esTextFilter = text
    }
    return this
  }

  withOneMatchingManufacturerOf (manufacturers: Manufacturer[]): PlatformSearchBuilder {
    if (manufacturers.length > 0) {
      this.serverSideFilterSettings.push({
        or: [
          {
            name: 'manufacturer_name',
            op: 'in_',
            val: manufacturers.map((m: Manufacturer) => m.name)
          },
          {
            name: 'manufacturer_uri',
            op: 'in_',
            val: manufacturers.map((m: Manufacturer) => m.uri)
          }
        ]
      })
    }
    return this
  }

  withOneMatchingStatusOf (states: Status[]): PlatformSearchBuilder {
    if (states.length > 0) {
      this.serverSideFilterSettings.push({
        or: [
          {
            name: 'status_name',
            op: 'in_',
            val: states.map((s: Status) => s.name)
          },
          {
            name: 'status_uri',
            op: 'in_',
            val: states.map((s: Status) => s.uri)
          }
        ]
      })
    }
    return this
  }

  withOneMatchingPlatformTypeOf (types: PlatformType[]): PlatformSearchBuilder {
    if (types.length > 0) {
      this.serverSideFilterSettings.push({
        or: [
          {
            name: 'platform_type_name',
            op: 'in_',
            val: types.map((t: PlatformType) => t.name)
          },
          {
            name: 'platform_type_uri',
            op: 'in_',
            val: types.map((t: PlatformType) => t.uri)
          }
        ]
      })
    }
    return this
  }

  build (): PlatformSearcher {
    return new PlatformSearcher(
      this.axiosApi,
      this.clientSideFilterFunc,
      this.serverSideFilterSettings,
      this.esTextFilter,
      this.serializer
    )
  }
}

export class PlatformSearcher {
  private axiosApi: AxiosInstance
  private clientSideFilterFunc: (platform: Platform) => boolean
  private serverSideFilterSettings: IFlaskJSONAPIFilter[]
  private esTextFilter: string | null
  private serializer: PlatformSerializer

  constructor (
    axiosApi: AxiosInstance,
    clientSideFilterFunc: (platform: Platform) => boolean,
    serverSideFilterSetting: IFlaskJSONAPIFilter[],
    esTextFilter: string | null,
    serializer: PlatformSerializer
  ) {
    this.axiosApi = axiosApi
    this.clientSideFilterFunc = clientSideFilterFunc
    this.serverSideFilterSettings = serverSideFilterSetting
    this.esTextFilter = esTextFilter
    this.serializer = serializer
  }

  private get commonParams (): any {
    const result: any = {
      filter: JSON.stringify(this.serverSideFilterSettings)
    }
    if (this.esTextFilter) {
      result.q = this.esTextFilter
    } else {
      result.sort = 'short_name'
    }
    return result
  }

  findMatchingAsList (): Promise<Platform[]> {
    return this.axiosApi.get(
      '',
      {
        params: {
          'page[size]': 10000,
          ...this.commonParams
        }
      }
    ).then((rawResponse: any) => {
      const rawData = rawResponse.data
      // We don't ask the api to include the contacts, so we add dummy objects.
      // This way we at least stay with the relationships.
      return this.serializer
        .convertJsonApiObjectListToModelList(rawData)
        .map(platformWithMetaToPlatformByAddingDummyObjects)
    })
  }

  findMatchingAsPaginationLoader (pageSize: number): Promise<IPaginationLoader<Platform>> {
    const loaderPromise: Promise<IPaginationLoader<Platform>> = this.findAllOnPage(1, pageSize)
    return loaderPromise.then((loader) => {
      return new FilteredPaginationedLoader<Platform>(loader, this.clientSideFilterFunc)
    })
  }

  private findAllOnPage (page: number, pageSize: number): Promise<IPaginationLoader<Platform>> {
    return this.axiosApi.get(
      '',
      {
        params: {
          'page[size]': pageSize,
          'page[number]': page,
          ...this.commonParams
        }
      }
    ).then((rawResponse) => {
      const rawData = rawResponse.data
      // client side filtering will not be done here
      // (but in the FilteredPaginationedLoader)
      // so that we know if we still have elements here
      // there may be others to load as well

      // And - again - as we don't ask the api to include the contacts, we just handle
      // the missing contact data by adding dummy objects for those.
      const elements: Platform[] = this.serializer
        .convertJsonApiObjectListToModelList(rawData)
        .map(platformWithMetaToPlatformByAddingDummyObjects)

      // This is given by the json api. Regardless of the pagination it
      // represents the total amount of entries found.
      const totalCount = rawData.meta.count

      let funToLoadNext = null
      if (elements.length > 0) {
        funToLoadNext = () => this.findAllOnPage(page + 1, pageSize)
      }

      return {
        elements,
        totalCount,
        funToLoadNext
      }
    })
  }
}
