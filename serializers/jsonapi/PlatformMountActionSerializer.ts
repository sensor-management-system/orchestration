/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2021 - 2022
 * - Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
 * - Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
 * - Tim Eder (UFZ, tim.eder@ufz.de)
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

import { IJsonApiRelationships, IJsonApiEntityWithoutDetails, IJsonApiEntityWithOptionalId, IJsonApiEntityListEnvelope } from '@/serializers/jsonapi/JsonApiTypes'

import { ContactSerializer } from '@/serializers/jsonapi/ContactSerializer'
import { PlatformSerializer } from '@/serializers/jsonapi/PlatformSerializer'

import { Contact } from '@/models/Contact'
import { Platform } from '@/models/Platform'
import { PlatformMountAction } from '@/models/PlatformMountAction'

export class PlatformMountActionSerializer {
  private contactSerializer: ContactSerializer
  private platformSerializer: PlatformSerializer

  constructor () {
    this.contactSerializer = new ContactSerializer()
    this.platformSerializer = new PlatformSerializer()
  }

  convertModelToJsonApiData (configurationId: string, platformMountAction: PlatformMountAction): IJsonApiEntityWithOptionalId {
    const data: any = {
      type: 'platform_mount_action',
      attributes: {
        offset_x: platformMountAction.offsetX,
        offset_y: platformMountAction.offsetY,
        offset_z: platformMountAction.offsetZ,
        begin_description: platformMountAction.beginDescription,
        end_description: platformMountAction.endDescription,
        begin_date: platformMountAction.beginDate.setZone('UTC').toISO(),
        end_date: platformMountAction.endDate === null ? null : platformMountAction.endDate.setZone('UTC').toISO()

      },
      relationships: {
        platform: {
          data: {
            type: 'platform',
            id: platformMountAction.platform.id
          }
        },
        begin_contact: {
          data: {
            type: 'contact',
            id: platformMountAction.beginContact.id
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

    if (platformMountAction.endContact) {
      data.relationships.end_contact = {
        data: {
          type: 'contact',
          id: platformMountAction.endContact ? platformMountAction.endContact.id : null
        }
      }
    }

    if (platformMountAction.parentPlatform) {
      data.relationships.parent_platform = {
        data: {
          type: 'platform',
          id: platformMountAction.parentPlatform.id
        }
      }
    }

    if (platformMountAction.id) {
      data.id = platformMountAction.id
    }

    return data
  }

  convertJsonApiObjectListToModelList (jsonApiObjectList: IJsonApiEntityListEnvelope): PlatformMountAction[] {
    const data = jsonApiObjectList.data

    const contactLookup: {[idx: string]: Contact} = {}
    const platformLookup: {[idx: string]: Platform} = {}

    for (const included of jsonApiObjectList.included || []) {
      if (included.type === 'contact') {
        const contact = this.contactSerializer.convertJsonApiDataToModel(included)
        if (contact.id !== null) {
          contactLookup[contact.id] = contact
        }
      } else if (included.type === 'platform') {
        const platform = this.platformSerializer.convertJsonApiDataToModel(included, [])
        if (platform.platform.id !== null) {
          platformLookup[platform.platform.id] = platform.platform
        }
      }
    }

    const result = []

    for (const platformMountActionPayload of data) {
      const attributes = platformMountActionPayload.attributes

      const relationships = platformMountActionPayload.relationships as IJsonApiRelationships

      // platform is mandatory
      const platformRelationship = relationships.platform as IJsonApiRelationships
      const platformData = platformRelationship.data as IJsonApiEntityWithoutDetails
      const platformId = platformData.id
      const platform = platformLookup[platformId]

      // beginContact is mandatory
      const beginContactRelationship = relationships.begin_contact as IJsonApiRelationships
      const beginContactData = beginContactRelationship.data as IJsonApiEntityWithoutDetails
      const beginContactId = beginContactData.id
      const beginContact = contactLookup[beginContactId]

      let endContactId = null
      if (relationships.end_contact && relationships.end_contact.data) {
        const endContactData = relationships.end_contact.data as IJsonApiEntityWithoutDetails
        endContactId = endContactData.id
      }
      let endContact = null
      if (endContactId !== null && contactLookup[endContactId]) {
        endContact = contactLookup[endContactId]
      }

      let parentPlatformId = null
      if (relationships.parent_platform && relationships.parent_platform.data) {
        const parentPlatformData = relationships.parent_platform.data as IJsonApiEntityWithoutDetails
        parentPlatformId = parentPlatformData.id
      }
      let parentPlatform = null
      if (parentPlatformId !== null && platformLookup[parentPlatformId]) {
        parentPlatform = platformLookup[parentPlatformId]
      }

      const platformMountAction = new PlatformMountAction(
        platformMountActionPayload.id || '',
        platform,
        parentPlatform,
        DateTime.fromISO(attributes?.begin_date, { zone: 'UTC' }),
        attributes?.end_date ? DateTime.fromISO(attributes?.end_date, { zone: 'UTC' }) : null,
        attributes?.offset_x || 0,
        attributes?.offset_y || 0,
        attributes?.offset_z || 0,
        beginContact,
        endContact,
        attributes?.begin_description || '',
        attributes?.end_description || ''
      )

      result.push(
        platformMountAction
      )
    }

    return result
  }
}
