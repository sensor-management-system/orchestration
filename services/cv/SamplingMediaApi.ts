import axios, { AxiosInstance } from 'axios'

import SamplingMedia from '@/models/SamplingMedia'

const BASE_URL = process.env.cvBackendUrl + '/medium'

export default class SamplingMediaApi {
  private axiosApi: AxiosInstance

  constructor (baseURL: string = BASE_URL) {
    this.axiosApi = axios.create({
      baseURL
    })
  }

  newSearchBuilder (): SamplingMediaSearchBuilder {
    return new SamplingMediaSearchBuilder(this.axiosApi)
  }

  findAll (): Promise<SamplingMedia[]> {
    return this.newSearchBuilder().build().findMatchingAsList()
  }
}

export function serverResponseToEntity (entry: any): SamplingMedia {
  const id = entry.id
  const name = entry.attributes.name
  const url = entry.links.self

  return SamplingMedia.createWithData(id, name, url)
}

export class SamplingMediaSearchBuilder {
  private axiosApi: AxiosInstance

  constructor (axiosApi: AxiosInstance) {
    this.axiosApi = axiosApi
  }

  build (): SamplingMediaSearcher {
    return new SamplingMediaSearcher(this.axiosApi)
  }
}

export class SamplingMediaSearcher {
  private axiosApi: AxiosInstance

  constructor (axiosApi: AxiosInstance) {
    this.axiosApi = axiosApi
  }

  findMatchingAsList (): Promise<SamplingMedia[]> {
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
      const result: SamplingMedia[] = []

      for (const entry of response.data) {
        result.push(serverResponseToEntity(entry))
      }

      return result
    })
  }
}
