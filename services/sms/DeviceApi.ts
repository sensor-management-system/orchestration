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
import { DeviceCalibrationAction } from '@/models/DeviceCalibrationAction'
import { DeviceProperty } from '@/models/DeviceProperty'
import { DeviceType } from '@/models/DeviceType'
import { Manufacturer } from '@/models/Manufacturer'
import { Status } from '@/models/Status'
import { GenericAction } from '@/models/GenericAction'
import { SoftwareUpdateAction } from '@/models/SoftwareUpdateAction'
import { PermissionGroup } from '@/models/PermissionGroup'

import { DeviceMountAction } from '@/models/views/devices/actions/DeviceMountAction'
import { DeviceUnmountAction } from '@/models/views/devices/actions/DeviceUnmountAction'

import { ContactSerializer } from '@/serializers/jsonapi/ContactSerializer'
import { CustomTextFieldSerializer } from '@/serializers/jsonapi/CustomTextFieldSerializer'
import { DeviceAttachmentSerializer } from '@/serializers/jsonapi/DeviceAttachmentSerializer'
import { DevicePropertySerializer } from '@/serializers/jsonapi/DevicePropertySerializer'
import { GenericDeviceActionSerializer } from '@/serializers/jsonapi/GenericActionSerializer'
import { DeviceSoftwareUpdateActionSerializer } from '@/serializers/jsonapi/SoftwareUpdateActionSerializer'

import { DeviceMountActionSerializer } from '@/serializers/jsonapi/composed/devices/actions/DeviceMountActionSerializer'
import { DeviceUnmountActionSerializer } from '@/serializers/jsonapi/composed/devices/actions/DeviceUnmountActionSerializer'

import {
  DeviceSerializer,
  deviceWithMetaToDeviceByAddingDummyObjects,
  deviceWithMetaToDeviceThrowingNoErrorOnMissing
} from '@/serializers/jsonapi/DeviceSerializer'
import { DeviceCalibrationActionSerializer } from '@/serializers/jsonapi/DeviceCalibrationActionSerializer'

export interface IncludedRelationships {
  includeContacts?: boolean
  includeCustomFields?: boolean
  includeDeviceProperties?: boolean
  includeDeviceAttachments?: boolean
  includeCreatedBy?: boolean
  includeUpdatedBy?: boolean
}

function getIncludeParams (includes: IncludedRelationships): string {
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
  if (includes.includeCreatedBy) {
    listIncludedRelationships.push('created_by.contact')
  }
  if (includes.includeUpdatedBy) {
    listIncludedRelationships.push('updated_by.contact')
  }
  return listIncludedRelationships.join(',')
}

export type DevicePermissionFetchFunction = () => Promise<PermissionGroup[]>

export class DeviceApi {
  private axiosApi: AxiosInstance
  readonly basePath: string
  private serializer: DeviceSerializer
  private permissionFetcher: DevicePermissionFetchFunction | undefined

  private _searchedManufacturers: Manufacturer[] = []
  private _searchedStates: Status[] = []
  private _searchedDeviceTypes: DeviceType[] = []
  private _searchedUserMail: string | null = null
  private _searchText: string | null = null
  private filterSettings: any[] = []

  constructor (axiosInstance: AxiosInstance, basePath: string, permissionFetcher?: DevicePermissionFetchFunction) {
    this.axiosApi = axiosInstance
    this.basePath = basePath
    this.serializer = new DeviceSerializer()
    if (permissionFetcher) {
      this.permissionFetcher = permissionFetcher
    }
  }

  get searchedManufacturers (): Manufacturer[] {
    return this._searchedManufacturers
  }

  setSearchedManufacturers (value: Manufacturer[]) {
    this._searchedManufacturers = value
    return this
  }

  get searchedStates (): Status[] {
    return this._searchedStates
  }

  setSearchedStates (value: Status[]) {
    this._searchedStates = value
    return this
  }

  get searchedDeviceTypes (): DeviceType[] {
    return this._searchedDeviceTypes
  }

  setSearchedDeviceTypes (value: DeviceType[]) {
    this._searchedDeviceTypes = value
    return this
  }

