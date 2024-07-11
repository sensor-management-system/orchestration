/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2023
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
import { DateTime } from 'luxon'

import { Contact, IContact } from '@/models/Contact'

import {
  IJsonApiEntityListEnvelope,
  IJsonApiEntityEnvelope,
  IJsonApiEntityWithOptionalId,
  IJsonApiEntityWithOptionalAttributes,
  IJsonApiEntityWithoutDetails,
  IJsonApiRelationships,
  IJsonApiEntityWithoutDetailsDataDict,
  IJsonApiEntityWithoutDetailsDataDictList,
  IJsonApiTypedEntityWithoutDetailsDataDict,
  IJsonApiTypedEntityWithoutDetailsDataDictList
} from '@/serializers/jsonapi/JsonApiTypes'

export interface IMissingContactData {
  ids: string[]
}

export interface IMissingSingleContactData {
  id: string
}

export interface IContactsAndMissing {
  contacts: Contact[]
  missing: IMissingContactData
}

export interface IContactAndMissing {
  contact: Contact | null
  missing: IMissingSingleContactData
}

export class ContactSerializer {
  convertJsonApiObjectToModel (jsonApiObject: IJsonApiEntityEnvelope): Contact {
    const data = jsonApiObject.data
    return this.convertJsonApiDataToModel(data)
  }

  convertJsonApiDataToModel (jsonApiData: IJsonApiEntityWithOptionalAttributes): Contact {
    const attributes = jsonApiData.attributes

    const newEntry = Contact.createEmpty()

    newEntry.id = jsonApiData.id.toString()

    if (attributes) {
      newEntry.givenName = attributes.given_name || ''
      newEntry.familyName = attributes.family_name || ''
      newEntry.website = attributes.website || ''
      newEntry.organization = attributes.organization || ''
      newEntry.email = attributes.email
      newEntry.orcid = attributes.orcid || ''
      newEntry.createdAt = attributes.created_at != null ? DateTime.fromISO(attributes.created_at, { zone: 'UTC' }) : null
      newEntry.updatedAt = attributes.updated_at != null ? DateTime.fromISO(attributes.updated_at, { zone: 'UTC' }) : null
    }

    const relationships = jsonApiData.relationships
    // just pick the contact from the relationships that is referenced by the created_by user
    if (relationships && relationships.created_by?.data && 'id' in relationships.created_by?.data) {
      const userId = (relationships.created_by.data as IJsonApiEntityWithoutDetails).id
      newEntry.createdByUserId = userId
    }

    return newEntry
  }

  convertJsonApiObjectListToModelList (jsonApiObjectList: IJsonApiEntityListEnvelope): Contact[] {
    return jsonApiObjectList.data.map(this.convertJsonApiDataToModel)
  }

  convertModelListToJsonApiRelationshipObject (contacts: IContact[]): IJsonApiTypedEntityWithoutDetailsDataDictList {
    return {
      contacts: {
        data: this.convertModelListToTupleListWithIdAndType(contacts)
      }
    }
  }

  convertModelToJsonApiRelationshipObject (contact: IContact): IJsonApiTypedEntityWithoutDetailsDataDict {
    return {
      contact: {
        data: this.convertModelToTupleWithIdAndType(contact)
      }
    }
  }

  convertModelToJsonApiData (contact: IContact): IJsonApiEntityWithOptionalId {
    const data: any = {
      type: 'contact',
      attributes: {
        given_name: contact.givenName,
        family_name: contact.familyName,
        email: contact.email,
        website: contact.website,
        organization: contact.organization,
        // We don't want it to be empty string, as this would make
        // the unique constraint problematic.
        // Using null is save here.
        orcid: contact.orcid ? contact.orcid : null
      }
    }
    if (contact.id) {
      data.id = contact.id
    }
    return data
  }

  convertModelListToTupleListWithIdAndType (contacts: IContact[]): IJsonApiEntityWithoutDetails[] {
    const result: IJsonApiEntityWithoutDetails[] = []
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

  convertModelToTupleWithIdAndType (contact: IContact): IJsonApiEntityWithoutDetails {
    return {
      id: contact.id || '',
      type: 'contact'
    }
  }

  convertJsonApiRelationshipsModelList (relationships: IJsonApiRelationships, included: IJsonApiEntityWithOptionalAttributes[]): IContactsAndMissing {
    const contactIds = []
    if (relationships.contacts) {
      const contactObject = relationships.contacts as IJsonApiEntityWithoutDetailsDataDictList
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

  convertJsonApiRelationshipsSingleModel (relationships: IJsonApiRelationships, included: IJsonApiEntityWithOptionalAttributes[]): IContactAndMissing {
    let relationContactId: string = ''
    if (relationships.contact) {
      const contactObject = relationships.contact as IJsonApiEntityWithoutDetailsDataDict
      if (contactObject.data && contactObject.data.id) {
        relationContactId = contactObject.data.id
      }
    }

    let serializedContact: Contact | null = null
    if (included && included.length > 0) {
      for (const includedEntry of included) {
        if (includedEntry.type !== 'contact') {
          continue
        }
        const contactId = includedEntry.id
        if (relationContactId === contactId) {
          serializedContact = this.convertJsonApiDataToModel(includedEntry)
        }
      }
    }

    return {
      contact: serializedContact,
      missing: {
        id: serializedContact ? '' : relationContactId
      }
    }
  }

  getContactFromIncludedByUserId (userId: string, included: IJsonApiEntityWithOptionalAttributes[]): Contact | undefined {
    const includedUser = included.find(item => item.type === 'user' && item.id === userId)
    if (includedUser && includedUser.relationships?.contact?.data) {
      const contactId = (includedUser.relationships.contact.data as IJsonApiEntityWithoutDetails).id
      const includedContact = included.find(item => item.type === 'contact' && item.id === contactId)
      if (includedContact) {
        return this.convertJsonApiDataToModel(includedContact)
      }
    }
  }
}
