/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020, 2021
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

import { Attachment } from '@/models/Attachment'
import { Contact } from '@/models/Contact'
import { CustomTextField } from '@/models/CustomTextField'
import { Device } from '@/models/Device'
import { DeviceProperty } from '@/models/DeviceProperty'
import { DeviceType } from '@/models/DeviceType'
import { Manufacturer } from '@/models/Manufacturer'
import { Status } from '@/models/Status'
import { GenericAction } from '@/models/GenericAction'

import { ContactSerializer } from '@/serializers/jsonapi/ContactSerializer'
import { CustomTextFieldSerializer } from '@/serializers/jsonapi/CustomTextFieldSerializer'
import { DeviceAttachmentSerializer } from '@/serializers/jsonapi/DeviceAttachmentSerializer'
import { DevicePropertySerializer } from '@/serializers/jsonapi/DevicePropertySerializer'
import { GenericDeviceActionSerializer } from '@/serializers/jsonapi/GenericActionSerializer'

import { IFlaskJSONAPIFilter } from '@/utils/JSONApiInterfaces'

import { FilteredPaginationedLoader, IPaginationLoader } from '@/utils/PaginatedLoader'
import {
  DeviceSerializer,
  deviceWithMetaToDeviceByAddingDummyObjects,
  deviceWithMetaToDeviceThrowingNoErrorOnMissing
} from '@/serializers/jsonapi/DeviceSerializer'

interface IncludedRelationships {
  includeContacts?: boolean
  includeCustomFields?: boolean
  includeDeviceProperties?: boolean
  includeDeviceAttachments?: boolean
}

export class DeviceApi {
  private axiosApi: AxiosInstance
  private serializer: DeviceSerializer

  constructor (axiosInstance: AxiosInstance) {
    this.axiosApi = axiosInstance
    this.serializer = new DeviceSerializer()
  }

  findById (id: string, includes: IncludedRelationships): Promise<Device> {
    const listIncludedRelationships: string[] = []
    if (includes.includeContacts) {
      listIncludedRelationships.push('contacts')
    }
    if (includes.includeDeviceProperties) {
      listIncludedRelationships.push('device_properties')
    }
    if (includes.includeCustomFields) {
      listIncludedRelationships.push('customfields')
    }
    if (includes.includeDeviceAttachments) {
      listIncludedRelationships.push('device_attachments')
    }
    const include = listIncludedRelationships.join(',')

    return this.axiosApi.get(id, {
      params: {
        include
      }
    }).then((rawResponse) => {
      const rawData = rawResponse.data
      return deviceWithMetaToDeviceThrowingNoErrorOnMissing(
        this.serializer.convertJsonApiObjectToModel(rawData))
    })
  }

  deleteById (id: string): Promise<void> {
    return this.axiosApi.delete<string, void>(id)
  }

