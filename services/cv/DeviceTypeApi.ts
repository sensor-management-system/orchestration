import { AxiosInstance } from 'axios'

import DeviceType from '@/models/DeviceType'
import { removeBaseUrl } from '@/utils/urlHelpers'

export default class DeviceTypeApi {
  private axiosApi: AxiosInstance
  private cvBaseUrl: string | undefined

  constructor (axiosInstance: AxiosInstance, cvBaseUrl: string | undefined) {
    this.axiosApi = axiosInstance
    this.cvBaseUrl = cvBaseUrl
  }

  newSearchBuilder (): DeviceTypeSearchBuilder {
    return new DeviceTypeSearchBuilder(this.axiosApi, this.cvBaseUrl)
  }

  findAll (): Promise<DeviceType[]> {
    return this.newSearchBuilder().build().findMatchingAsList()
  }
}

export function serverResponseToEntity (entry: any, cvBaseUrl: string | undefined): DeviceType {
  const id = entry.id
  const name = entry.attributes.name
  const url = removeBaseUrl(entry.links.self, cvBaseUrl)

  return DeviceType.createWithData(id, name, url)
}

export class DeviceTypeSearchBuilder {
  private axiosApi: AxiosInstance
  private cvBaseUrl: string | undefined

  constructor (axiosApi: AxiosInstance, cvBaseUrl: string | undefined) {
    this.axiosApi = axiosApi
    this.cvBaseUrl = cvBaseUrl
  }

  build (): DeviceTypeSearcher {
    return new DeviceTypeSearcher(this.axiosApi, this.cvBaseUrl)
  }
}

export class DeviceTypeSearcher {
  private axiosApi: AxiosInstance
  private cvBaseUrl: string | undefined

  constructor (axiosApi: AxiosInstance, cvBaseUrl: string | undefined) {
    this.axiosApi = axiosApi
    this.cvBaseUrl = cvBaseUrl
  }

  findMatchingAsList (): Promise<DeviceType[]> {
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
      const result: DeviceType[] = []

      for (const entry of response.data) {
        result.push(serverResponseToEntity(entry, this.cvBaseUrl))
      }

      return result
    })
  }
}
