import { AxiosInstance } from 'axios'

import Status from '@/models/Status'
import { StatusSerializer } from '@/serializers/jsonapi/StatusSerializer'

export default class StatusApi {
  private axiosApi: AxiosInstance
  private serializer: StatusSerializer

  constructor (axiosInstance: AxiosInstance, cvBaseUrl: string | undefined) {
    this.axiosApi = axiosInstance
    this.serializer = new StatusSerializer(cvBaseUrl)
  }

  newSearchBuilder (): StatusSearchBuilder {
    return new StatusSearchBuilder(this.axiosApi, this.serializer)
  }

  findAll (): Promise<Status[]> {
    return this.newSearchBuilder().build().findMatchingAsList()
  }
}

export class StatusSearchBuilder {
  private axiosApi: AxiosInstance
  private serializer: StatusSerializer

  constructor (axiosApi: AxiosInstance, serializer: StatusSerializer) {
    this.axiosApi = axiosApi
    this.serializer = serializer
  }

  build (): StatusSearcher {
    return new StatusSearcher(this.axiosApi, this.serializer)
  }
}

export class StatusSearcher {
  private axiosApi: AxiosInstance
  private serializer: StatusSerializer

  constructor (axiosApi: AxiosInstance, serializer: StatusSerializer) {
    this.axiosApi = axiosApi
    this.serializer = serializer
  }

  findMatchingAsList (): Promise<Status[]> {
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
      return this.serializer.convertJsonApiObjectListToModelList(response)
    })
  }
}
