import axios, { AxiosInstance } from 'axios'

import Status from '@/models/Status'

const BASE_URL = process.env.cvBackendUrl + '/equipmentstatus'

export default class StatusApi {
  private axiosApi: AxiosInstance

  constructor (baseURL: string = BASE_URL) {
    this.axiosApi = axios.create({
      baseURL
    })
  }

  newSearchBuilder (): StatusSearchBuilder {
    return new StatusSearchBuilder(this.axiosApi)
  }

  findAll (): Promise<Status[]> {
    return this.newSearchBuilder().build().findMatchingAsList()
  }
}

export function serverResponseToEntity (entry: any): Status {
  const id = entry.id
  const name = entry.attributes.name
  const url = entry.links.self

  return Status.createWithData(id, name, url)
}

export class StatusSearchBuilder {
  private axiosApi: AxiosInstance

  constructor (axiosApi: AxiosInstance) {
    this.axiosApi = axiosApi
  }

  build (): StatusSearcher {
    return new StatusSearcher(this.axiosApi)
  }
}

export class StatusSearcher {
  private axiosApi: AxiosInstance

  constructor (axiosApi: AxiosInstance) {
    this.axiosApi = axiosApi
  }

  findMatchingAsList (): Promise<Status[]> {
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
      const result: Status[] = []

      for (const entry of response.data) {
        result.push(serverResponseToEntity(entry))
      }

      return result
    })
  }
}
