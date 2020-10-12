import { AxiosInstance } from 'axios'

import Manufacturer from '@/models/Manufacturer'
import { ManufacturerSerializer } from '@/serializers/jsonapi/ManufacturerSerializer'

export default class ManufacturerApi {
  private axiosApi: AxiosInstance
  private serializer: ManufacturerSerializer

  constructor (axiosInstance: AxiosInstance, cvBaseUrl: string | undefined) {
    this.axiosApi = axiosInstance
    this.serializer = new ManufacturerSerializer(cvBaseUrl)
  }

  newSearchBuilder (): ManufacturerSearchBuilder {
    return new ManufacturerSearchBuilder(this.axiosApi, this.serializer)
  }

  findAll (): Promise<Manufacturer[]> {
    return this.newSearchBuilder().build().findMatchingAsList()
  }
}

export class ManufacturerSearchBuilder {
  private axiosApi: AxiosInstance
  private serializer: ManufacturerSerializer

  constructor (axiosApi: AxiosInstance, serializer: ManufacturerSerializer) {
    this.axiosApi = axiosApi
    this.serializer = serializer
  }

  build (): ManufacturerSearcher {
    return new ManufacturerSearcher(this.axiosApi, this.serializer)
  }
}

export class ManufacturerSearcher {
  private axiosApi: AxiosInstance
  private serializer: ManufacturerSerializer

  constructor (axiosApi: AxiosInstance, serializer: ManufacturerSerializer) {
    this.axiosApi = axiosApi
    this.serializer = serializer
  }

  findMatchingAsList (): Promise<Manufacturer[]> {
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
