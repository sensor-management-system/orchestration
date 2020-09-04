import { AxiosInstance } from 'axios'

import PlatformType from '@/models/PlatformType'
import { removeBaseUrl } from '@/utils/urlHelpers'

export default class PlatformTypeApi {
  private axiosApi: AxiosInstance
  private cvBaseUrl: string | undefined

  constructor (axiosInstance: AxiosInstance, cvBaseUrl: string | undefined) {
    this.axiosApi = axiosInstance
    this.cvBaseUrl = cvBaseUrl
  }

  newSearchBuilder (): PlatformTypeSearchBuilder {
    return new PlatformTypeSearchBuilder(this.axiosApi, this.cvBaseUrl)
  }

  findAll (): Promise<PlatformType[]> {
    return this.newSearchBuilder().build().findMatchingAsList()
  }
}

export function serverResponseToEntity (entry: any, cvBaseUrl: string | undefined): PlatformType {
  const id = entry.id
  const name = entry.attributes.name
  const url = removeBaseUrl(entry.links.self, cvBaseUrl)

  return PlatformType.createWithData(id, name, url)
}

export class PlatformTypeSearchBuilder {
  private axiosApi: AxiosInstance
  private cvBaseUrl: string | undefined

  constructor (axiosApi: AxiosInstance, cvBaseUrl: string | undefined) {
    this.axiosApi = axiosApi
    this.cvBaseUrl = cvBaseUrl
  }

  build (): PlatformTypeSearcher {
    return new PlatformTypeSearcher(this.axiosApi, this.cvBaseUrl)
  }
}

export class PlatformTypeSearcher {
  private axiosApi: AxiosInstance
  private cvBaseUrl: string | undefined

  constructor (axiosApi: AxiosInstance, cvBaseUrl: string | undefined) {
    this.axiosApi = axiosApi
    this.cvBaseUrl = cvBaseUrl
  }

  findMatchingAsList (): Promise<PlatformType[]> {
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
      const result: PlatformType[] = []

      for (const entry of response.data) {
        result.push(serverResponseToEntity(entry, this.cvBaseUrl))
      }

      return result
    })
  }
}
