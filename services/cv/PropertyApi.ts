import { AxiosInstance } from 'axios'

import Property from '@/models/Property'
import { removeBaseUrl } from '@/utils/urlHelpers'

export default class PropertyApi {
  private axiosApi: AxiosInstance
  private cvBaseUrl: string | undefined

  constructor (axiosInstance: AxiosInstance, cvBaseUrl: string | undefined) {
    this.axiosApi = axiosInstance
    this.cvBaseUrl = cvBaseUrl
  }

  newSearchBuilder (): PropertySearchBuilder {
    return new PropertySearchBuilder(this.axiosApi, this.cvBaseUrl)
  }

  findAll (): Promise<Property[]> {
    return this.newSearchBuilder().build().findMatchingAsList()
  }
}

export function serverResponseToEntity (entry: any, cvBaseUrl: string | undefined): Property {
  const id = entry.id
  const name = entry.attributes.name
  const url = removeBaseUrl(entry.links.self, cvBaseUrl)

  return Property.createWithData(id, name, url)
}

export class PropertySearchBuilder {
  private axiosApi: AxiosInstance
  private cvBaseUrl: string | undefined

  constructor (axiosApi: AxiosInstance, cvBaseUrl: string | undefined) {
    this.axiosApi = axiosApi
    this.cvBaseUrl = cvBaseUrl
  }

  build (): PropertySearcher {
    return new PropertySearcher(this.axiosApi, this.cvBaseUrl)
  }
}

export class PropertySearcher {
  private axiosApi: AxiosInstance
  private cvBaseUrl: string | undefined

  constructor (axiosApi: AxiosInstance, cvBaseUrl: string | undefined) {
    this.axiosApi = axiosApi
    this.cvBaseUrl = cvBaseUrl
  }

  findMatchingAsList (): Promise<Property[]> {
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
      const result: Property[] = []

      for (const entry of response.data) {
        result.push(serverResponseToEntity(entry, this.cvBaseUrl))
      }

      return result
    })
  }
}
