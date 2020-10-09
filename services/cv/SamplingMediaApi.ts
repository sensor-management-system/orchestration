import { AxiosInstance } from 'axios'

import SamplingMedia from '@/models/SamplingMedia'
import SamplingMediaSerializer from '@/serializers/jsonapi/SamplingMediaSerializer'

export default class SamplingMediaApi {
  private axiosApi: AxiosInstance
  private serializer: SamplingMediaSerializer

  constructor (axiosInstance: AxiosInstance, cvBaseUrl: string | undefined) {
    this.axiosApi = axiosInstance
    this.serializer = new SamplingMediaSerializer(cvBaseUrl)
  }

  newSearchBuilder (): SamplingMediaSearchBuilder {
    return new SamplingMediaSearchBuilder(this.axiosApi, this.serializer)
  }

  findAll (): Promise<SamplingMedia[]> {
    return this.newSearchBuilder().build().findMatchingAsList()
  }
}

export class SamplingMediaSearchBuilder {
  private axiosApi: AxiosInstance
  private serializer: SamplingMediaSerializer

  constructor (axiosApi: AxiosInstance, serializer: SamplingMediaSerializer) {
    this.axiosApi = axiosApi
    this.serializer = serializer
  }

  build (): SamplingMediaSearcher {
    return new SamplingMediaSearcher(this.axiosApi, this.serializer)
  }
}

export class SamplingMediaSearcher {
  private axiosApi: AxiosInstance
  private serializer: SamplingMediaSerializer

  constructor (axiosApi: AxiosInstance, serializer: SamplingMediaSerializer) {
    this.axiosApi = axiosApi
    this.serializer = serializer
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
      return this.serializer.convertJsonApiObjectListToModelList(response)
    })
  }
}
