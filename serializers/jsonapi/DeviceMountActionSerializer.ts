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
import { Device } from '@/models/Device'
import { DeviceMountAction } from '@/models/DeviceMountAction'
import { Platform } from '@/models/Platform'

export class DeviceMountActionSerializer {
  convertJsonApiRelationshipsModelList (
    relationships: IJsonApiRelationships,
    included: IJsonApiEntityWithOptionalAttributes[],
    possibleContacts: {[key: string]: Contact},
    possibleDevices: {[key: string]: Device},
    possiblePlatforms: {[key: string]: Platform}
  ): DeviceMountAction[] {
    const deviceMountActionIds = []
    if (relationships.device_mount_actions) {
      const deviceMountActionObject = relationships.device_mount_actions as IJsonApiEntityWithoutDetailsDataDictList
      if (deviceMountActionObject.data && deviceMountActionObject.data.length > 0) {
        for (const relationShipDeviceMountActionData of deviceMountActionObject.data) {
          const deviceMountActionId = relationShipDeviceMountActionData.id
          deviceMountActionIds.push(deviceMountActionId)
        }
      }
    }

    const result = []
    if (included && included.length > 0) {
      for (const includedEntry of included) {
        if (includedEntry.type === 'device_mount_action') {
          if (deviceMountActionIds.includes(includedEntry.id) && includedEntry.relationships) {
            if (includedEntry.attributes) {
              const deviceRelationshipData = includedEntry.relationships.device.data as IJsonApiEntityWithoutDetails
              const device = possibleDevices[deviceRelationshipData.id]
              let parentPlatform = null
              if (includedEntry.relationships.parent_platform &&
                includedEntry.relationships.parent_platform.data &&
                (includedEntry.relationships.parent_platform.data as IJsonApiEntityWithoutDetails).id
              ) {
                const parentPlatformRelationshipData = includedEntry.relationships.parent_platform.data as IJsonApiEntityWithoutDetails
                parentPlatform = possiblePlatforms[parentPlatformRelationshipData.id]
              }
              const contactRelationshipData = includedEntry.relationships.contact.data as IJsonApiEntityWithoutDetails
              const deviceMountAction = DeviceMountAction.createFromObject({
                id: includedEntry.id || '',
                offsetX: includedEntry.attributes.offset_x,
                offsetY: includedEntry.attributes.offset_y,
                offsetZ: includedEntry.attributes.offset_z,
                description: includedEntry.attributes.description,
                date: DateTime.fromISO(includedEntry.attributes.begin_date, { zone: 'UTC' }),
                device,
                parentPlatform,
                contact: possibleContacts[contactRelationshipData.id]
              })
              result.push(deviceMountAction)
            }
          }
        }
      }
    }

    return result
  }

  convertModelToJsonApiData (configurationId: string, deviceMountAction: DeviceMountAction): IJsonApiEntityWithOptionalId {
    const data: any = {
      type: 'device_mount_action',
      attributes: {
        offset_x: deviceMountAction.offsetX,
        offset_y: deviceMountAction.offsetY,
        offset_z: deviceMountAction.offsetZ,
        description: deviceMountAction.description,
        begin_date: deviceMountAction.date.setZone('UTC').toISO()
      },
      relationships: {
        device: {
          data: {
            type: 'device',
            id: deviceMountAction.device.id
          }
        },
        contact: {
          data: {
            type: 'contact',
            id: deviceMountAction.contact.id
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
}
