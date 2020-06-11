import axios from 'axios'

import Platform from '../models/Platform'
import Device from '../models/Device'
import Contact from '../models/Contact'

import { IDeviceOrPlatformSearchObject } from '../models/IDeviceOrPlatformSearchObject'

import { PlatformOrDeviceSearchType } from '../enums/PlatformOrDeviceSearchType'
import Manufacturer from '~/models/Manufacturer'
import Status from '~/models/Status'
import PlatformType from '~/models/PlatformType'

// Use on version for all the queries
const BASE_URL = process.env.backendUrl + '/rdm/svm-api/v1'

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
        url: platform.website
        // TODO: handle contacts
        // TODO: Handle attachments

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
        url: device.website
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

  static findAllPlatforms (): Promise<Platform[]> {
    // TODO: Think about also including the contacts
    // with ?include=contacts
    return axios.get(BASE_URL + '/platforms').then((rawResponse) => {
      const rawData = rawResponse.data
      const result: Platform[] = []

      for (const entry of rawData.data) {
        result.push(this.serverPlatformResponseToEntity(entry))
      }

      return result
    })
  }

  static findAllDevices (): Promise<Device[]> {
    // TODO: Think about also including the contacts
    // with ?include=contacts
    return axios.get(BASE_URL + '/devices').then((rawResonse) => {
      const rawData = rawResonse.data
      const result: Device[] = []

      for (const entry of rawData.data) {
        result.push(this.serverDeviceResponseToEntity(entry))
      }

      return result
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

  static findPlatformsAndSensors (
    text: string | null,
    platformOrDevice: PlatformOrDeviceSearchType,
    manufacturer: Manufacturer[],
    platformTypeLookupByUri: Map<string, PlatformType>,
    statusLookupByUri: Map<string, Status>
  ): Promise<IDeviceOrPlatformSearchObject[]> {
    let promiseAllPlatforms: Promise<Platform[]> = new Promise(resolve => resolve([]))
    let promiseAllDevices: Promise<Device[]> = new Promise(resolve => resolve([]))

    if (platformOrDevice === PlatformOrDeviceSearchType.PLATFORMS) {
      promiseAllPlatforms = this.findAllPlatforms()
    } else if (platformOrDevice === PlatformOrDeviceSearchType.DEVICES) {
      promiseAllDevices = this.findAllDevices()
    } else {
      promiseAllPlatforms = this.findAllPlatforms()
      promiseAllDevices = this.findAllDevices()
    }

    return new Promise((resolve) => {
      promiseAllPlatforms.then((allPlatforms) => {
        promiseAllDevices.then((allDevices) => {
          const result = []

          let filterFuncPlatform = (_platform: Platform): boolean => { return true }
          let filterFuncDevice = (_device: Device): boolean => { return true }

          if (text) {
            filterFuncPlatform = (platform: Platform): boolean => {
              return platform.shortName.includes(text)
            }
            filterFuncDevice = (device: Device): boolean => {
              return device.shortName.includes(text)
            }
          }

          if (manufacturer.length > 0) {
            const oldFilterFuncPlatform = filterFuncPlatform
            const oldFilterFuncDevice = filterFuncDevice

            filterFuncPlatform = (platform: Platform): boolean => {
              return oldFilterFuncPlatform(platform) && (
                manufacturer.findIndex(m => m.uri === platform.manufacturerUri) > -1
              )
            }

            filterFuncDevice = (device: Device) : boolean => {
              return oldFilterFuncDevice(device) && (
                // TODO
                manufacturer.findIndex(m => m.uri === device.manufacturerUri) > -1
              )
            }
          }

          for (const platform of allPlatforms) {
            if (filterFuncPlatform(platform)) {
              result.push(platform.toSearchObject(platformTypeLookupByUri, statusLookupByUri))
            }
          }

          for (const device of allDevices) {
            if (filterFuncDevice(device)) {
              result.push(device.toSearchObject(statusLookupByUri))
            }
          }

          resolve(result)
        })
      })
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
