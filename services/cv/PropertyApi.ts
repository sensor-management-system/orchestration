import axios, { AxiosInstance } from 'axios'

import Property from '@/models/Property'

const BASE_URL = process.env.cvBackendUrl + '/variablename'

export default class PropertyApi {
  private axiosApi: AxiosInstance

  constructor (baseURL: string = BASE_URL) {
    this.axiosApi = axios.create({
      baseURL
    })
  }

  newSearchBuilder (): PropertySearchBuilder {
    return new PropertySearchBuilder(this.axiosApi)
  }

  findAll (): Promise<Property[]> {
    return this.newSearchBuilder().build().findMatchingAsList()
  }
}

export function serverResponseToEntity (entry: any): Property {
  const id = entry.id
  const name = entry.attributes.name
  const url = entry.links.self

  return Property.createWithData(id, name, url)
}

export class PropertySearchBuilder {
  private axiosApi: AxiosInstance

  constructor (axiosApi: AxiosInstance) {
    this.axiosApi = axiosApi
  }

  build (): PropertySearcher {
    return new PropertySearcher(this.axiosApi)
  }
}

export class PropertySearcher {
  private axiosApi: AxiosInstance

  constructor (axiosApi: AxiosInstance) {
    this.axiosApi = axiosApi
  }

  findMatchingAsList (): Promise<Property[]> {
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
      const result: Property[] = []

      for (const entry of response.data) {
        result.push(serverResponseToEntity(entry))
      }

      return result
    })
  }
}
