/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2022 - 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */

import { ContactRole, IContactRole } from '@/models/ContactRole'
import { Contact } from '@/models/Contact'
import { IJsonApiEntityListEnvelope, IJsonApiEntityWithoutDetails } from '@/serializers/jsonapi/JsonApiTypes'
import { ContactSerializer } from '@/serializers/jsonapi/ContactSerializer'

export class ContactRoleSerializer {
  convertJsonApiObjectListToModelList (jsonApiObjectList: IJsonApiEntityListEnvelope): ContactRole[] {
    const result: ContactRole[] = []

    const contactLookUpById: {[idx: string]: Contact} = {}
    for (const contactData of jsonApiObjectList.included || []) {
      if (contactData.type === 'contact') {
        const contact = new ContactSerializer().convertJsonApiDataToModel(contactData)
        contactLookUpById[contact.id!] = contact
      }
    }

    for (const contactRoleData of jsonApiObjectList.data) {
      const contactRelationship = contactRoleData.relationships!.contact.data as IJsonApiEntityWithoutDetails
      result.push(ContactRole.createFromObject({
        id: contactRoleData.id,
        roleName: contactRoleData.attributes.role_name,
        roleUri: contactRoleData.attributes.role_uri,
        contact: contactLookUpById[contactRelationship.id]
      }))
    }

    return result
  }

  convertModelToJsonApiData (contactRole: IContactRole, entityType: string, entityRelationshipType: string, entityRelationshipId: string) {
    const relationships: any = {
      contact: {
        data: {
          type: 'contact',
          id: contactRole.contact!.id
        }
      }
    }
    relationships[entityRelationshipType] = {
      data: {
        type: entityRelationshipType,
        id: entityRelationshipId
      }
    }

    const data = {
      type: entityType,
      attributes: {
        role_uri: contactRole.roleUri,
        role_name: contactRole.roleName
      },
      relationships
    }
    return data
  }
}
