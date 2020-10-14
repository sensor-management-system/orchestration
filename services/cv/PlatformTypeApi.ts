import { AxiosInstance } from 'axios'

import { PlatformType } from '@/models/PlatformType'
import { PlatformTypeSerializer } from '@/serializers/jsonapi/PlatformTypeSerializer'

export class PlatformTypeApi {
  private axiosApi: AxiosInstance
  private serializer: PlatformTypeSerializer

  constructor (axiosInstance: AxiosInstance, cvBaseUrl: string | undefined) {
    this.axiosApi = axiosInstance
    this.serializer = new PlatformTypeSerializer(cvBaseUrl)
  }

  newSearchBuilder (): PlatformTypeSearchBuilder {
    return new PlatformTypeSearchBuilder(this.axiosApi, this.serializer)
  }

  findAll (): Promise<PlatformType[]> {
    return this.newSearchBuilder().build().findMatchingAsList()
  }
}

export class PlatformTypeSearchBuilder {
  private axiosApi: AxiosInstance
  private serializer: PlatformTypeSerializer

  constructor (axiosApi: AxiosInstance, serializer: PlatformTypeSerializer) {
    this.axiosApi = axiosApi
    this.serializer = serializer
  }

  build (): PlatformTypeSearcher {
    return new PlatformTypeSearcher(this.axiosApi, this.serializer)
  }
}

export class PlatformTypeSearcher {
  private axiosApi: AxiosInstance
  private serializer: PlatformTypeSerializer

  constructor (axiosApi: AxiosInstance, serializer: PlatformTypeSerializer) {
    this.axiosApi = axiosApi
    this.serializer = serializer
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
      return this.serializer.convertJsonApiObjectListToModelList(response)
    })
  }
}
