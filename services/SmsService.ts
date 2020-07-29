import axios from 'axios'

import {
  IPaginationLoader, FilteredPaginationedLoader
} from '@/utils/PaginatedLoader'

import Platform from '../models/Platform'
import Device from '../models/Device'
import Contact from '../models/Contact'
import Manufacturer from '~/models/Manufacturer'

// Use on version for all the queries
const BASE_URL = process.env.smsBackendUrl + '/rdm/svm-api/v1'

export default class SmsService {
  static serverPlatformResponseToEntity (entry: any) : Platform {
    const result: Platform = Platform.createEmpty()

    const attributes = entry.attributes

    // TODO: use camelCase only!!!
    result.id = Number.parseInt(entry.id)

    result.description = attributes.description || ''
    result.inventoryNumber = attributes.inventory_number || ''
    result.longName = attributes.long_name || ''
    // TODO: Renaming to manufacturerUri after Change in Backend
    result.manufacturerUri = attributes.manufacturer || ''
    // TODO: Read from the right field
    result.model = attributes.type || ''
    // TODO: Renaming to platform_type_uri after change in backend
    // TODO: Add platformTypeName
    result.platformTypeUri = attributes.platform_type || ''
    result.shortName = attributes.short_name || ''
    result.website = attributes.url || ''
    // TODO: statusUri
    // TODO: serialNumber

    // TODO: reading the contacts
    result.contacts = []

    return result
  }

  static serverDeviceResponseToEntity (entry: any) : Device {
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

  static findPlatformById (id: string): Promise<Platform> {
    // TODO: Think about also including the contacts
    // with ?include=contacts
    return axios.get(BASE_URL + '/platforms/' + id).then((rawResponse) => {
      const entry = rawResponse.data.data
      return this.serverPlatformResponseToEntity(entry)
    })
  }

  static deletePlatform (id: number) {
    return axios.delete(BASE_URL + '/platforms/' + id)
  }

  static deleteDevice (id: number) {
    return axios.delete(BASE_URL + '/devices/' + id)
  }

  static savePlatform (platform: Platform) {
    let method = axios.patch
    // TODO: consistent camelCase
    const data: any = {
      type: 'platform',
      attributes: {
        description: platform.description,
        inventory_number: platform.inventoryNumber,
        long_name: platform.longName,
        // TODO: handle manufacturerName
        manufacturer: platform.manufacturerUri,
        // TODO: Handle platformTypeName
        platform_type: platform.platformTypeUri,
        // TODO: serialNumber
        short_name: platform.shortName,
        // TODO: statusUri
        url: platform.website,
        // TODO: handle contacts
        // TODO: Handle attachments

        // TODO: Remove type
        // --> For the platform we have a platform type, but no other
        // general type.
        type: ''

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
    let url = BASE_URL + '/platforms'

    if (platform.id === null) {
      // new -> post
      method = axios.post
    } else {
      // old -> patch
      data.id = platform.id
      url = url + '/' + platform.id
    }

    // TODO: links for contacts
    return method(
      url,
      {
        data
      }
    ).then((serverAnswer) => {
      return this.serverPlatformResponseToEntity(serverAnswer.data.data)
    })
  }

  static saveDevice (device: Device) {
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
    let url = BASE_URL + '/devices'

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
      return this.serverDeviceResponseToEntity(serverAnswer.data.data)
    })
  }

  // we start with zero
  static findAllPlatformsOnPage (page: number, pageSize: number): Promise<IPaginationLoader<Platform>> {
    const pageParameter = 'page[size]=' + pageSize + '&page[number]=' + page

    return axios.get(BASE_URL + '/platforms?' + pageParameter).then((rawResponse) => {
      const rawData = rawResponse.data
      const result: Platform[] = []

      for (const entry of rawData.data) {
        result.push(this.serverPlatformResponseToEntity(entry))
      }

      let funToLoadNext = null

      if (result.length > 0) {
        funToLoadNext = () => this.findAllPlatformsOnPage(page + 1, pageSize)
      }

      return {
        elements: result,
        funToLoadNext
      }
    })
  }

  static findAllDevicesOnPage (page: number, pageSize: number): Promise<IPaginationLoader<Device>> {
    const pageParameter = 'page[size]=' + pageSize + '&page[number]=' + page
    // TODO: Think about also including the contacts
    // with ?include=contacts
    // size for having one query to get all the devices (no pagination)
    return axios.get(BASE_URL + '/devices?' + pageParameter).then((rawResonse) => {
      const rawData = rawResonse.data
      const result: Device[] = []

      for (const entry of rawData.data) {
        result.push(this.serverDeviceResponseToEntity(entry))
      }

      let funToLoadNext = null

      if (result.length > 0) {
        funToLoadNext = () => this.findAllDevicesOnPage(page + 1, pageSize)
      }

      return {
        elements: result,
        funToLoadNext
      }
    })
  }

  static findDeviceById (id: string): Promise<Device> {
    // TODO: Think about also including the contacts
    // with ?include=contacts
    return axios.get(BASE_URL + '/devices/' + id).then((rawResponse) => {
      const entry = rawResponse.data.data
      return this.serverDeviceResponseToEntity(entry)
    })
  }

  static findDevices (
    pageSize: number,
    text: string | null,
    manufacturer: Manufacturer[]
  ): Promise<IPaginationLoader<Device>> {
    const loaderPromise: Promise<IPaginationLoader<Device>> = this.findAllDevicesOnPage(1, pageSize)

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

    return loaderPromise.then((loader) => {
      return new FilteredPaginationedLoader<Device>(loader, filterFunc)
    })
  }

  static findPlatforms (
    pageSize: number,
    text: string | null,
    manufacturer: Manufacturer[]
  ): Promise<IPaginationLoader<Platform>> {
    const loaderPromise: Promise<IPaginationLoader<Platform>> = this.findAllPlatformsOnPage(1, pageSize)

    let filterFunc = (_platform: Platform): boolean => { return true }

    if (text) {
      filterFunc = (platform: Platform): boolean => {
        return platform.shortName.includes(text)
      }
    }
    if (manufacturer.length > 0) {
      const oldFilterFunc = filterFunc

      filterFunc = (platform: Platform): boolean => {
        return oldFilterFunc(platform) && (
          manufacturer.findIndex(m => m.uri === platform.manufacturerUri) > -1
        )
      }
    }
    return loaderPromise.then((loader) => {
      return new FilteredPaginationedLoader<Platform>(loader, filterFunc)
    })
  }

  static findAllContacts (): Promise<Contact[]> {
    return axios.get(BASE_URL + '/contacts').then((rawResponse) => {
      const rawData = rawResponse.data
      const result: Contact[] = []

      for (const entry of rawData.data) {
        const attributes = entry.attributes
        const newEntry = Contact.createEmpty()

        newEntry.id = Number.parseInt(entry.id)
        newEntry.email = attributes.email
        // TODO: Consistant usage of camel/snake case
        // JSONAPI uses camelcase
        if (attributes.first_name) {
          newEntry.givenName = attributes.first_name
        }
        if (attributes.last_name) {
          newEntry.familyName = attributes.last_name
        }
        if (attributes.profile_link) {
          newEntry.website = attributes.profile_link
        }
        result.push(newEntry)
      }

      return result
    })
  }
}
