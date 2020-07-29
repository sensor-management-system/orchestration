import axios, { AxiosInstance } from 'axios'

import Compartment from '@/models/Compartment'

const BASE_URL = process.env.cvBackendUrl + '/variabletype'

export default class DeviceTypeApi {
  private axiosApi: AxiosInstance

  constructor (baseURL: string = BASE_URL) {
    this.axiosApi = axios.create({
      baseURL
    })
  }

  newSearchBuilder (): CompartmentSearchBuilder {
    return new CompartmentSearchBuilder(this.axiosApi)
  }

  findAll (): Promise<Compartment[]> {
    return this.newSearchBuilder().build().findMatchingAsList()
  }
}

export function serverResponseToEntity (entry: any): Compartment {
  const id = entry.id
  const name = entry.attributes.name
  const url = entry.links.self

  return Compartment.createWithData(id, name, url)
}

export class CompartmentSearchBuilder {
  private axiosApi: AxiosInstance

  constructor (axiosApi: AxiosInstance) {
    this.axiosApi = axiosApi
  }

  build (): CompartmentSearcher {
    return new CompartmentSearcher(this.axiosApi)
  }
}

export class CompartmentSearcher {
  private axiosApi: AxiosInstance

  constructor (axiosApi: AxiosInstance) {
    this.axiosApi = axiosApi
  }

  findMatchingAsList (): Promise<Compartment[]> {
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
      const result: Compartment[] = []

      for (const entry of response.data) {
        result.push(serverResponseToEntity(entry))
      }

      return result
    })
  }
}
