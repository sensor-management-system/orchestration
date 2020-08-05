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
  newEntry.email = attributes.email
  // TODO: Consistant usage of camel/snake case
  // JSONAPI uses camelcase
  if (attributes.first_name) {
    newEntry.givenName = attributes.first_name
  }
  if (attributes.last_name) {
    newEntry.familyName = attributes.last_name
  }
  if (attributes.profile_link) {
    newEntry.website = attributes.profile_link
  }

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
          'page[size]': 100000
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