  get searchedUserMail (): string | null {
    return this._searchedUserMail
  }

  setSearchedUserMail (value: string | null) {
    this._searchedUserMail = value
    return this
  }

  get searchText (): string | null {
    return this._searchText
  }

  setSearchText (value: string | null) {
    this._searchText = value
    return this
  }

  private get commonParams (): any {
    const result: any = {
      filter: JSON.stringify(this.filterSettings)
    }
    if (this.searchText) {
      result.q = this.searchText
    }
    result.sort = 'short_name'
    return result
  }

  async searchPaginated (pageNumber: number, pageSize: number, includes: IncludedRelationships = {}) {
    this.prepareSearch()
    // set the permission groups for the serializer
    if (this.permissionFetcher) {
      this.serializer.permissionGroups = await this.permissionFetcher()
    }

    const include = getIncludeParams(includes)

    return this.axiosApi.get(
      this.basePath,
      {
        params: {
          'page[size]': pageSize,
          'page[number]': pageNumber,
          include,
          ...this.commonParams
        }
      }
    ).then((rawResponse) => {
      const rawData = rawResponse.data
      // And - again - we don't ask the api here to load the contact data as well
      // so we will add the dummy objects to stay with the relationships
      const elements: Device[] = this.serializer.convertJsonApiObjectListToModelList(
        rawData
      ).map(deviceWithMetaToDeviceByAddingDummyObjects)

      const totalCount = rawData.meta.count

      return {
        elements,
        totalCount
      }
    })
  }

