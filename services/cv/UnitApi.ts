import { AxiosInstance } from 'axios'

import { Unit } from '@/models/Unit'
import { UnitSerializer } from '@/serializers/jsonapi/UnitSerializer'

export class UnitApi {
  private axiosApi: AxiosInstance
  private serializer: UnitSerializer

  constructor (axiosInstance: AxiosInstance, cvBaseUrl: string | undefined) {
    this.axiosApi = axiosInstance
    this.serializer = new UnitSerializer(cvBaseUrl)
  }

  newSearchBuilder (): UnitSearchBuilder {
    return new UnitSearchBuilder(this.axiosApi, this.serializer)
  }

  findAll (): Promise<Unit[]> {
    return this.newSearchBuilder().build().findMatchingAsList()
  }
}

export class UnitSearchBuilder {
  private axiosApi: AxiosInstance
  private serializer: UnitSerializer

  constructor (axiosApi: AxiosInstance, serializer: UnitSerializer) {
    this.axiosApi = axiosApi
    this.serializer = serializer
  }

  build (): UnitSearcher {
    return new UnitSearcher(this.axiosApi, this.serializer)
  }
}

export class UnitSearcher {
  private axiosApi: AxiosInstance
  private serializer: UnitSerializer

  constructor (axiosApi: AxiosInstance, serializer: UnitSerializer) {
    this.axiosApi = axiosApi
    this.serializer = serializer
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
      return this.serializer.convertJsonApiObjectListToModelList(response)
    })
  }
}
