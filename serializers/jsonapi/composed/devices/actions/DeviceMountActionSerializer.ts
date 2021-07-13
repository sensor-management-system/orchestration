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

import { ContactBasicData } from '@/models/basic/ContactBasicData'
import { ConfigurationBasicData } from '@/models/basic/ConfigurationBasicData'
import { PlatformBasicData } from '@/models/basic/PlatformBasicData'

import { DeviceMountAction } from '@/models/views/devices/actions/DeviceMountAction'

import {
  IJsonApiEntityListEnvelope, IJsonApiRelationshipsData, IJsonApiRelationships, IJsonApiEntityWithoutDetails
} from '@/serializers/jsonapi/JsonApiTypes'

import { ConfigurationBasicDataSerializer } from '@/serializers/jsonapi/basic/ConfigurationBasicDataSerializer'
import { ContactBasicDataSerializer } from '@/serializers/jsonapi/basic/ContactBasicDataSerializer'
import { DeviceMountActionBasicDataSerializer } from '@/serializers/jsonapi/basic/DeviceMountActionBasicDataSerializer'
import { PlatformBasicDataSerializer } from '@/serializers/jsonapi/basic/PlatformBasicDataSerializer'

export class DeviceMountActionSerializer {
  private deviceMountActionBasicDataSerializer: DeviceMountActionBasicDataSerializer
  private contactBasicDataSerializer: ContactBasicDataSerializer
  private configurationBasicDataSerializer: ConfigurationBasicDataSerializer
  private platformBasicDataSerializer: PlatformBasicDataSerializer

  constructor () {
    this.deviceMountActionBasicDataSerializer = new DeviceMountActionBasicDataSerializer()
    this.contactBasicDataSerializer = new ContactBasicDataSerializer()
    this.configurationBasicDataSerializer = new ConfigurationBasicDataSerializer()
    this.platformBasicDataSerializer = new PlatformBasicDataSerializer()
  }

  convertJsonApiObjectListToModelList (jsonApiObjectList: IJsonApiEntityListEnvelope): DeviceMountAction[] {
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

    for (const deviceMountActionPayload of data) {
      const deviceMountActionBasic = this.deviceMountActionBasicDataSerializer.convertJsonApiDataToModel(deviceMountActionPayload)

      const relationships = deviceMountActionPayload.relationships as IJsonApiRelationships

      const configurationRelationship = relationships.configuration as IJsonApiRelationshipsData
      const configurationData = configurationRelationship.data as IJsonApiEntityWithoutDetails
      const configurationId = configurationData.id

      const contactRelationship = relationships.contact as IJsonApiRelationships
      const contactData = contactRelationship.data as IJsonApiEntityWithoutDetails
      const contactId = contactData.id

      let parentPlatformId = null

      if (relationships.parent_platform && relationships.parent_platform.data) {
        const parentPlatformData = relationships.parent_platform.data as IJsonApiEntityWithoutDetails
        parentPlatformId = parentPlatformData.id
      }

      if (configurationByIdLookup[configurationId] && contactByIdLookup[contactId]) {
        const configurationBasicData = configurationByIdLookup[configurationId]
        const contactBasicData = contactByIdLookup[contactId]

        let parentPlatformBasicData = null

        if (parentPlatformId !== null && platformByIdLookup[parentPlatformId]) {
          parentPlatformBasicData = platformByIdLookup[parentPlatformId]
        }

        result.push(
          new DeviceMountAction(deviceMountActionBasic, configurationBasicData, contactBasicData, parentPlatformBasicData)
        )
      }
    }

    return result
  }
}