  async searchAll () {
    this.prepareSearch()
    // set the permission groups for the serializer
    if (this.permissionFetcher) {
      this.serializer.permissionGroups = await this.permissionFetcher()
    }
    return this.axiosApi.get(
      this.basePath,
      {
        params: {
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

  searchMatchingAsCsvBlob (): Promise<Blob> {
    this.prepareSearch()

    const url = this.basePath
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

  prepareSearch () {
    this.resetFilterSetting()
    this.prepareManufacturers()
    this.prepareStates()
    this.prepareTypes()
    this.prepareMail()
  }

  prepareMail () {
    if (this.searchedUserMail) {
      this.filterSettings.push({
        name: 'contacts.email',
        op: 'eq',
        val: this.searchedUserMail
      })
    }
  }

  resetFilterSetting () {
    this.filterSettings = []
  }

  prepareManufacturers () {
    if (this.searchedManufacturers.length > 0) {
      this.filterSettings.push({
        or: [
          {
            name: 'manufacturer_name',
            op: 'in_',
            val: this.searchedManufacturers.map((m: Manufacturer) => m.name)
          },
          {
            name: 'manufacturer_uri',
            op: 'in_',
            val: this.searchedManufacturers.map((m: Manufacturer) => m.uri)
          }
        ]
      })
    }
  }

  prepareStates () {
    if (this.searchedStates.length > 0) {
      this.filterSettings.push({
        or: [
          {
            name: 'status_name',
            op: 'in_',
            val: this.searchedStates.map((s: Status) => s.name)
          },
          {
            name: 'status_uri',
            op: 'in_',
            val: this.searchedStates.map((s: Status) => s.uri)
          }
        ]
      })
    }
  }

  prepareTypes () {
    if (this.searchedDeviceTypes.length > 0) {
      this.filterSettings.push({
        or: [
          {
            name: 'device_type_name',
            op: 'in_',
            val: this.searchedDeviceTypes.map((t: DeviceType) => t.name)
          },
          {
            name: 'device_type_uri',
            op: 'in_',
            val: this.searchedDeviceTypes.map((t: DeviceType) => t.uri)
          }
        ]
      })
    }
  }

  async findById (id: string, includes: IncludedRelationships = {}): Promise<Device> {
    const include = getIncludeParams(includes)
    // set the permission groups for the serializer
    if (this.permissionFetcher) {
      this.serializer.permissionGroups = await this.permissionFetcher()
    }

    const rawResponse = await this.axiosApi.get(
      this.basePath + '/' + id,
      {
        params: {
          include
        }
      }
    )
    const rawData = rawResponse.data
    return deviceWithMetaToDeviceThrowingNoErrorOnMissing(
      this.serializer.convertJsonApiObjectToModel(rawData)
    )
  }

  deleteById (id: string): Promise<void> {
    return this.axiosApi.delete<string, void>(this.basePath + '/' + id)
  }

  save (device: Device) {
    // The relationships themselves will be added, updated & deleted in their
    // own tabs and in their own services.
    // If we would include them here (without fetching them before), we would
    // delete them. So we will skip them in order to keep them in the backend.
    const includeRelationships = false
    const data: any = this.serializer.convertModelToJsonApiData(device, includeRelationships)
    let method: Method = 'patch'
    let url = this.basePath

    if (device.id === null) {
      // new -> post
      method = 'post'
    } else {
      // old -> patch
      url += '/' + String(device.id)
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

  // newSearchBuilder (): DeviceSearchBuilder {
  //   return new DeviceSearchBuilder(this.axiosApi, this.basePath, this.serializer)
  // }

  findRelatedContacts (deviceId: string): Promise<Contact[]> {
    const url = this.basePath + '/' + deviceId + '/contacts'
    const params = {
      'page[size]': 10000
    }
    return this.axiosApi.get(url, { params }).then((rawServerResponse) => {
      return new ContactSerializer().convertJsonApiObjectListToModelList(rawServerResponse.data)
    })
  }

  removeContact (deviceId: string, contactId: string): Promise<void> {
    const url = this.basePath + '/' + deviceId + '/relationships/contacts'
    const params = {
      data: [{
        type: 'contact',
        id: contactId
      }]
    }
    return this.axiosApi.delete(url, { data: params })
  }

  addContact (deviceId: string, contactId: string): Promise<void> {
    const url = this.basePath + '/' + deviceId + '/relationships/contacts'
    const data = [{
      type: 'contact',
      id: contactId
    }]
    return this.axiosApi.post(url, { data })
  }

  findRelatedCustomFields (deviceId: string): Promise<CustomTextField[]> {
    const url = this.basePath + '/' + deviceId + '/customfields'
    const params = {
      'page[size]': 10000
    }
    return this.axiosApi.get(url, { params }).then((rawServerResponse) => {
      return new CustomTextFieldSerializer().convertJsonApiObjectListToModelList(rawServerResponse.data)
    })
  }

  findRelatedDeviceAttachments (deviceId: string): Promise<Attachment[]> {
    const url = this.basePath + '/' + deviceId + '/device-attachments'
    const params = {
      'page[size]': 10000
    }
    return this.axiosApi.get(url, { params }).then((rawServerResponse) => {
      return new DeviceAttachmentSerializer().convertJsonApiObjectListToModelList(rawServerResponse.data)
    })
  }

  findRelatedDeviceProperties (deviceId: string): Promise<DeviceProperty[]> {
    const url = this.basePath + '/' + deviceId + '/device-properties'
    const params = {
      'page[size]': 10000
    }
    return this.axiosApi.get(url, { params }).then((rawServerResponse) => {
      return new DevicePropertySerializer().convertJsonApiObjectListToModelList(rawServerResponse.data)
    })
  }

  findRelatedGenericActions (deviceId: string): Promise<GenericAction[]> {
    const url = this.basePath + '/' + deviceId + '/generic-device-actions'
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

  findRelatedSoftwareUpdateActions (deviceId: string): Promise<SoftwareUpdateAction[]> {
    const url = this.basePath + '/' + deviceId + '/device-software-update-actions'
    const params = {
      'page[size]': 10000,
      include: [
        'contact',
        'device_software_update_action_attachments.attachment'
      ].join(',')
    }
    return this.axiosApi.get(url, { params }).then((rawServerResponse) => {
      return new DeviceSoftwareUpdateActionSerializer().convertJsonApiObjectListToModelList(rawServerResponse.data)
    })
  }

  findRelatedCalibrationActions (deviceId: string): Promise<DeviceCalibrationAction[]> {
    const url = this.basePath + '/' + deviceId + '/device-calibration-actions'
    const params = {
      'page[size]': 10000,
      include: [
        'contact',
        'device_calibration_attachments.attachment',
        'device_property_calibrations',
        'device_property_calibrations.device_property'
      ].join(',')
    }
    return this.axiosApi.get(url, { params }).then((rawServerResponse) => {
      return new DeviceCalibrationActionSerializer().convertJsonApiObjectListToModelList(rawServerResponse.data)
    })
  }

  findRelatedMountActions (deviceId: string): Promise<DeviceMountAction[]> {
    const url = this.basePath + '/' + deviceId + '/device-mount-actions'
    const params = {
      'page[size]': 10000,
      include: [
        'contact',
        'parent_platform',
        'configuration'
      ].join(',')
    }
    return this.axiosApi.get(url, { params }).then((rawServerResponse) => {
      return new DeviceMountActionSerializer().convertJsonApiObjectListToModelList(rawServerResponse.data)
    })
  }

  findRelatedUnmountActions (deviceId: string): Promise<DeviceUnmountAction[]> {
    const url = this.basePath + '/' + deviceId + '/device-unmount-actions'
    const params = {
      'page[size]': 10000,
      include: [
        'contact',
        'configuration'
      ].join(',')
    }
    return this.axiosApi.get(url, { params }).then((rawServerResponse) => {
      return new DeviceUnmountActionSerializer().convertJsonApiObjectListToModelList(rawServerResponse.data)
    })
  }
}
//
// export class DeviceSearchBuilder {
//   private axiosApi: AxiosInstance
//   readonly basePath: string
//   private clientSideFilterFunc: (device: Device) => boolean
//   private serverSideFilterSettings: IFlaskJSONAPIFilter[] = []
//   private esTextFilter: string | null = null
//   private serializer: DeviceSerializer
//
//   constructor (axiosApi: AxiosInstance, basePath: string, serializer: DeviceSerializer) {
//     this.axiosApi = axiosApi
//     this.basePath = basePath
//     this.clientSideFilterFunc = (_d: Device) => true
//     this.serializer = serializer
//   }
//
//   withText (text: string | null) {
//     if (text) {
//       this.esTextFilter = text
//     }
//     return this
//   }
//
//   withOneMachtingManufacturerOf (manufacturers: Manufacturer[]) {
//     if (manufacturers.length > 0) {
//       this.serverSideFilterSettings.push({
//         or: [
//           {
//             name: 'manufacturer_name',
//             op: 'in_',
//             val: manufacturers.map((m: Manufacturer) => m.name)
//           },
//           {
//             name: 'manufacturer_uri',
//             op: 'in_',
//             val: manufacturers.map((m: Manufacturer) => m.uri)
//           }
//         ]
//       })
//     }
//     return this
//   }
//
//   withOneMatchingStatusOf (states: Status[]) {
//     if (states.length > 0) {
//       this.serverSideFilterSettings.push({
//         or: [
//           {
//             name: 'status_name',
//             op: 'in_',
//             val: states.map((s: Status) => s.name)
//           },
//           {
//             name: 'status_uri',
//             op: 'in_',
//             val: states.map((s: Status) => s.uri)
//           }
//         ]
//       })
//     }
//     return this
//   }
//
//   withOneMatchingDeviceTypeOf (types: DeviceType[]) {
//     if (types.length > 0) {
//       this.serverSideFilterSettings.push({
//         or: [
//           {
//             name: 'device_type_name',
//             op: 'in_',
//             val: types.map((t: DeviceType) => t.name)
//           },
//           {
//             name: 'device_type_uri',
//             op: 'in_',
//             val: types.map((t: DeviceType) => t.uri)
//           }
//         ]
//       })
//     }
//     return this
//   }
//
//   withContactEmail (email: string) {
//     this.serverSideFilterSettings.push({
//       name: 'contacts.email',
//       op: 'eq',
//       val: email
//     })
//     return this
//   }
//
//   build (): DeviceSearcher {
//     return new DeviceSearcher(
//       this.axiosApi,
//       this.basePath,
//       this.clientSideFilterFunc,
//       this.serverSideFilterSettings,
//       this.esTextFilter,
//       this.serializer
//     )
//   }
// }
//
// export class DeviceSearcher {
//   private axiosApi: AxiosInstance
//   readonly basePath: string
//   private clientSideFilterFunc: (device: Device) => boolean
//   private serverSideFilterSettings: IFlaskJSONAPIFilter[]
//   private esTextFilter: string | null
//   private serializer: DeviceSerializer
//
//   constructor (
//     axiosApi: AxiosInstance,
//     basePath: string,
//     clientSideFilterFunc: (device: Device) => boolean,
//     serverSideFilterSettings: IFlaskJSONAPIFilter[],
//     esTextFilter: string | null,
//     serializer: DeviceSerializer
//   ) {
//     this.axiosApi = axiosApi
//     this.basePath = basePath
//     this.clientSideFilterFunc = clientSideFilterFunc
//     this.serverSideFilterSettings = serverSideFilterSettings
//     this.esTextFilter = esTextFilter
//     this.serializer = serializer
//   }
//
//   private get commonParams (): any {
//     const result: any = {
//       filter: JSON.stringify(this.serverSideFilterSettings)
//     }
//     if (this.esTextFilter) {
//       result.q = this.esTextFilter
//     } else {
//       result.sort = 'short_name'
//     }
//     return result
//   }
//
//   findMatchingAsCsvBlob (): Promise<Blob> {
//     const url = this.basePath
//     return this.axiosApi.request({
//       url,
//       method: 'get',
//       headers: {
//         accept: 'text/csv'
//       },
//       params: {
//         'page[size]': 10000,
//         ...this.commonParams
//       }
//     }).then((response) => {
//       return new Blob([response.data], { type: 'text/csv;charset=utf-8' })
//     })
//   }
//
//   findMatchingAsList (): Promise<Device[]> {
//     return this.axiosApi.get(
//       this.basePath,
//       {
//         params: {
//           'page[size]': 10000,
//           ...this.commonParams
//         }
//       }
//     ).then((rawResponse: any) => {
//       const rawData = rawResponse.data
//       // We don't ask the api to load the contacts, so we just add dummy objects
//       // to stay with the relationships
//       return this.serializer
//         .convertJsonApiObjectListToModelList(rawData)
//         .map(deviceWithMetaToDeviceByAddingDummyObjects)
//     })
//   }
//
//   findMatchingAsPaginationLoaderOnPage (page: number, pageSize: number): Promise<IPaginationLoader<Device>> {
//     return this.findAllOnPage(page, pageSize)
//   }
//
//   private findAllOnPage (page: number, pageSize: number): Promise<IPaginationLoader<Device>> {
//     return this.axiosApi.get(
//       this.basePath,
//       {
//         params: {
//           'page[size]': pageSize,
//           'page[number]': page,
//           ...this.commonParams
//         }
//       }
//     ).then((rawResponse) => {
//       const rawData = rawResponse.data
//       // And - again - we don't ask the api here to load the contact data as well
//       // so we will add the dummy objects to stay with the relationships
//       const elements: Device[] = this.serializer.convertJsonApiObjectListToModelList(
//         rawData
//       ).map(deviceWithMetaToDeviceByAddingDummyObjects)
//
//       const totalCount = rawData.meta.count
//
//       // check if the provided page param is valid
//       if (totalCount > 0 && elements.length === 0) {
//         throw new RangeError('page is out of bounds')
//       }
//
//       let funToLoadNext = null
//       if (elements.length > 0) {
//         funToLoadNext = () => this.findAllOnPage(page + 1, pageSize)
//       }
//
//       let funToLoadPage = null
//       if (elements.length > 0) {
//         funToLoadPage = (pageNr: number) => this.findAllOnPage(pageNr, pageSize)
//       }
//
//       return {
//         elements,
//         totalCount,
//         page: elements.length ? page : 0,
//         funToLoadNext,
//         funToLoadPage
//       }
//     })
//   }
// }
