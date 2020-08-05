import { AxiosInstance } from 'axios'

import PlatformType from '@/models/PlatformType'

export default class PlatformTypeApi {
  private axiosApi: AxiosInstance

  constructor (axiosInstance: AxiosInstance) {
    this.axiosApi = axiosInstance
  }

  newSearchBuilder (): PlatformTypeSearchBuilder {
    return new PlatformTypeSearchBuilder(this.axiosApi)
  }

  findAll (): Promise<PlatformType[]> {
    return this.newSearchBuilder().build().findMatchingAsList()
  }
}

export function serverResponseToEntity (entry: any): PlatformType {
  const id = entry.id
  const name = entry.attributes.name
  const url = entry.links.self

  return PlatformType.createWithData(id, name, url)
}

export class PlatformTypeSearchBuilder {
  private axiosApi: AxiosInstance

  constructor (axiosApi: AxiosInstance) {
    this.axiosApi = axiosApi
  }

  build (): PlatformTypeSearcher {
    return new PlatformTypeSearcher(this.axiosApi)
  }
}

export class PlatformTypeSearcher {
  private axiosApi: AxiosInstance

  constructor (axiosApi: AxiosInstance) {
    this.axiosApi = axiosApi
  }

  findMatchingAsList (): Promise<PlatformType[]> {
    return this.axiosApi.get(
      '',
      {
        params: {
          'page[limit]': 100000,
          'filter[active]': true
        }
      }
    ).then((rawResponse) => {
      const response = rawResponse.data
      const result: PlatformType[] = []

      for (const entry of response.data) {
        result.push(serverResponseToEntity(entry))
      }

      return result
    })
  }
}
