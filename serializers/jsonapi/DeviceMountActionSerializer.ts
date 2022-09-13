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

import {
  IJsonApiRelationships,
  IJsonApiEntityWithoutDetails,
  IJsonApiEntityWithOptionalId,
  IJsonApiEntityListEnvelope,
  IJsonApiEntityEnvelope,
  IJsonApiEntity,
  IJsonApiEntityWithOptionalAttributes
} from '@/serializers/jsonapi/JsonApiTypes'

import { ContactSerializer } from '@/serializers/jsonapi/ContactSerializer'
import { DeviceSerializer } from '@/serializers/jsonapi/DeviceSerializer'
import { PlatformSerializer } from '@/serializers/jsonapi/PlatformSerializer'

import { Contact } from '@/models/Contact'
import { Device } from '@/models/Device'
import { Platform } from '@/models/Platform'
import { DeviceMountAction } from '@/models/DeviceMountAction'

export class DeviceMountActionSerializer {
  private contactSerializer: ContactSerializer
  private deviceSerializer: DeviceSerializer
  private platformSerializer: PlatformSerializer

  private contactLookup: {[idx: string]: Contact} = {}
  private platformLookup: {[idx: string]: Platform} = {}
  private deviceLookup: {[idx: string]: Device} = {}

  constructor () {
    this.contactSerializer = new ContactSerializer()
    this.deviceSerializer = new DeviceSerializer()
    this.platformSerializer = new PlatformSerializer()
  }

  convertModelToJsonApiData (configurationId: string, deviceMountAction: DeviceMountAction): IJsonApiEntityWithOptionalId {
    const data: any = {
      type: 'device_mount_action',
      attributes: {
        offset_x: deviceMountAction.offsetX,
        offset_y: deviceMountAction.offsetY,
        offset_z: deviceMountAction.offsetZ,
        begin_description: deviceMountAction.beginDescription,
        end_description: deviceMountAction.endDescription,
        begin_date: deviceMountAction.beginDate.setZone('UTC').toISO(),
        end_date: deviceMountAction.endDate ? deviceMountAction.endDate.setZone('UTC').toISO() : null
      },
      relationships: {
        device: {
          data: {
            type: 'device',
            id: deviceMountAction.device.id
          }
        },
        begin_contact: {
          data: {
            type: 'contact',
            id: deviceMountAction.beginContact.id
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
    if (deviceMountAction.endContact) {
      data.relationships.end_contact = {
        data: {
          type: 'contact',
          id: deviceMountAction.endContact ? deviceMountAction.endContact.id : null
        }
      }
    }

    if (deviceMountAction.parentPlatform) {
      data.relationships.parent_platform = {
        data: {
          type: 'platform',
          id: deviceMountAction.parentPlatform.id
        }
      }
    }

    if (deviceMountAction.id) {
      data.id = deviceMountAction.id
    }

    return data
  }

  convertJsonApiObjectToModel (jsonApiObject: IJsonApiEntityEnvelope): DeviceMountAction {
    if (jsonApiObject.included) {
      this.convertJsonApiIncluded(jsonApiObject.included)
    }
    return this.convertJsonApiEntityToModel(jsonApiObject.data)
  }

  convertJsonApiObjectListToModelList (jsonApiObjectList: IJsonApiEntityListEnvelope): DeviceMountAction[] {
    if (jsonApiObjectList.included) {
      this.convertJsonApiIncluded(jsonApiObjectList.included)
    }
    const data = jsonApiObjectList.data
    const result = []
    for (const deviceMountActionPayload of data) {
      result.push(
        this.convertJsonApiEntityToModel(deviceMountActionPayload)
      )
    }
    return result
  }

  private convertJsonApiIncluded (included: IJsonApiEntityWithOptionalAttributes[]): void {
    this.contactLookup = {}
    this.deviceLookup = {}
    this.platformLookup = {}

    for (const entity of included) {
      if (entity.type === 'contact') {
        const contact = this.contactSerializer.convertJsonApiDataToModel(entity)
        if (contact.id !== null) {
          this.contactLookup[contact.id] = contact
        }
      } else if (entity.type === 'platform') {
        const platform = this.platformSerializer.convertJsonApiDataToModel(entity, [])
        if (platform.platform.id !== null) {
          this.platformLookup[platform.platform.id] = platform.platform
        }
      } else if (entity.type === 'device') {
        const device = this.deviceSerializer.convertJsonApiDataToModel(entity, included)
        if (device.device.id !== null) {
          this.deviceLookup[device.device.id] = device.device
        }
      }
    }
  }

  private convertJsonApiEntityToModel (data: IJsonApiEntity): DeviceMountAction {
    const attributes = data.attributes
    const relationships = data.relationships as IJsonApiRelationships

    // device is mandatory
    const deviceRelationship = relationships.device as IJsonApiRelationships
    const deviceData = deviceRelationship.data as IJsonApiEntityWithoutDetails
    const deviceId = deviceData.id
    const device = this.deviceLookup[deviceId]

    // beginContact is mandatory
    const beginContactRelationship = relationships.begin_contact as IJsonApiRelationships
    const beginContactData = beginContactRelationship.data as IJsonApiEntityWithoutDetails
    const beginContactId = beginContactData.id
    const beginContact = this.contactLookup[beginContactId]

    let endContactId = null
    if (relationships.end_contact && relationships.end_contact.data) {
      const endContactData = relationships.end_contact.data as IJsonApiEntityWithoutDetails
      endContactId = endContactData.id
    }
    let endContact = null
    if (endContactId !== null && this.contactLookup[endContactId]) {
      endContact = this.contactLookup[endContactId]
    }

    let parentPlatformId = null
    if (relationships.parent_platform && relationships.parent_platform.data) {
      const parentPlatformData = relationships.parent_platform.data as IJsonApiEntityWithoutDetails
      parentPlatformId = parentPlatformData.id
    }
    let parentPlatform = null
    if (parentPlatformId !== null && this.platformLookup[parentPlatformId]) {
      parentPlatform = this.platformLookup[parentPlatformId]
    }

    const deviceMountAction = new DeviceMountAction(
      data.id || '',
      device,
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

    return deviceMountAction
  }
}
