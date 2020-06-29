import axios from 'axios'

import Manufacturer from '../models/Manufacturer'
import PlatformType from '~/models/PlatformType'
import Status from '~/models/Status'
import DeviceType from '~/models/DeviceType'

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
    return axios.get(BASE_URL + '/sitetype').then((rawResponse) => {
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
    return axios.get(BASE_URL + '/equipmenttype').then((rawResponse) => {
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
}
