/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020, 2021
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

import { DateTime } from 'luxon'
import { Contact } from '@/models/Contact'
import { DynamicLocationEndAction } from '@/models/DynamicLocationEndAction'
import { IJsonApiEntityWithOptionalId, IJsonApiRelationships, IJsonApiEntityWithOptionalAttributes, IJsonApiEntityWithoutDetailsDataDictList, IJsonApiEntityWithoutDetails } from '@/serializers/jsonapi/JsonApiTypes'

export class DynamicLocationEndActionSerializer {
  convertJsonApiRelationshipsModelList (
    relationships: IJsonApiRelationships,
    included: IJsonApiEntityWithOptionalAttributes[],
    possibleContacts: {[key: string]: Contact}
  ): DynamicLocationEndAction[] {
    const actionIds = []

    if (relationships.configuration_dynamic_location_end_actions) {
      const actionObject = relationships.configuration_dynamic_location_end_actions as IJsonApiEntityWithoutDetailsDataDictList
      if (actionObject.data && actionObject.data.length > 0) {
        for (const relationShipActionData of actionObject.data) {
          const actionId = relationShipActionData.id
          actionIds.push(actionId)
        }
      }
    }
    const result = []

    if (included && included.length > 0) {
      for (const includedEntry of included) {
        if (includedEntry.type === 'configuration_dynamic_location_end_action') {
          if (actionIds.includes(includedEntry.id) && includedEntry.relationships) {
            if (includedEntry.attributes) {
              const contactRelationshipData = includedEntry.relationships.contact.data as IJsonApiEntityWithoutDetails
              const action = DynamicLocationEndAction.createFromObject({
                id: includedEntry.id || '',
                description: includedEntry.attributes.description,
                endDate: DateTime.fromISO(includedEntry.attributes.end_date, { zone: 'UTC' }),
                contact: possibleContacts[contactRelationshipData.id]
              })
              result.push(action)
            }
          }
        }
      }
    }

    return result
  }

  convertModelToJsonApiData (configurationId: string, action: DynamicLocationEndAction) : IJsonApiEntityWithOptionalId {
    const data: any = {
      type: 'configuration_dynamic_location_end_action',
      attributes: {
        description: action.description,
        end_date: action.endDate!.setZone('UTC').toISO()
      },
      relationships: {
        contact: {
          data: {
            type: 'contact',
            id: action.contact!.id
          }
        },
        configuration: {
          data: {
            type: 'configuration',
            id: configurationId
          }
        }
      }
    }

    if (action.id) {
      data.id = action.id
    }

    return data
  }
}
