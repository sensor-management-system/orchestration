import axios from 'axios'

import Platform from '../models/Platform'
import Device from '../models/Device'

export default class DeviceService {
  static serverPlatformResponseToEntity (entry: any) : Platform {
    const result: Platform = Platform.createEmpty()

    const attributes = entry.attributes

    // TODO: use camelCase only!!!
    result.id = Number.parseInt(entry.id)
    result.platformType = attributes.platform_type || ''
    result.shortName = attributes.short_name || ''
    result.longName = attributes.long_name || ''
    result.description = attributes.description || ''
    result.manufacturer = attributes.manufacturer || ''
    result.type = attributes.type || ''
    result.inventoryNumber = attributes.inventory_number || ''
    result.url = attributes.url || ''

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
    result.manufacturer = attributes.manufacturer || ''
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
    return axios.get(process.env.backendUrl + '/sis/v1/platforms/' + id).then((rawResponse) => {
      const entry = rawResponse.data.data
      return DeviceService.serverPlatformResponseToEntity(entry)
    })
  }

  static deletePlatform (id: number) {
    return axios.delete(process.env.backendUrl + '/sis/v1/platforms/' + id)
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
        manufacturer: platform.manufacturer,
        type: platform.type,
        inventory_number: platform.inventoryNumber,
        platform_type: platform.platformType,
        url: platform.url
      }
    }
    let url = process.env.backendUrl + '/sis/v1/platforms'

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
      return DeviceService.serverPlatformResponseToEntity(serverAnswer.data.data)
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
        manufacturer: device.manufacturer,
        model: device.model,
        // TODO: This *must* be fixed at backend. PID is *NOT* a integer
        persistent_identifier: Number.parseInt(device.persistentId),
        url: device.urlWebsite,
        type: device.type,
        status: device.state,
        serial_number: device.serialNumber
      }
    }
    let url = process.env.backendUrl + '/sis/v1/devices'

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
      return DeviceService.serverDeviceResponseToEntity(serverAnswer.data.data)
    })
  }

  static findAllPlatforms (): Promise<Platform[]> {
    return axios.get(process.env.backendUrl + '/sis/v1/platforms').then((rawResponse) => {
      const rawData = rawResponse.data
      const result: Platform[] = []

      for (const entry of rawData.data) {
        result.push(this.serverPlatformResponseToEntity(entry))
      }

      return result
    })
  }

  static findAllDevices (): Promise<Device[]> {
    return axios.get(process.env.backendUrl + '/sis/v1/devices').then((rawResonse) => {
      const rawData = rawResonse.data
      const result: Device[] = []

      for (const entry of rawData.data) {
        result.push(this.serverDeviceResponseToEntity(entry))
      }

      return result
    })
  }

  static findDeviceById (id: string): Promise<Device> {
    return axios.get(process.env.backendUrl + '/sis/v1/devices/' + id).then((rawResponse) => {
      const entry = rawResponse.data.data
      return DeviceService.serverDeviceResponseToEntity(entry)
    })
  }

  static findPlatformsAndSensors (text: string | null): Promise<Array<object>> {
    const promiseAllPlatforms = this.findAllPlatforms()
    const promiseAllDevices = this.findAllDevices()

    return new Promise((resolve) => {
      promiseAllPlatforms.then((allPlatforms) => {
        promiseAllDevices.then((allDevices) => {
          const result = []

          let filterFuncPlatform = (_platform: any): boolean => { return true }
          let filterFuncDevice = (_device: any): boolean => { return true }

          if (text) {
            filterFuncPlatform = (platform: any): boolean => {
              return platform.shortName.includes(text)
            }
            filterFuncDevice = (device: any): boolean => {
              return device.label.includes(text)
            }
          }

          for (const platform of allPlatforms) {
            if (filterFuncPlatform(platform)) {
              result.push(
                {
                  id: platform.id,
                  name: platform.shortName,
                  project: '...',
                  type: platform.platformType,
                  state: 'shipping',
                  devicetype: 'platform'
                }
              )
            }
          }

          for (const device of allDevices) {
            if (filterFuncDevice(device)) {
              result.push(
                {
                  id: device.id,
                  name: device.label,
                  project: '...',
                  type: device.type,
                  state: device.state,
                  devicetype: 'device'
                }
              )
            }
          }

          resolve(result)
        })
      })
    })
  }
}
