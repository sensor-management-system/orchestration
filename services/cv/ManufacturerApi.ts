import { AxiosInstance } from 'axios'

import Manufacturer from '@/models/Manufacturer'
import { removeBaseUrl } from '@/utils/urlHelpers'

export default class ManufacturerApi {
  private axiosApi: AxiosInstance
  private cvBaseUrl: string | undefined

  constructor (axiosInstance: AxiosInstance, cvBaseUrl: string | undefined) {
    this.axiosApi = axiosInstance
    this.cvBaseUrl = cvBaseUrl
  }

  newSearchBuilder (): ManufacturerSearchBuilder {
    return new ManufacturerSearchBuilder(this.axiosApi, this.cvBaseUrl)
  }

  findAll (): Promise<Manufacturer[]> {
    return this.newSearchBuilder().build().findMatchingAsList()
  }
}

export function serverResponseToEntity (entry: any, cvBaseUrl: string | undefined): Manufacturer {
  const id = entry.id
  const name = entry.attributes.name
  const url = removeBaseUrl(entry.links.self, cvBaseUrl)

  return Manufacturer.createWithData(id, name, url)
}

export class ManufacturerSearchBuilder {
  private axiosApi: AxiosInstance
  private cvBaseUrl: string | undefined

  constructor (axiosApi: AxiosInstance, cvBaseUrl: string | undefined) {
    this.axiosApi = axiosApi
    this.cvBaseUrl = cvBaseUrl
  }

  build (): ManufacturerSearcher {
    return new ManufacturerSearcher(this.axiosApi, this.cvBaseUrl)
  }
}

export class ManufacturerSearcher {
  private axiosApi: AxiosInstance
  private cvBaseUrl: string | undefined

  constructor (axiosApi: AxiosInstance, cvBaseUrl: string | undefined) {
    this.axiosApi = axiosApi
    this.cvBaseUrl = cvBaseUrl
  }

  findMatchingAsList (): Promise<Manufacturer[]> {
    return this.axiosApi.get(
      '',
      {
        params: {
          'page[limit]': 100000,
          'filter[active]': true,
          sort: 'name'
        }
      }
    ).then((rawResponse) => {
      const response = rawResponse.data
      const result: Manufacturer[] = []

      for (const entry of response.data) {
        result.push(serverResponseToEntity(entry, this.cvBaseUrl))
      }

      return result
    })
  }
}
