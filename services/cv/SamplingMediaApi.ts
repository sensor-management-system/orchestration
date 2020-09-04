import { AxiosInstance } from 'axios'

import SamplingMedia from '@/models/SamplingMedia'
import { removeBaseUrl } from '@/utils/urlHelpers'

export default class SamplingMediaApi {
  private axiosApi: AxiosInstance
  private cvBaseUrl: string | undefined

  constructor (axiosInstance: AxiosInstance, cvBaseUrl: string | undefined) {
    this.axiosApi = axiosInstance
    this.cvBaseUrl = cvBaseUrl
  }

  newSearchBuilder (): SamplingMediaSearchBuilder {
    return new SamplingMediaSearchBuilder(this.axiosApi, this.cvBaseUrl)
  }

  findAll (): Promise<SamplingMedia[]> {
    return this.newSearchBuilder().build().findMatchingAsList()
  }
}

export function serverResponseToEntity (entry: any, cvBaseUrl: string | undefined): SamplingMedia {
  const id = entry.id
  const name = entry.attributes.name
  const url = removeBaseUrl(entry.links.self, cvBaseUrl)

  return SamplingMedia.createWithData(id, name, url)
}

export class SamplingMediaSearchBuilder {
  private axiosApi: AxiosInstance
  private cvBaseUrl: string | undefined

  constructor (axiosApi: AxiosInstance, cvBaseUrl: string | undefined) {
    this.axiosApi = axiosApi
    this.cvBaseUrl = cvBaseUrl
  }

  build (): SamplingMediaSearcher {
    return new SamplingMediaSearcher(this.axiosApi, this.cvBaseUrl)
  }
}

export class SamplingMediaSearcher {
  private axiosApi: AxiosInstance
  private cvBaseUrl: string | undefined

  constructor (axiosApi: AxiosInstance, cvBaseUrl: string | undefined) {
    this.axiosApi = axiosApi
    this.cvBaseUrl = cvBaseUrl
  }

  findMatchingAsList (): Promise<SamplingMedia[]> {
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
      const result: SamplingMedia[] = []

      for (const entry of response.data) {
        result.push(serverResponseToEntity(entry, this.cvBaseUrl))
      }

      return result
    })
  }
}