  save (device: Device) {
    // The relationships themselves will be added, updated & deleted in their
    // own tabs and in their own services.
    // If we would include them here (without fetching them before), we would
    // delete them. So we will skip them in order to keep them in the backend.
    const includeRelationships = false
    const data: any = this.serializer.convertModelToJsonApiData(device, includeRelationships)
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
      const answerData = serverAnswer.data
      return deviceWithMetaToDeviceThrowingNoErrorOnMissing(
        this.serializer.convertJsonApiObjectToModel(answerData))
    })
  }

  newSearchBuilder (): DeviceSearchBuilder {
    return new DeviceSearchBuilder(this.axiosApi, this.serializer)
  }

  findRelatedContacts (deviceId: string): Promise<Contact[]> {
    const url = deviceId + '/contacts'
    const params = {
      'page[size]': 10000
    }
    return this.axiosApi.get(url, { params }).then((rawServerResponse) => {
      return new ContactSerializer().convertJsonApiObjectListToModelList(rawServerResponse.data)
    })
  }

  removeContact (deviceId: string, contactId: string): Promise<void> {
    const url = deviceId + '/relationships/contacts'
    const params = {
      data: [{
        type: 'contact',
        id: contactId
      }]
    }
    return this.axiosApi.delete(url, { data: params })
  }

  addContact (deviceId: string, contactId: string): Promise<void> {
    const url = deviceId + '/relationships/contacts'
    const data = [{
      type: 'contact',
      id: contactId
    }]
    return this.axiosApi.post(url, { data })
  }

  findRelatedCustomFields (deviceId: string): Promise<CustomTextField[]> {
    const url = deviceId + '/customfields'
    const params = {
      'page[size]': 10000
    }
    return this.axiosApi.get(url, { params }).then((rawServerResponse) => {
      return new CustomTextFieldSerializer().convertJsonApiObjectListToModelList(rawServerResponse.data)
    })
  }

  findRelatedDeviceAttachments (deviceId: string): Promise<Attachment[]> {
    const url = deviceId + '/device-attachments'
    const params = {
      'page[size]': 10000
    }
    return this.axiosApi.get(url, { params }).then((rawServerResponse) => {
      return new DeviceAttachmentSerializer().convertJsonApiObjectListToModelList(rawServerResponse.data)
    })
  }

  findRelatedDeviceProperties (deviceId: string): Promise<DeviceProperty[]> {
    const url = deviceId + '/device-properties'
    const params = {
      'page[size]': 10000
    }
    return this.axiosApi.get(url, { params }).then((rawServerResponse) => {
      return new DevicePropertySerializer().convertJsonApiObjectListToModelList(rawServerResponse.data)
    })
  }

  findRelatedGenericActions (deviceId: string): Promise<GenericAction[]> {
    const url = deviceId + '/generic-device-actions'
    const params = {
      'page[size]': 10000,
      include: [
        'contact',
        'generic_device_action_attachments.attachment'
      ].join(',')
    }
    return this.axiosApi.get(url, { params }).then((rawServerResponse) => {
      return new GenericDeviceActionSerializer().convertJsonApiObjectListToModelList(rawServerResponse.data)
    })
  }
}

export class DeviceSearchBuilder {
  private axiosApi: AxiosInstance
  private clientSideFilterFunc: (device: Device) => boolean
  private serverSideFilterSettings: IFlaskJSONAPIFilter[] = []
  private esTextFilter: string | null = null
  private serializer: DeviceSerializer

  constructor (axiosApi: AxiosInstance, serializer: DeviceSerializer) {
    this.axiosApi = axiosApi
    this.clientSideFilterFunc = (_d: Device) => true
    this.serializer = serializer
  }

  withText (text: string | null) {
    if (text) {
      this.esTextFilter = text
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
      this.esTextFilter,
      this.serializer
    )
  }
}

export class DeviceSearcher {
  private axiosApi: AxiosInstance
  private clientSideFilterFunc: (device: Device) => boolean
  private serverSideFilterSettings: IFlaskJSONAPIFilter[]
  private esTextFilter: string | null
  private serializer: DeviceSerializer

  constructor (
    axiosApi: AxiosInstance,
    clientSideFilterFunc: (device: Device) => boolean,
    serverSideFilterSettings: IFlaskJSONAPIFilter[],
    esTextFilter: string | null,
    serializer: DeviceSerializer
  ) {
    this.axiosApi = axiosApi
    this.clientSideFilterFunc = clientSideFilterFunc
    this.serverSideFilterSettings = serverSideFilterSettings
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

  findMatchingAsCsvBlob (): Promise<Blob> {
    const url = ''
    return this.axiosApi.request({
      url,
      method: 'get',
      headers: {
        accept: 'text/csv'
      },
      params: {
        'page[size]': 10000,
        ...this.commonParams
      }
    }).then((response) => {
      return new Blob([response.data], { type: 'text/csv;charset=utf-8' })
    })
  }

  findMatchingAsList (): Promise<Device[]> {
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
