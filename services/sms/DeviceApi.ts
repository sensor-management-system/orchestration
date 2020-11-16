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

import { Device } from '@/models/Device'
import { DeviceType } from '@/models/DeviceType'
import { Manufacturer } from '@/models/Manufacturer'
import { Status } from '@/models/Status'

import { IFlaskJSONAPIFilter } from '@/utils/JSONApiInterfaces'

import {
  IPaginationLoader, FilteredPaginationedLoader
} from '@/utils/PaginatedLoader'
import {
  DeviceSerializer,
  deviceWithMetaToDeviceByThrowingErrorOnMissing,
  deviceWithMetaToDeviceByAddingDummyObjects
} from '@/serializers/jsonapi/DeviceSerializer'

export class DeviceApi {
  private axiosApi: AxiosInstance
  private serializer: DeviceSerializer

  constructor (axiosInstance: AxiosInstance) {
    this.axiosApi = axiosInstance
    this.serializer = new DeviceSerializer()
  }

  findById (id: string): Promise<Device> {
    return this.axiosApi.get(id, {
      params: {
        include: 'contacts'
      }
    }).then((rawResponse) => {
      const rawData = rawResponse.data
      // as we load the contacts, we want them to be included
      // otherwise we throw an Error
      return deviceWithMetaToDeviceByThrowingErrorOnMissing(this.serializer.convertJsonApiObjectToModel(rawData))
    })
  }

  deleteById (id: string) : Promise<void> {
    return this.axiosApi.delete<string, void>(id)
  }

  save (device: Device) {
    const data: any = this.serializer.convertModelToJsonApiData(device)
    let method: Method = 'patch'
    let url = ''

    if (device.id === null) {
      // new -> post
      method = 'post'
    } else {
      // old -> patch
      url = String(device.id)
    }

    return this.axiosApi.request({
      url,
      method,
      data: {
        data
      }
    }).then((serverAnswer) => {
      // the server answer doesn't include the contacts
      // so we will reload from the database
      return this.findById(serverAnswer.data.data.id)
    })
  }

  newSearchBuilder (): DeviceSearchBuilder {
    return new DeviceSearchBuilder(this.axiosApi, this.serializer)
  }
}

export class DeviceSearchBuilder {
  private axiosApi: AxiosInstance
  private clientSideFilterFunc: (device: Device) => boolean
  private serverSideFilterSettings: IFlaskJSONAPIFilter[] = []
  private serializer: DeviceSerializer

  constructor (axiosApi: AxiosInstance, serializer: DeviceSerializer) {
    this.axiosApi = axiosApi
    this.clientSideFilterFunc = (_d: Device) => true
    this.serializer = serializer
  }

  withTextInName (text: string | null) {
    if (text) {
      const ilikeValue = '%' + text + '%'
      const fieldsToSearchIn = [
        'short_name',
        'long_name'
        // here we can add description
        // as well
        // --> if so, also change the method name here
      ]

      const filter: IFlaskJSONAPIFilter[] = []
      for (const field of fieldsToSearchIn) {
        filter.push({
          name: field,
          op: 'ilike',
          val: ilikeValue
        })
      }

      this.serverSideFilterSettings.push({
        or: filter
      })
    }
    return this
  }

  withOneMachtingManufacturerOf (manufacturers: Manufacturer[]) {
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

  withOneMatchingStatusOf (states: Status[]) {
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

  withOneMatchingDeviceTypeOf (types: DeviceType[]) {
    if (types.length > 0) {
      this.serverSideFilterSettings.push({
        or: [
          {
            name: 'device_type_name',
            op: 'in_',
            val: types.map((t: DeviceType) => t.name)
          },
          {
            name: 'device_type_uri',
            op: 'in_',
            val: types.map((t: DeviceType) => t.uri)
          }
        ]
      })
    }
    return this
  }

  build (): DeviceSearcher {
    return new DeviceSearcher(
      this.axiosApi,
      this.clientSideFilterFunc,
      this.serverSideFilterSettings,
      this.serializer
    )
  }
}

export class DeviceSearcher {
  private axiosApi: AxiosInstance
  private clientSideFilterFunc: (device: Device) => boolean
  private serverSideFilterSettings: IFlaskJSONAPIFilter[]
  private serializer: DeviceSerializer

  constructor (
    axiosApi: AxiosInstance,
    clientSideFilterFunc: (device: Device) => boolean,
    serverSideFilterSettings: IFlaskJSONAPIFilter[],
    serializer: DeviceSerializer
  ) {
    this.axiosApi = axiosApi
    this.clientSideFilterFunc = clientSideFilterFunc
    this.serverSideFilterSettings = serverSideFilterSettings
    this.serializer = serializer
  }

  private get commonParams (): any {
    return {
      filter: JSON.stringify(this.serverSideFilterSettings),
      sort: 'short_name'
    }
  }

  findMatchingAsList (): Promise<Device[]> {
    return this.axiosApi.get(
      '',
      {
        params: {
          'page[size]': 100000,
          ...this.commonParams
        }
      }
    ).then((rawResponse: any) => {
      const rawData = rawResponse.data
      // We don't ask the api to load the contacts, so we just add dummy objects
      // to stay with the relationships
      return this.serializer
        .convertJsonApiObjectListToModelList(rawData)
        .map(deviceWithMetaToDeviceByAddingDummyObjects)
    })
  }

  findMatchingAsPaginationLoader (pageSize: number): Promise<IPaginationLoader<Device>> {
    const loaderPromise: Promise<IPaginationLoader<Device>> = this.findAllOnPage(1, pageSize)
    return loaderPromise.then((loader) => {
      return new FilteredPaginationedLoader<Device>(loader, this.clientSideFilterFunc)
    })
  }

  private findAllOnPage (page: number, pageSize: number): Promise<IPaginationLoader<Device>> {
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

      // And - again - we don't ask the api here to load the contact data as well
      // so we will add the dummy objects to stay with the relationships
      const elements: Device[] = this.serializer.convertJsonApiObjectListToModelList(
        rawData
      ).map(deviceWithMetaToDeviceByAddingDummyObjects)

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
