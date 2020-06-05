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
    // TODO: Renaming to platform_type_uri after change in backend
    result.platformTypeUri = attributes.platform_type || ''
    result.shortName = attributes.short_name || ''
    result.longName = attributes.long_name || ''
    result.description = attributes.description || ''
    // TODO: Renaming to manufacturerUri after Change in Backend
    result.manufacturerUri = attributes.manufacturer || ''
    result.model = attributes.type || ''
    result.inventoryNumber = attributes.inventory_number || ''
    result.website = attributes.url || ''
    // TODO: platformstatusUri
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
    result.dualUse = attributes.dual_use || false
    result.inventoryNumber = attributes.inventory_number || ''
    result.label = attributes.label || ''
    // TODO: Change to uri after change in Backend
    result.manufacturerUri = attributes.manufacturer || ''
    result.model = attributes.model || ''
    result.persistentId = attributes.persistent_identifier || ''
    result.serialNumber = attributes.serial_number || ''
    // TODO: What to do with short name?
    // newEntry.name = attributes.short_name
    result.type = attributes.type || ''
    result.urlWebsite = attributes.url || ''

    // TODO
    result.contacts = []
    result.properties = []
    result.customFields = []

    return result
  }

  static findPlatformById (id: string): Promise<Platform> {
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
        short_name: platform.shortName,
        long_name: platform.longName,
        // TODO: Change after renaming to manufacturerUri in backend
        manufacturer: platform.manufacturerUri,
        type: platform.model,
        inventory_number: platform.inventoryNumber,
        // TODO: Change after renaming to platformTypeUri in backend
        platform_type: platform.platformTypeUri,
        url: platform.website
        // TODO: platformstatusUri
        // TODO: serialNumber

      }
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
        // Decide what to do with the short name
        // short_name: device.shortName,
        // Same for long name
        // long_name: device.longName
        dual_use: device.dualUse,
        inventory_number: device.inventoryNumber,
        label: device.label,
        // TODO: Change to uri after backend change
        manufacturer: device.manufacturerUri,
        model: device.model,
        persistent_identifier: device.persistentId,
        url: device.urlWebsite,
        type: device.type,
        status: device.status,
        serial_number: device.serialNumber
      }
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
              return device.label.includes(text)
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
              result.push(device.toSearchObject())
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
