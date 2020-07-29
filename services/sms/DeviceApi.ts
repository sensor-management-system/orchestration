import axios from 'axios'

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
  static serverResponseToEntity (entry: any) : Device {
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

  static deleteById (id: number) {
    return axios.delete(BASE_URL + '/' + id)
  }

  static save (device: Device) {
    let method = axios.patch
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
    let url = BASE_URL

    if (device.id === null) {
      // new -> post
      method = axios.post
    } else {
      // old -> patch
      data.id = device.id
      url = url + '/' + device.id
    }

    // TODO: links for contacts
    return method(
      url,
      {
        data
      }
    ).then((serverAnswer) => {
      return this.serverResponseToEntity(serverAnswer.data.data)
    })
  }

  static findAllOnPage (page: number, pageSize: number): Promise<IPaginationLoader<Device>> {
    const pageParameter = 'page[size]=' + pageSize + '&page[number]=' + page
    // TODO: Think about also including the contacts
    // with ?include=contacts
    // size for having one query to get all the devices (no pagination)
    return axios.get(BASE_URL + '?' + pageParameter).then((rawResonse) => {
      const rawData = rawResonse.data
      const result: Device[] = []

      for (const entry of rawData.data) {
        result.push(this.serverResponseToEntity(entry))
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

  static findById (id: string): Promise<Device> {
    // TODO: Think about also including the contacts
    // with ?include=contacts
    return axios.get(BASE_URL + '/' + id).then((rawResponse) => {
      const entry = rawResponse.data.data
      return this.serverResponseToEntity(entry)
    })
  }

  static find (
    pageSize: number,
    text: string | null,
    manufacturer: Manufacturer[],
    states: Status[],
    types: DeviceType[]
  ): Promise<IPaginationLoader<Device>> {
    const loaderPromise: Promise<IPaginationLoader<Device>> = this.findAllOnPage(1, pageSize)

    let filterFunc = (_device: Device): boolean => { return true }

    if (text) {
      filterFunc = (device: Device): boolean => {
        return device.shortName.includes(text)
      }
    }
    if (manufacturer.length > 0) {
      const oldFilterFunc = filterFunc

      filterFunc = (device: Device): boolean => {
        return oldFilterFunc(device) && (
          manufacturer.findIndex(m => m.uri === device.manufacturerUri) > -1
        )
      }
    }
    if (states.length > 0) {
      const oldFilterFunc = filterFunc
      filterFunc = (device: Device): boolean => {
        return oldFilterFunc(device) && (
          states.findIndex(s => s.uri === device.statusUri) > -1
        )
      }
    }
    if (types.length > 0) {
      const oldFilterFunc = filterFunc
      filterFunc = (device: Device): boolean => {
        return oldFilterFunc(device) && (
          types.findIndex(t => t.uri === device.deviceTypeUri) > -1
        )
      }
    }

    return loaderPromise.then((loader) => {
      return new FilteredPaginationedLoader<Device>(loader, filterFunc)
    })
  }
}
