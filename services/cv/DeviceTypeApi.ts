import axios, { AxiosInstance } from 'axios'

import DeviceType from '@/models/DeviceType'

const BASE_URL = process.env.cvBackendUrl + '/equipmenttype'

export default class DeviceTypeApi {
  private axiosApi: AxiosInstance

  constructor (baseURL: string = BASE_URL) {
    this.axiosApi = axios.create({
      baseURL
    })
  }

  newSearchBuilder (): DeviceTypeSearchBuilder {
    return new DeviceTypeSearchBuilder(this.axiosApi)
  }

  findAll (): Promise<DeviceType[]> {
    return this.newSearchBuilder().build().findMatchingAsList()
  }
}

export function serverResponseToEntity (entry: any): DeviceType {
  const id = entry.id
  const name = entry.attributes.name
  const url = entry.links.self

  return DeviceType.createWithData(id, name, url)
}

export class DeviceTypeSearchBuilder {
  private axiosApi: AxiosInstance

  constructor (axiosApi: AxiosInstance) {
    this.axiosApi = axiosApi
  }

  build (): DeviceTypeSearcher {
    return new DeviceTypeSearcher(this.axiosApi)
  }
}

export class DeviceTypeSearcher {
  private axiosApi: AxiosInstance

  constructor (axiosApi: AxiosInstance) {
    this.axiosApi = axiosApi
  }

  findMatchingAsList (): Promise<DeviceType[]> {
    return this.axiosApi.get(
      '',
      {
        params: {
          'page[size]': 100000,
          'filter[active]': true
        }
      }
    ).then((rawResponse) => {
      const response = rawResponse.data
      const result: DeviceType[] = []

      for (const entry of response.data) {
        result.push(serverResponseToEntity(entry))
      }

      return result
    })
  }
}
