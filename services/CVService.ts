import axios from 'axios'

import Compartment from '@/models/Compartment'
import DeviceType from '@/models/DeviceType'
import Manufacturer from '@/models/Manufacturer'
import PlatformType from '@/models/PlatformType'
import Property from '@/models/Property'
import SamplingMedia from '@/models/SamplingMedia'
import Status from '@/models/Status'
import Unit from '@/models/Unit'

const BASE_URL = process.env.cvBackendUrl + '/api'

export default class CVService {
  static findAllManufacturers (): Promise<Manufacturer[]> {
    return axios.get(BASE_URL + '/manufacturer?page[size]=100000&filter[active]=true').then((rawResponse) => {
      const response = rawResponse.data
      const data = response.data

      const result = []

      for (const record of data) {
        const id = record.id
        const name = record.attributes.name
        const url = record.links.self

        result.push(
          Manufacturer.createWithData(id, name, url)
        )
      }

      return result
    })
  }

  static findAllPlatformTypes (): Promise<PlatformType[]> {
    return axios.get(BASE_URL + '/platformtype?page[size]=100000&filter[active]=true').then((rawResponse) => {
      const response = rawResponse.data
      const data = response.data

      const result = []

      for (const record of data) {
        const id = record.id
        const name = record.attributes.name
        const url = record.links.self

        result.push(
          PlatformType.createWithData(id, name, url)
        )
      }

      return result
    })
  }

  static findAllStates (): Promise<Status[]> {
    return axios.get(BASE_URL + '/equipmentstatus?page[size]=100000&filter[active]=true').then((rawResponse) => {
      const response = rawResponse.data
      const data = response.data

      const result = []

      for (const record of data) {
        const id = record.id
        const name = record.attributes.name
        const url = record.links.self

        result.push(
          Status.createWithData(id, name, url)
        )
      }

      return result
    })
  }

  static findAllDeviceTypes (): Promise<DeviceType[]> {
    return axios.get(BASE_URL + '/equipmenttype?page[limit]=100000&filter[active]=true').then((rawResponse) => {
      const response = rawResponse.data
      const data = response.data

      const result = []

      for (const record of data) {
        const id = record.id
        const name = record.attributes.name
        const url = record.links.self

        result.push(
          DeviceType.createWithData(id, name, url)
        )
      }

      return result
    })
  }

  static findAllCompartments (): Promise<Compartment[]> {
    return axios.get(BASE_URL + '/variabletype?page[limit]=100000&filter[active]=true').then((rawResponse) => {
      const response = rawResponse.data
      const data = response.data

      const result = []

      for (const record of data) {
        const id = record.id
        const name = record.attributes.name
        const url = record.links.self

        result.push(
          Compartment.createWithData(id, name, url)
        )
      }

      return result
    })
  }

  static findAllSamplingMedias (): Promise<SamplingMedia[]> {
    return axios.get(BASE_URL + '/medium?page[limit]=100000&filter[active]=true').then((rawResponse) => {
      const response = rawResponse.data
      const data = response.data

      const result = []

      for (const record of data) {
        const id = record.id
        const name = record.attributes.name
        const url = record.links.self

        result.push(
          SamplingMedia.createWithData(id, name, url)
        )
      }

      return result
    })
  }

  static findAllProperties (): Promise<Property[]> {
    return axios.get(BASE_URL + '/variablename?page[limit]=100000&filter[active]=true').then((rawResponse) => {
      const response = rawResponse.data
      const data = response.data

      const result = []

      for (const record of data) {
        const id = record.id
        const name = record.attributes.name
        const url = record.links.self

        result.push(
          Property.createWithData(id, name, url)
        )
      }

      return result
    })
  }

  static findAllUnits (): Promise<Unit[]> {
    return axios.get(BASE_URL + '/unit?page[limit]=100000&filter[active]=true').then((rawResponse) => {
      const response = rawResponse.data
      const data = response.data

      const result = []

      for (const record of data) {
        const id = record.id
        let name = record.attributes.unitsname
        if (record.attributes.unitsabbreviation) {
          name += ' [' + record.attributes.unitsabbreviation + ']'
        }
        const url = record.attributes.unitslink || record.links.self

        result.push(
          Unit.createWithData(id, name, url)
        )
      }

      return result
    })
  }
}
