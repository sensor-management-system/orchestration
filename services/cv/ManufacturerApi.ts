import { AxiosInstance } from 'axios'

import Manufacturer from '@/models/Manufacturer'

export default class ManufacturerApi {
  private axiosApi: AxiosInstance

  constructor (axiosInstance: AxiosInstance) {
    this.axiosApi = axiosInstance
  }

  newSearchBuilder (): ManufacturerSearchBuilder {
    return new ManufacturerSearchBuilder(this.axiosApi)
  }

  findAll (): Promise<Manufacturer[]> {
    return this.newSearchBuilder().build().findMatchingAsList()
  }
}

export function serverResponseToEntity (entry: any): Manufacturer {
  const id = entry.id
  const name = entry.attributes.name
  const url = entry.links.self

  return Manufacturer.createWithData(id, name, url)
}

export class ManufacturerSearchBuilder {
  private axiosApi: AxiosInstance

  constructor (axiosApi: AxiosInstance) {
    this.axiosApi = axiosApi
  }

  build (): ManufacturerSearcher {
    return new ManufacturerSearcher(this.axiosApi)
  }
}

export class ManufacturerSearcher {
  private axiosApi: AxiosInstance

  constructor (axiosApi: AxiosInstance) {
    this.axiosApi = axiosApi
  }

  findMatchingAsList (): Promise<Manufacturer[]> {
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
      const result: Manufacturer[] = []

      for (const entry of response.data) {
        result.push(serverResponseToEntity(entry))
      }

      return result
    })
  }
}
