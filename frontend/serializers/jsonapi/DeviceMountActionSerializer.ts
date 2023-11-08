/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2021 - 2023
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

    if (deviceMountAction.parentDevice) {
      data.relationships.parent_device = {
        data: {
          type: 'device',
          id: deviceMountAction.parentDevice.id
        }
      }
    }

    if (deviceMountAction.id) {
      data.id = deviceMountAction.id
    }

    return data
  }

  convertJsonApiObjectToModel (jsonApiObject: IJsonApiEntityEnvelope): DeviceMountAction {
    const included = jsonApiObject.included || []
    return this.convertJsonApiDataToModel(jsonApiObject.data, included)
  }

  convertJsonApiObjectListToModelList (jsonApiObjectList: IJsonApiEntityListEnvelope): DeviceMountAction[] {
    const included = jsonApiObjectList.included || []

    return jsonApiObjectList.data.map((model: IJsonApiEntity) => {
      return this.convertJsonApiDataToModel(model, included)
    })
  }

  convertJsonApiDataToModel (jsonApiData: IJsonApiEntityWithOptionalAttributes, included: IJsonApiEntityWithOptionalAttributes[]): DeviceMountAction {
    const contactLookup: {[idx: string]: Contact} = {}
    const platformLookup: {[idx: string]: Platform} = {}
    const deviceLookup: {[idx: string]: Device} = {}

    const attributes = jsonApiData.attributes
    const relationships = jsonApiData.relationships as IJsonApiRelationships

    for (const includedEntry of included) {
      if (includedEntry.type === 'contact') {
        const contact = this.contactSerializer.convertJsonApiDataToModel(includedEntry)
        if (contact.id !== null) {
          contactLookup[contact.id] = contact
        }
      } else if (includedEntry.type === 'platform') {
        const platform = this.platformSerializer.convertJsonApiDataToModel(includedEntry, [])
        if (platform.platform.id !== null) {
          platformLookup[platform.platform.id] = platform.platform
        }
      } else if (includedEntry.type === 'device') {
        const device = this.deviceSerializer.convertJsonApiDataToModel(includedEntry, included)
        if (device.device.id !== null) {
          deviceLookup[device.device.id] = device.device
        }
      }
    }

    const device = this.getDevice(relationships, deviceLookup)
    const parentPlatform = this.getPlatform(relationships, platformLookup)
    const parentDevice = this.getParentDevice(relationships, deviceLookup)
    const beginContact = this.getBeginContact(relationships, contactLookup)
    const endContact = this.getEndContact(relationships, contactLookup)

    const result = new DeviceMountAction(
      jsonApiData.id.toString() || '',
      device,
      parentPlatform,
      parentDevice,
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

    return result
  }

  private getBeginContact (relationships: IJsonApiRelationships, contactLookup: { [p: string]: Contact }) {
    const beginContactRelationship = relationships.begin_contact as IJsonApiRelationships
    return this.getContact(beginContactRelationship, contactLookup)
  }

  private getEndContact (relationships: IJsonApiRelationships, contactLookup: { [p: string]: Contact }) {
    if (relationships.end_contact && relationships.end_contact.data) {
      const endContactRelationship = relationships.end_contact as IJsonApiRelationships
      return this.getContact(endContactRelationship, contactLookup)
    }

    return null
  }

  private getContact (contactRelationship: IJsonApiRelationships, contactLookup: { [p: string]: Contact }) {
    const contactData = contactRelationship.data as IJsonApiEntityWithoutDetails
    const contactId = contactData.id
    return contactLookup[contactId]
  }

  private getDevice (relationships: IJsonApiRelationships, lookup: { [p: string]: Device }) {
    const deviceRelationship = relationships.device as IJsonApiRelationships
    const deviceData = deviceRelationship.data as IJsonApiEntityWithoutDetails
    const deviceId = deviceData.id
    const device = lookup[deviceId]
    return device
  }

  private getParentDevice (relationships: IJsonApiRelationships, lookup: { [p: string]: Device }) {
    let parentDeviceId = null
    let parentDevice = null

    if (relationships.parent_device && relationships.parent_device.data) {
      const parentDeviceData = relationships.parent_device.data as IJsonApiEntityWithoutDetails
      parentDeviceId = parentDeviceData.id
    }

    if (parentDeviceId !== null && lookup[parentDeviceId]) {
      parentDevice = lookup[parentDeviceId]
    }

    return parentDevice
  }

  private getPlatform (relationships: IJsonApiRelationships, lookup: { [p: string]: Platform }) {
    let parentPlatformId = null
    let parentPlatform = null

    if (relationships.parent_platform && relationships.parent_platform.data) {
      const parentPlatformData = relationships.parent_platform.data as IJsonApiEntityWithoutDetails
      parentPlatformId = parentPlatformData.id
    }

    if (parentPlatformId !== null && lookup[parentPlatformId]) {
      parentPlatform = lookup[parentPlatformId]
    }

    return parentPlatform
  }
}
