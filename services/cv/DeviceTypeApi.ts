import { AxiosInstance } from 'axios'

import DeviceType from '@/models/DeviceType'
import DeviceTypeSerializer from '@/serializers/jsonapi/DeviceTypeSerializer'

export default class DeviceTypeApi {
  private axiosApi: AxiosInstance
  private serializer: DeviceTypeSerializer

  constructor (axiosInstance: AxiosInstance, cvBaseUrl: string | undefined) {
    this.axiosApi = axiosInstance
    this.serializer = new DeviceTypeSerializer(cvBaseUrl)
  }

  newSearchBuilder (): DeviceTypeSearchBuilder {
    return new DeviceTypeSearchBuilder(this.axiosApi, this.serializer)
  }

  findAll (): Promise<DeviceType[]> {
    return this.newSearchBuilder().build().findMatchingAsList()
  }
}

export class DeviceTypeSearchBuilder {
  private axiosApi: AxiosInstance
  private serializer: DeviceTypeSerializer

  constructor (axiosApi: AxiosInstance, serializer: DeviceTypeSerializer) {
    this.axiosApi = axiosApi
    this.serializer = serializer
  }

  build (): DeviceTypeSearcher {
    return new DeviceTypeSearcher(this.axiosApi, this.serializer)
  }
}

export class DeviceTypeSearcher {
  private axiosApi: AxiosInstance
  private serializer: DeviceTypeSerializer

  constructor (axiosApi: AxiosInstance, serializer: DeviceTypeSerializer) {
    this.axiosApi = axiosApi
    this.serializer = serializer
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
      return this.serializer.convertJsonApiObjectListToModelList(response)
    })
  }
}
