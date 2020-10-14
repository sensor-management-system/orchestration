import { AxiosInstance } from 'axios'

import { Contact } from '@/models/Contact'
import { ContactSerializer } from '@/serializers/jsonapi/ContactSerializer'

export class ContactApi {
  private axiosApi: AxiosInstance

  constructor (axiosInstance: AxiosInstance) {
    this.axiosApi = axiosInstance
  }

  newSearchBuilder (): ContactSearchBuilder {
    return new ContactSearchBuilder(this.axiosApi)
  }

  findAll (): Promise<Contact[]> {
    return this.newSearchBuilder().build().findMatchingAsList()
  }
}

export function serverResponseToEntity (entry: any): Contact {
  const attributes = entry.attributes
  const newEntry = Contact.createEmpty()

  newEntry.id = entry.id
  newEntry.givenName = attributes.given_name || ''
  newEntry.familyName = attributes.family_name || ''
  newEntry.website = attributes.website || ''
  newEntry.email = attributes.email

  // todo: Check list of platforms, list of devices and the user

  return newEntry
}

export class ContactSearchBuilder {
  private axiosApi: AxiosInstance

  constructor (axiosApi: AxiosInstance) {
    this.axiosApi = axiosApi
  }

  build (): ContactSearcher {
    return new ContactSearcher(this.axiosApi, new ContactSerializer())
  }
}

export class ContactSearcher {
  private axiosApi: AxiosInstance
  private serializer: ContactSerializer

  constructor (axiosApi: AxiosInstance, serializer: ContactSerializer) {
    this.axiosApi = axiosApi
    this.serializer = serializer
  }

  findMatchingAsList (): Promise<Contact[]> {
    return this.axiosApi.get(
      // we use the base path
      '',
      {
        params: {
          'page[size]': 100000,
          sort: 'email'
        }
      }).then((rawResponse: any) => {
      return this.serializer.convertJsonApiObjectListToModelList(rawResponse.data)
    })
  }
}
