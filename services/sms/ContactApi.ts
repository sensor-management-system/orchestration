import { AxiosInstance } from 'axios'

import Contact from '@/models/Contact'

export default class ContactApi {
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

  newEntry.id = Number.parseInt(entry.id)
  newEntry.givenName = attributes.givenName || ''
  newEntry.familyName = attributes.familyName || ''
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
    return new ContactSearcher(this.axiosApi)
  }
}

export class ContactSearcher {
  private axiosApi: AxiosInstance

  constructor (axiosApi: AxiosInstance) {
    this.axiosApi = axiosApi
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
      const rawData = rawResponse.data
      const result: Contact[] = []

      for (const entry of rawData.data) {
        result.push(serverResponseToEntity(entry))
      }
      return result
    })
  }
}
