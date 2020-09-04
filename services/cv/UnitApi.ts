import { AxiosInstance } from 'axios'

import Unit from '@/models/Unit'
import { removeBaseUrl } from '@/utils/urlHelpers'

export default class UnitApi {
  private axiosApi: AxiosInstance
  private cvBaseUrl: string | undefined

  constructor (axiosInstance: AxiosInstance, cvBaseUrl: string | undefined) {
    this.axiosApi = axiosInstance
    this.cvBaseUrl = cvBaseUrl
  }

  newSearchBuilder (): UnitSearchBuilder {
    return new UnitSearchBuilder(this.axiosApi, this.cvBaseUrl)
  }

  findAll (): Promise<Unit[]> {
    return this.newSearchBuilder().build().findMatchingAsList()
  }
}

export function serverResponseToEntity (entry: any, cvBaseUrl: string | undefined): Unit {
  const id = entry.id
  let name = entry.attributes.unitsname
  if (entry.attributes.unitsabbreviation) {
    name += ' [' + entry.attributes.unitsabbreviation + ']'
  }
  const url = removeBaseUrl(entry.links.self, cvBaseUrl)

  return Unit.createWithData(id, name, url)
}

export class UnitSearchBuilder {
  private axiosApi: AxiosInstance
  private cvBaseUrl: string | undefined

  constructor (axiosApi: AxiosInstance, cvBaseUrl: string | undefined) {
    this.axiosApi = axiosApi
    this.cvBaseUrl = cvBaseUrl
  }

  build (): UnitSearcher {
    return new UnitSearcher(this.axiosApi, this.cvBaseUrl)
  }
}

export class UnitSearcher {
  private axiosApi: AxiosInstance
  private cvBaseUrl: string | undefined

  constructor (axiosApi: AxiosInstance, cvBaseUrl: string | undefined) {
    this.axiosApi = axiosApi
    this.cvBaseUrl = cvBaseUrl
  }

  findMatchingAsList (): Promise<Unit[]> {
    return this.axiosApi.get(
      '',
      {
        params: {
          'page[limit]': 100000,
          'filter[active]': true,
          sort: 'unitsname'
        }
      }
    ).then((rawResponse) => {
      const response = rawResponse.data
      const result: Unit[] = []

      for (const entry of response.data) {
        result.push(serverResponseToEntity(entry, this.cvBaseUrl))
      }

      return result
    })
  }
}
