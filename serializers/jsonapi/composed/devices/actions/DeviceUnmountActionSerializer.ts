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

import { DeviceUnmountAction } from '@/models/views/devices/actions/DeviceUnmountAction'

import {
  IJsonApiEntityListEnvelope, IJsonApiRelationshipsData, IJsonApiRelationships, IJsonApiEntityWithoutDetails
} from '@/serializers/jsonapi/JsonApiTypes'

import { ConfigurationBasicDataSerializer } from '@/serializers/jsonapi/basic/ConfigurationBasicDataSerializer'
import { ContactBasicDataSerializer } from '@/serializers/jsonapi/basic/ContactBasicDataSerializer'
import { DeviceUnmountActionBasicDataSerializer } from '@/serializers/jsonapi/basic/DeviceUnmountActionBasicDataSerializer'

export class DeviceUnmountActionSerializer {
  private deviceUnmountActionBasicDataSerializer: DeviceUnmountActionBasicDataSerializer
  private contactBasicDataSerializer: ContactBasicDataSerializer
  private configurationBasicDataSerializer: ConfigurationBasicDataSerializer

  constructor () {
    this.deviceUnmountActionBasicDataSerializer = new DeviceUnmountActionBasicDataSerializer()
    this.contactBasicDataSerializer = new ContactBasicDataSerializer()
    this.configurationBasicDataSerializer = new ConfigurationBasicDataSerializer()
  }

  convertJsonApiObjectListToModelList (jsonApiObjectList: IJsonApiEntityListEnvelope): DeviceUnmountAction[] {
    const data = jsonApiObjectList.data

    const contactByIdLookup: {[idx: string]: ContactBasicData} = {}
    const configurationByIdLookup: {[idx: string]: ConfigurationBasicData} = {}

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
      }
    }

    const result = []

    for (const deviceUnmountActionPayload of data) {
      const deviceUnmountActionBasic = this.deviceUnmountActionBasicDataSerializer.convertJsonApiDataToModel(deviceUnmountActionPayload)

      const relationships = deviceUnmountActionPayload.relationships as IJsonApiRelationships

      const configurationRelationship = relationships.configuration as IJsonApiRelationshipsData
      const configurationData = configurationRelationship.data as IJsonApiEntityWithoutDetails
      const configurationId = configurationData.id

      const contactRelationship = relationships.contact as IJsonApiRelationships
      const contactData = contactRelationship.data as IJsonApiEntityWithoutDetails
      const contactId = contactData.id

      if (configurationByIdLookup[configurationId] && contactByIdLookup[contactId]) {
        const configurationBasicData = configurationByIdLookup[configurationId]
        const contactBasicData = contactByIdLookup[contactId]

        result.push(
          new DeviceUnmountAction(deviceUnmountActionBasic, configurationBasicData, contactBasicData)
        )
      }
    }

    return result
  }
}
