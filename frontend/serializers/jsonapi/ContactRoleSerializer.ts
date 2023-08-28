/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2022
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
