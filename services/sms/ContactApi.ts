import axios, { AxiosInstance } from 'axios'

import Contact from '@/models/Contact'

const BASE_URL = process.env.smsBackendUrl + '/contacts'

export default class ContactApi {
  private axiosApi: AxiosInstance

  constructor (baseURL: string = BASE_URL) {
    this.axiosApi = axios.create({
      baseURL
    })
  }

  newSearchBuilder (): ContactSearchBuilder {
    return new ContactSearchBuilder(this.axiosApi)
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
