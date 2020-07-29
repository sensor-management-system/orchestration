import axios from 'axios'

import Platform from '@/models/Platform'
import PlatformType from '@/models/PlatformType'

import Manufacturer from '@/models/Manufacturer'
import Status from '@/models/Status'

import {
  IPaginationLoader, FilteredPaginationedLoader
} from '@/utils/PaginatedLoader'

const BASE_URL = process.env.SmsBackendUrl

export default class PlatformApi {
  static serverResponseToEntity (entry: any) : Platform {
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

  static findById (id: string): Promise<Platform> {
    // TODO: Think about also including the contacts
    // with ?include=contacts
    return axios.get(BASE_URL + '/platforms/' + id).then((rawResponse) => {
      const entry = rawResponse.data.data
      return this.serverResponseToEntity(entry)
    })
  }

  static deleteById (id: number) {
    return axios.delete(BASE_URL + '/platforms/' + id)
  }

  static save (platform: Platform) {
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
      return this.serverResponseToEntity(serverAnswer.data.data)
    })
  }

  // we start with zero
  static findAllOnPage (page: number, pageSize: number): Promise<IPaginationLoader<Platform>> {
    const pageParameter = 'page[size]=' + pageSize + '&page[number]=' + page

    return axios.get(BASE_URL + '/platforms?' + pageParameter).then((rawResponse) => {
      const rawData = rawResponse.data
      const result: Platform[] = []

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

  static find (
    pageSize: number,
    text: string | null,
    manufacturer: Manufacturer[],
    states: Status[],
    types: PlatformType[]
  ): Promise<IPaginationLoader<Platform>> {
    const loaderPromise: Promise<IPaginationLoader<Platform>> = this.findAllOnPage(1, pageSize)

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

    if (states.length > 0) {
      const oldFilterFunc = filterFunc
      filterFunc = (platform: Platform): boolean => {
        return oldFilterFunc(platform) && (
          states.findIndex(s => s.uri === platform.statusUri) > -1
        )
      }
    }
    if (types.length > 0) {
      const oldFilterFunc = filterFunc
      filterFunc = (platform: Platform): boolean => {
        return oldFilterFunc(platform) && (
          types.findIndex(t => t.uri === platform.platformTypeUri) > -1
        )
      }
    }

    return loaderPromise.then((loader) => {
      return new FilteredPaginationedLoader<Platform>(loader, filterFunc)
    })
  }
}
