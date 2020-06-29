import axios from 'axios'

import Manufacturer from '../models/Manufacturer'
import PlatformType from '~/models/PlatformType'
import Status from '~/models/Status'
import DeviceType from '~/models/DeviceType'
import Compartment from '~/models/Compartment'
import SamplingMedia from '~/models/SamplingMedia'
import Property from '~/models/Property'
import Unit from '~/models/Unit'

const BASE_URL = process.env.cvBackendUrl + '/api'

export default class CVService {
  static findAllManufacturers (): Promise<Manufacturer[]> {
    return new Promise<Manufacturer[]>((resolve) => {
      resolve([
        Manufacturer.createWithData(1, 'Manufacturer 01', 'http://helmholtz/smsvc/manfucturer/1'),
        Manufacturer.createWithData(2, 'Manufacturer 02', 'http://helmholtz/smsvs/manfucturer/2')
      ])
    })
  }

  static findAllPlatformTypes (): Promise<PlatformType[]> {
    return axios.get(BASE_URL + '/sitetype?page[size]=100000').then((rawResponse) => {
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
    return new Promise<Status[]>((resolve) => {
      resolve([
        Status.createWithData(1, 'in warehouse', 'https//helmholtz/smsvc/platformstatus/1'),
        Status.createWithData(2, 'in use', 'https//helmholtz/smsvc/platformstatus/2'),
        Status.createWithData(3, 'under construction', 'https//helmholtz/smsvc/platformstatus/3'),
        Status.createWithData(4, 'blocked', 'https//helmholtz/smsvc/platformstatus/4'),
        Status.createWithData(5, 'scrapped', 'https//helmholtz/smsvc/platformstatus/5')
      ])
    })
  }

  static findAllDeviceTypes (): Promise<DeviceType[]> {
    return axios.get(BASE_URL + '/equipmenttype?page[limit]=100000').then((rawResponse) => {
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
    return axios.get(BASE_URL + '/variabletype?page[limit]=100000').then((rawResponse) => {
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
    return axios.get(BASE_URL + '/medium?page[limit]=100000').then((rawResponse) => {
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
    // TODO: It seems that a value > 250 is ignored
    // but as we have here > 900 entries, we need to support those as well
    return axios.get(BASE_URL + '/variablename?page[limit]=100000').then((rawResponse) => {
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
    // we don't have the http://vocabulary.odm2.org/units/
    // at the moment in our database
    return new Promise<Unit[]>((resolve) => {
      resolve([
        Unit.createWithData('1', 'm', 'https//helmholtz/smsvc/unit/1'),
        Unit.createWithData('2', 'm/s', 'https//helmholtz/smsvc/unit/2'),
        Unit.createWithData('3', 's', 'https//helmholtz/smsvc/unit/3'),
        Unit.createWithData('4', 'kg', 'https//helmholtz/smsvc/unit/4'),
        Unit.createWithData('5', 'hz', 'https//helmholtz/smsvc/unit/5')
      ])
    })
  }
}
