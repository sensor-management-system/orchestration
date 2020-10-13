import Contact from '@/models/Contact'

import { IJsonApiObjectList, IJsonApiObject, IJsonApiTypeIdDataListDict, IJsonApiTypeIdAttributes } from '@/serializers/jsonapi/JsonApiTypes'

export interface IMissingContactData {
  ids: string[]
}

export interface IContactsAndMissing {
  contacts: Contact[]
  missing: IMissingContactData
}

export class ContactSerializer {
  convertJsonApiObjectToModel (jsonApiObject: IJsonApiObject): Contact {
    const data = jsonApiObject.data
    return this.convertJsonApiDataToModel(data)
  }

  convertJsonApiDataToModel (jsonApiData: IJsonApiTypeIdAttributes): Contact {
    const attributes = jsonApiData.attributes

    const newEntry = Contact.createEmpty()

    newEntry.id = jsonApiData.id
    newEntry.givenName = attributes.given_name || ''
    newEntry.familyName = attributes.family_name || ''
    newEntry.website = attributes.website || ''
    newEntry.email = attributes.email

    return newEntry
  }

  convertJsonApiObjectListToModelList (jsonApiObjectList: IJsonApiObjectList): Contact[] {
    return jsonApiObjectList.data.map(this.convertJsonApiDataToModel)
  }

  convertModelListToJsonApiRelationshipObject (contacts: Contact[]): IJsonApiTypeIdDataListDict {
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

  convertJsonApiRelationshipsModelList (relationships: IJsonApiTypeIdDataListDict, included: IJsonApiTypeIdAttributes[]): IContactsAndMissing {
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
    const missingDataForContactIds = []

    for (const contactId of contactIds) {
      if (possibleContacts[contactId]) {
        contacts.push(possibleContacts[contactId])
      } else {
        missingDataForContactIds.push(contactId)
      }
    }

    return {
      contacts,
      missing: {
        ids: missingDataForContactIds
      }
    }
  }
}
