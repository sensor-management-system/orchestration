import Contact from '@/models/Contact'

export default class ContactSerializer {
  convertJsonApiObjectToModel (jsonApiObject: any): Contact {
    const data = jsonApiObject.data
    return this.convertJsonApiDataToModel(data)
  }

  convertJsonApiDataToModel (jsonApiData: any): Contact {
    const attributes = jsonApiData.attributes

    const newEntry = Contact.createEmpty()

    newEntry.id = jsonApiData.id
    newEntry.givenName = attributes.given_name || ''
    newEntry.familyName = attributes.family_name || ''
    newEntry.website = attributes.website || ''
    newEntry.email = attributes.email

    return newEntry
  }

  convertJsonApiObjectListToModelList (jsonApiObjectList: any): Contact[] {
    return jsonApiObjectList.data.map(this.convertJsonApiDataToModel)
  }

  convertModelListToJsonApiRelationshipObject (contacts: Contact[]): any {
    return {
      contacts: {
        data: this.convertModelListToTupleListWithIdAndType(contacts)
      }
    }
  }

  convertModelListToTupleListWithIdAndType (contacts: Contact[]): any {
    const result = []
    for (const contact of contacts) {
      result.push({
        id: contact.id,
        type: 'contact'
      })
    }
    return result
  }

  convertJsonApiRelationshipsModelList (relationships: any, included: any[]): Contact[] {
    const contactIds = []
    if (relationships.contacts && relationships.contacts.data && relationships.contacts.data.length > 0) {
      for (const relationShipContactData of relationships.contacts.data) {
        const contactId = relationShipContactData.id
        contactIds.push(contactId)
      }
    }

    const possibleContacts: {[key: string]: Contact} = {}
    if (included && included.length > 0) {
      for (const includedEntry of included) {
        if (includedEntry.type === 'contact') {
          const contactId = includedEntry.id
          if (contactIds.includes(contactId)) {
            const contact = this.convertJsonApiDataToModel(includedEntry)
            possibleContacts[contactId] = contact
          }
        }
      }
    }

    const contacts = []

    for (const contactId of contactIds) {
      if (possibleContacts[contactId]) {
        contacts.push(possibleContacts[contactId])
      } else {
        const contact = new Contact()
        contact.id = contactId
        contacts.push(contact)
      }
    }

    return contacts
  }
}
