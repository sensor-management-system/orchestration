import { AxiosInstance } from 'axios'

import Property from '@/models/Property'
import PropertySerializer from '@/serializers/jsonapi/PropertySerializer'

export default class PropertyApi {
  private axiosApi: AxiosInstance
  private serializer: PropertySerializer

  constructor (axiosInstance: AxiosInstance, cvBaseUrl: string | undefined) {
    this.axiosApi = axiosInstance
    this.serializer = new PropertySerializer(cvBaseUrl)
  }

  newSearchBuilder (): PropertySearchBuilder {
    return new PropertySearchBuilder(this.axiosApi, this.serializer)
  }

  findAll (): Promise<Property[]> {
    return this.newSearchBuilder().build().findMatchingAsList()
  }
}

export class PropertySearchBuilder {
  private axiosApi: AxiosInstance
  private serializer: PropertySerializer

  constructor (axiosApi: AxiosInstance, serializer: PropertySerializer) {
    this.axiosApi = axiosApi
    this.serializer = serializer
  }

  build (): PropertySearcher {
    return new PropertySearcher(this.axiosApi, this.serializer)
  }
}

export class PropertySearcher {
  private axiosApi: AxiosInstance
  private serializer: PropertySerializer

  constructor (axiosApi: AxiosInstance, serializer: PropertySerializer) {
    this.axiosApi = axiosApi
    this.serializer = serializer
  }

  findMatchingAsList (): Promise<Property[]> {
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
