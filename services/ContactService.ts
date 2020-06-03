import axios from 'axios'
import Contact from '../models/Contact'

// must be replaced by something that filters the
// contacts that are part of a given project
export default class ContactService {
  static findAllContacts (): Promise<Contact[]> {
    return axios.get(process.env.backendUrl + '/sis/v1/contacts').then((rawResponse) => {
      const rawData = rawResponse.data
      const result: Contact[] = []

      for (const entry of rawData.data) {
        const attributes = entry.attributes
        const newEntry = Contact.createEmpty()

        newEntry.id = Number.parseInt(entry.id)
        newEntry.email = attributes.email
        // TODO: Consistant usage of camel/snake case
        // JSONAPI uses camelcase
        if (attributes.first_name) {
          newEntry.firstName = attributes.first_name
        }
        if (attributes.last_name) {
          newEntry.lastName = attributes.last_name
        }
        if (attributes.profile_link) {
          newEntry.profileLink = attributes.profile_link
        }
        result.push(newEntry)
      }

      return result
    })
  }
}
