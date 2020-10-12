import { AxiosInstance } from 'axios'

import Compartment from '@/models/Compartment'
import { CompartmentSerializer } from '@/serializers/jsonapi/CompartmentSerializer'

export default class DeviceTypeApi {
  private axiosApi: AxiosInstance
  private serializer: CompartmentSerializer

  constructor (axiosInstance: AxiosInstance, cvBaseUrl: string | undefined) {
    this.axiosApi = axiosInstance
    this.serializer = new CompartmentSerializer(cvBaseUrl)
  }

  newSearchBuilder (): CompartmentSearchBuilder {
    return new CompartmentSearchBuilder(this.axiosApi, this.serializer)
  }

  findAll (): Promise<Compartment[]> {
    return this.newSearchBuilder().build().findMatchingAsList()
  }
}

export class CompartmentSearchBuilder {
  private axiosApi: AxiosInstance
  private serializer: CompartmentSerializer

  constructor (axiosApi: AxiosInstance, serializer: CompartmentSerializer) {
    this.axiosApi = axiosApi
    this.serializer = serializer
  }

  build (): CompartmentSearcher {
    return new CompartmentSearcher(this.axiosApi, this.serializer)
  }
}

export class CompartmentSearcher {
  private axiosApi: AxiosInstance
  private serializer: CompartmentSerializer

  constructor (axiosApi: AxiosInstance, serializer: CompartmentSerializer) {
    this.axiosApi = axiosApi
    this.serializer = serializer
  }

  findMatchingAsList (): Promise<Compartment[]> {
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
