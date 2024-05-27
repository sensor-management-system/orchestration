/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2021 - 2022
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */

import { ContactBasicData } from '@/models/basic/ContactBasicData'
import { ConfigurationBasicData } from '@/models/basic/ConfigurationBasicData'
import { PlatformBasicData } from '@/models/basic/PlatformBasicData'
import { PlatformMountAction } from '@/models/views/platforms/actions/PlatformMountAction'

import {
  IJsonApiEntityListEnvelope, IJsonApiRelationshipsData, IJsonApiRelationships, IJsonApiEntityWithoutDetails
} from '@/serializers/jsonapi/JsonApiTypes'

import { ConfigurationBasicDataSerializer } from '@/serializers/jsonapi/basic/ConfigurationBasicDataSerializer'
import { ContactBasicDataSerializer } from '@/serializers/jsonapi/basic/ContactBasicDataSerializer'
import { PlatformMountActionBasicDataSerializer } from '@/serializers/jsonapi/basic/PlatformMountActionBasicDataSerializer'
import { PlatformBasicDataSerializer } from '@/serializers/jsonapi/basic/PlatformBasicDataSerializer'

export class PlatformMountActionSerializer {
  private platformMountActionBasicDataSerializer: PlatformMountActionBasicDataSerializer
  private contactBasicDataSerializer: ContactBasicDataSerializer
  private configurationBasicDataSerializer: ConfigurationBasicDataSerializer
  private platformBasicDataSerializer: PlatformBasicDataSerializer

  constructor () {
    this.platformMountActionBasicDataSerializer = new PlatformMountActionBasicDataSerializer()
    this.contactBasicDataSerializer = new ContactBasicDataSerializer()
    this.configurationBasicDataSerializer = new ConfigurationBasicDataSerializer()
    this.platformBasicDataSerializer = new PlatformBasicDataSerializer()
  }

  convertJsonApiObjectListToModelList (jsonApiObjectList: IJsonApiEntityListEnvelope): PlatformMountAction[] {
    const data = jsonApiObjectList.data

    const contactByIdLookup: {[idx: string]: ContactBasicData} = {}
    const configurationByIdLookup: {[idx: string]: ConfigurationBasicData} = {}
    const platformByIdLookup: {[idx: string]: PlatformBasicData} = {}

    for (const included of jsonApiObjectList.included || []) {
      if (included.type === 'contact') {
        const contactBasicData = this.contactBasicDataSerializer.convertJsonApiDataToModel(included)
        if (contactBasicData.id !== null) {
          contactByIdLookup[contactBasicData.id] = contactBasicData
        }
      } else if (included.type === 'configuration') {
        const configurationBasicData = this.configurationBasicDataSerializer.convertJsonApiDataToModel(included)
        if (configurationBasicData.id !== null) {
          configurationByIdLookup[configurationBasicData.id] = configurationBasicData
        }
      } else if (included.type === 'platform') {
        const platformBasicData = this.platformBasicDataSerializer.convertJsonApiDataToModel(included)
        if (platformBasicData.id !== null) {
          platformByIdLookup[platformBasicData.id] = platformBasicData
        }
      }
    }

    const result = []

    for (const platformMountActionPayload of data) {
      const platformMountActionBasic = this.platformMountActionBasicDataSerializer.convertJsonApiDataToModel(platformMountActionPayload)

      const relationships = platformMountActionPayload.relationships as IJsonApiRelationships

      const configurationRelationship = relationships.configuration as IJsonApiRelationshipsData
      const configurationData = configurationRelationship.data as IJsonApiEntityWithoutDetails
      const configurationId = configurationData.id

      const beginContactRelationship = relationships.begin_contact as IJsonApiRelationships
      const beginContactData = beginContactRelationship.data as IJsonApiEntityWithoutDetails
      const beginContactId = beginContactData.id

      let parentPlatformId = null

      if (relationships.parent_platform && relationships.parent_platform.data) {
        const parentPlatformData = relationships.parent_platform.data as IJsonApiEntityWithoutDetails
        parentPlatformId = parentPlatformData.id
      }

      let endContactId = null

      if (relationships.end_contact && relationships.end_contact.data) {
        const endContactData = relationships.end_contact.data as IJsonApiEntityWithoutDetails
        endContactId = endContactData.id
      }

      if (configurationByIdLookup[configurationId] && contactByIdLookup[beginContactId]) {
        const configurationBasicData = configurationByIdLookup[configurationId]
        const contactBasicData = contactByIdLookup[beginContactId]

        let parentPlatformBasicData = null

        if (parentPlatformId !== null && platformByIdLookup[parentPlatformId]) {
          parentPlatformBasicData = platformByIdLookup[parentPlatformId]
        }

        let endContactData = null
        if (endContactId !== null && contactByIdLookup[endContactId]) {
          endContactData = contactByIdLookup[endContactId]
        }

        result.push(
          new PlatformMountAction(platformMountActionBasic, configurationBasicData, contactBasicData, endContactData, parentPlatformBasicData)
        )
      }
    }

    return result
  }
}
