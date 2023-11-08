/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2021-2023
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
import { DeviceBasicData } from '@/models/basic/DeviceBasicData'
import { DeviceBasicDataSerializer } from '@/serializers/jsonapi/basic/DeviceBasicDataSerializer'

export class DeviceMountActionSerializer {
  private deviceMountActionBasicDataSerializer: DeviceMountActionBasicDataSerializer
  private contactBasicDataSerializer: ContactBasicDataSerializer
  private configurationBasicDataSerializer: ConfigurationBasicDataSerializer
  private platformBasicDataSerializer: PlatformBasicDataSerializer
  private deviceBasicDataSerializer: DeviceBasicDataSerializer

  constructor () {
    this.deviceMountActionBasicDataSerializer = new DeviceMountActionBasicDataSerializer()
    this.contactBasicDataSerializer = new ContactBasicDataSerializer()
    this.configurationBasicDataSerializer = new ConfigurationBasicDataSerializer()
    this.platformBasicDataSerializer = new PlatformBasicDataSerializer()
    this.deviceBasicDataSerializer = new DeviceBasicDataSerializer()
  }

  convertJsonApiObjectListToModelList (jsonApiObjectList: IJsonApiEntityListEnvelope): DeviceMountAction[] {
    const data = jsonApiObjectList.data

    const contactByIdLookup: {[idx: string]: ContactBasicData} = {}
    const configurationByIdLookup: {[idx: string]: ConfigurationBasicData} = {}
    const platformByIdLookup: {[idx: string]: PlatformBasicData} = {}
    const deviceByIdLookup: {[idx: string]: DeviceBasicData} = {}

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
      } else if (included.type === 'device') {
        const deviceBasicData = this.deviceBasicDataSerializer.convertJsonApiDataToModel(included)
        if (deviceBasicData.id !== null) {
          deviceByIdLookup[deviceBasicData.id] = deviceBasicData
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

      const beginContactRelationship = relationships.begin_contact as IJsonApiRelationships
      const beginContactData = beginContactRelationship.data as IJsonApiEntityWithoutDetails
      const beginContactId = beginContactData.id

      let parentPlatformId = null
      let parentDeviceId = null

      if (relationships.parent_platform && relationships.parent_platform.data) {
        const parentPlatformData = relationships.parent_platform.data as IJsonApiEntityWithoutDetails
        parentPlatformId = parentPlatformData.id
      }
      if (relationships.parent_device && relationships.parent_device.data) {
        const parentDeviceData = relationships.parent_device.data as IJsonApiEntityWithoutDetails
        parentDeviceId = parentDeviceData.id
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
        let parentDeviceBasicData = null

        if (parentPlatformId !== null && platformByIdLookup[parentPlatformId]) {
          parentPlatformBasicData = platformByIdLookup[parentPlatformId]
        } else if (parentDeviceId !== null && deviceByIdLookup[parentDeviceId]) {
          parentDeviceBasicData = deviceByIdLookup[parentDeviceId]
        }

        let endContactData = null
        if (endContactId !== null && contactByIdLookup[endContactId]) {
          endContactData = contactByIdLookup[endContactId]
        }

        result.push(
          new DeviceMountAction(deviceMountActionBasic, configurationBasicData, contactBasicData, endContactData, parentPlatformBasicData, parentDeviceBasicData)
        )
      }
    }

    return result
  }
}
