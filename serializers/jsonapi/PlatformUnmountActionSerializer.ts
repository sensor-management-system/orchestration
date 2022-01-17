/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2021
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

import { IJsonApiRelationships, IJsonApiEntityWithOptionalAttributes, IJsonApiEntityWithoutDetailsDataDictList, IJsonApiEntityWithoutDetails, IJsonApiEntityWithOptionalId } from '@/serializers/jsonapi/JsonApiTypes'

import { Contact } from '@/models/Contact'
import { Platform } from '@/models/Platform'
import { PlatformUnmountAction } from '@/models/PlatformUnmountAction'

export class PlatformUnmountActionSerializer {
  convertJsonApiRelationshipsModelList (
    relationships: IJsonApiRelationships,
    included: IJsonApiEntityWithOptionalAttributes[],
    possibleContacts: {[key: string]: Contact},
    possiblePlatforms: {[key: string]: Platform}
  ): PlatformUnmountAction[] {
    const platformUnmountActionIds = []
    if (relationships.platform_unmount_actions) {
      const platformUnmountActionObject = relationships.platform_unmount_actions as IJsonApiEntityWithoutDetailsDataDictList
      if (platformUnmountActionObject.data && platformUnmountActionObject.data.length > 0) {
        for (const relationShipPlatformUnmountActionData of platformUnmountActionObject.data) {
          const platformUnmountActionId = relationShipPlatformUnmountActionData.id
          platformUnmountActionIds.push(platformUnmountActionId)
        }
      }
    }

    const result = []
    if (included && included.length > 0) {
      for (const includedEntry of included) {
        if (includedEntry.type === 'platform_unmount_action') {
          if (platformUnmountActionIds.includes(includedEntry.id) && includedEntry.relationships) {
            if (includedEntry.attributes) {
              const platformRelationshipData = includedEntry.relationships.platform.data as IJsonApiEntityWithoutDetails
              const platform = possiblePlatforms[platformRelationshipData.id]
              const contactRelationshipData = includedEntry.relationships.contact.data as IJsonApiEntityWithoutDetails
              const platformUnmountAction = PlatformUnmountAction.createFromObject({
                id: includedEntry.id || '',
                description: includedEntry.attributes.description,
                date: DateTime.fromISO(includedEntry.attributes.end_date, { zone: 'UTC' }),
                platform,
                contact: possibleContacts[contactRelationshipData.id]
              })
              result.push(platformUnmountAction)
            }
          }
        }
      }
    }

    return result
  }

  convertModelToJsonApiData (configurationId: string, platformUnmountAction: PlatformUnmountAction): IJsonApiEntityWithOptionalId {
    const data: any = {
      type: 'platform_unmount_action',
      attributes: {
        description: platformUnmountAction.description,
        end_date: platformUnmountAction.date.setZone('UTC').toISO()
      },
      relationships: {
        platform: {
          data: {
            type: 'platform',
            id: platformUnmountAction.platform.id
          }
        },
        contact: {
          data: {
            type: 'contact',
            id: platformUnmountAction.contact.id
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
    if (platformUnmountAction.id) {
      data.id = platformUnmountAction.id
    }

    return data
  }
}
