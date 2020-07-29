import axios, { AxiosInstance, Method } from 'axios'

import Device from '@/models/Device'
import DeviceType from '@/models/DeviceType'
import Manufacturer from '@/models/Manufacturer'
import Status from '@/models/Status'

import {
  IPaginationLoader, FilteredPaginationedLoader
} from '@/utils/PaginatedLoader'

// Use on version for all the queries
const BASE_URL = process.env.smsBackendUrl + '/devices'

export default class DeviceApi {
  private axiosApi: AxiosInstance

  constructor (baseURL: string = BASE_URL) {
    this.axiosApi = axios.create({
      baseURL
    })
  }

  findById (id: string): Promise<Device> {
    // TODO: Think about also including the contacts
    // with ?include=contacts
    return this.axiosApi.get(id).then((rawResponse) => {
      const entry = rawResponse.data.data
      return serverResponseToEntity(entry)
    })
  }

  deleteById (id: number) : Promise<void> {
    return this.axiosApi.delete<string, void>(String(id))
  }

  save (device: Device) {
    // TODO: consistent camelCase
    const data: any = {
      type: 'device',
      attributes: {
        description: device.description,
        dual_use: device.dualUse,
        inventory_number: device.inventoryNumber,
        long_name: device.longName,
        // TODO: Change to uri after backend change
        manufacturer: device.manufacturerName,
        // TODO: Add manufacturerUri
        model: device.model,
        persistent_identifier: device.persistentIdentifier,
        serial_number: device.serialNumber,
        short_name: device.shortName,
        // TODO: Add statusName & statusUri
        url: device.website,
        type: device.deviceTypeUri

        /*
        customFields: [
          {
            key: 'key1',
            value: 'value1'
          },
          {
            key: 'key2',
            value: 'value2
          }
        ]
        */
      }

      /*
      relationships: {
        contacts: {
          data: [
            {
              type: 'contact',
              id: 1,
            },
            {
              type: 'contact',
              id: 2
            }
          ]
        }

      }
      */
    }
    let method: Method = 'patch'
    let url = ''

    if (device.id === null) {
      // new -> post
      method = 'post'
    } else {
      // old -> patch
      data.id = device.id
      url = String(device.id)
    }

    // TODO: links for contacts
    return this.axiosApi.request({
      url,
      method,
      data: {
        data
      }
    }).then((serverAnswer) => {
      return serverResponseToEntity(serverAnswer.data.data)
    })
  }

  newSearchBuilder (): DeviceSearchBuilder {
    return new DeviceSearchBuilder(this.axiosApi)
  }
}

export class DeviceSearchBuilder {
  private axiosApi: AxiosInstance
  private clientSideFilterFunc: (device: Device) => boolean

  constructor (axiosApi: AxiosInstance) {
    this.axiosApi = axiosApi
    this.clientSideFilterFunc = (_d: Device) => true
  }

  withTextInShortName (text: string | null) {
    if (text) {
      const oldFilterFunc = this.clientSideFilterFunc
      this.clientSideFilterFunc = (device: Device): boolean => {
        return oldFilterFunc(device) && (
          device.shortName.includes(text)
        )
      }
    }
    return this
  }

  withOneMachtingManufacturerOf (manufacturers: Manufacturer[]) {
    if (manufacturers.length > 0) {
      const oldFilterFunc = this.clientSideFilterFunc
      this.clientSideFilterFunc = (device: Device) : boolean => {
        return oldFilterFunc(device) && (
          manufacturers.findIndex(m => m.uri === device.manufacturerUri) > -1
        )
      }
    }
    return this
  }

  withOneMatchingStatusOf (states: Status[]) {
    if (states.length > 0) {
      const oldFilterFunc = this.clientSideFilterFunc
      this.clientSideFilterFunc = (device: Device) : boolean => {
        return oldFilterFunc(device) && (
          states.findIndex(s => s.uri === device.statusUri) > -1
        )
      }
    }
    return this
  }

  withOneMatchingDeviceTypeOf (types: DeviceType[]) {
    if (types.length > 0) {
      const oldFilterFunc = this.clientSideFilterFunc
      this.clientSideFilterFunc = (device: Device) : boolean => {
        return oldFilterFunc(device) && (
          types.findIndex(t => t.uri === device.deviceTypeUri) > -1
        )
      }
    }
    return this
  }

  build (): DeviceSearcher {
    return new DeviceSearcher(
      this.axiosApi,
      this.clientSideFilterFunc
    )
  }
}

export class DeviceSearcher {
  private axiosApi: AxiosInstance
  private clientSideFilterFunc: (device: Device) => boolean

  constructor (
    axiosApi: AxiosInstance,
    clientSideFilterFunc: (device: Device) => boolean
  ) {
    this.axiosApi = axiosApi
    this.clientSideFilterFunc = clientSideFilterFunc
  }

  findMatchingAsList (): Promise<Device[]> {
    return this.axiosApi.get(
      '',
      {
        params: {
          'page[size]': 100000
        }
      }
    ).then((rawResponse: any) => {
      const rawData = rawResponse.data
      const result: Device[] = []

      for (const entry of rawData.data) {
        const device = serverResponseToEntity(entry)
        if (this.clientSideFilterFunc(device)) {
          result.push(device)
        }
      }
      return result
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
          'page[number]': page
        }
      }
    ).then((rawResponse) => {
      const rawData = rawResponse.data
      const result: Device[] = []
      for (const entry of rawData.data) {
        // client side filtering will not be done here
        // (but in the FilteredPaginationedLoader)
        // so that we know if we still have elements here
        // there may be others to load as well
        result.push(serverResponseToEntity(entry))
      }

      let funToLoadNext = null
      if (result.length > 0) {
        funToLoadNext = () => this.findAllOnPage(page + 1, pageSize)
      }

      return {
        elements: result,
        funToLoadNext
      }
    })
  }
}

export function serverResponseToEntity (entry: any) : Device {
  const result: Device = new Device()

  const attributes = entry.attributes

  result.id = entry.id

  result.description = attributes.description || ''
  // TODO: to camelcase
  result.dualUse = attributes.dual_use || false
  result.inventoryNumber = attributes.inventory_number || ''
  result.longName = attributes.long_name || ''
  result.manufacturerName = attributes.manufacturer || ''
  // TODO: manufacturerUri
  result.model = attributes.model || ''

  result.persistentIdentifier = attributes.persistent_identifier || ''
  result.shortName = attributes.short_name || ''
  result.serialNumber = attributes.serial_number || ''
  // TODO: StatusName & StatusUri
  result.website = attributes.url || ''

  result.deviceTypeUri = attributes.type || ''
  // TODO: createdAt, modifiedAt, createdBy, modifiedBy

  // TODO: Insert those as well
  result.contacts = []
  result.properties = []
  result.customFields = []

  // TODO: Attachments
  // TODO: events

  return result
}
