import { AxiosInstance } from 'axios'

import Unit from '@/models/Unit'

export default class UnitApi {
  private axiosApi: AxiosInstance

  constructor (axiosInstance: AxiosInstance) {
    this.axiosApi = axiosInstance
  }

  newSearchBuilder (): UnitSearchBuilder {
    return new UnitSearchBuilder(this.axiosApi)
  }

  findAll (): Promise<Unit[]> {
    return this.newSearchBuilder().build().findMatchingAsList()
  }
}

export function serverResponseToEntity (entry: any): Unit {
  const id = entry.id
  let name = entry.attributes.unitsname
  if (entry.attributes.unitsabbreviation) {
    name += ' [' + entry.attributes.unitsabbreviation + ']'
  }
  const url = entry.attributes.unitslink || entry.links.self

  return Unit.createWithData(id, name, url)
}

export class UnitSearchBuilder {
  private axiosApi: AxiosInstance

  constructor (axiosApi: AxiosInstance) {
    this.axiosApi = axiosApi
  }

  build (): UnitSearcher {
    return new UnitSearcher(this.axiosApi)
  }
}

export class UnitSearcher {
  private axiosApi: AxiosInstance

  constructor (axiosApi: AxiosInstance) {
    this.axiosApi = axiosApi
  }

  findMatchingAsList (): Promise<Unit[]> {
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
      const result: Unit[] = []

      for (const entry of response.data) {
        result.push(serverResponseToEntity(entry))
      }

      return result
    })
  }
}
