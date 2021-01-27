/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020
 * - Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
 * - Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for
 *   Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * Parts of this program were developed within the context of the
 * following publicly funded projects or measures:
 * - Helmholtz Earth and Environment DataHub
 *   (https://www.helmholtz.de/en/research/earth_and_environment/initiatives/#h51095)
 *
 * Licensed under the HEESIL, Version 1.0 or - as soon they will be
 * approved by the "Community" - subsequent versions of the HEESIL
 * (the "Licence").
 *
 * You may not use this work except in compliance with the Licence.
 *
 * You may obtain a copy of the Licence at:
 * https://gitext.gfz-potsdam.de/software/heesil
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the Licence is distributed on an "AS IS" basis,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
 * implied. See the Licence for the specific language governing
 * permissions and limitations under the Licence.
 */
import { Contact, IContact } from '@/models/Contact'

import { IJsonApiObjectList, IJsonApiObject, IJsonApiTypeIdDataListDict, IJsonApiTypeIdAttributes, IJsonApiTypeIdDataList, IJsonApiDataWithOptionalIdWithoutRelationships, IJsonApiTypeId } from '@/serializers/jsonapi/JsonApiTypes'

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

  convertModelListToJsonApiRelationshipObject (contacts: IContact[]): IJsonApiTypeIdDataListDict {
    return {
      contacts: {
        data: this.convertModelListToTupleListWithIdAndType(contacts)
      }
    }
  }

  convertModelToJsonApiData (contact: IContact): IJsonApiDataWithOptionalIdWithoutRelationships {
    const data: any = {
      type: 'contact',
      attributes: {
        given_name: contact.givenName,
        family_name: contact.familyName,
        email: contact.email,
        website: contact.website
      }
    }
    if (contact.id) {
      data.id = contact.id
    }
    return data
  }

  convertModelListToTupleListWithIdAndType (contacts: IContact[]): IJsonApiTypeId[] {
    const result: IJsonApiTypeId[] = []
    for (const contact of contacts) {
      if (contact.id !== null) {
        result.push({
          id: contact.id,
          type: 'contact'
        })
      }
    }
    return result
  }

  convertJsonApiRelationshipsModelList (relationships: IJsonApiTypeIdDataListDict, included: IJsonApiTypeIdAttributes[]): IContactsAndMissing {
    const contactIds = []
    if (relationships.contacts) {
      const contactObject = relationships.contacts as IJsonApiTypeIdDataList
      if (contactObject.data && contactObject.data.length > 0) {
        for (const relationShipContactData of contactObject.data) {
          const contactId = relationShipContactData.id
          contactIds.push(contactId)
        }
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
