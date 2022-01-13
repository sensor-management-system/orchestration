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
import { DeviceUnmountAction } from '@/models/DeviceUnmountAction'

export class DeviceUnmountActionSerializer {
  convertJsonApiRelationshipsModelList (
    relationships: IJsonApiRelationships,
    included: IJsonApiEntityWithOptionalAttributes[],
    possibleContacts: {[key: string]: Contact},
    possibleDevices: {[key: string]: Device}
  ): DeviceUnmountAction[] {
    const deviceUnmountActionIds = []
    if (relationships.device_unmount_actions) {
      const deviceUnmountActionObject = relationships.device_unmount_actions as IJsonApiEntityWithoutDetailsDataDictList
      if (deviceUnmountActionObject.data && deviceUnmountActionObject.data.length > 0) {
        for (const relationShipDeviceUnmountActionData of deviceUnmountActionObject.data) {
          const deviceUnmountActionId = relationShipDeviceUnmountActionData.id
          deviceUnmountActionIds.push(deviceUnmountActionId)
        }
      }
    }

    const result = []
    if (included && included.length > 0) {
      for (const includedEntry of included) {
        if (includedEntry.type === 'device_unmount_action') {
          if (deviceUnmountActionIds.includes(includedEntry.id) && includedEntry.relationships) {
            if (includedEntry.attributes) {
              const deviceRelationshipData = includedEntry.relationships.device.data as IJsonApiEntityWithoutDetails
              const device = possibleDevices[deviceRelationshipData.id]
              const contactRelationshipData = includedEntry.relationships.contact.data as IJsonApiEntityWithoutDetails
              const deviceUnmountAction = DeviceUnmountAction.createFromObject({
                id: includedEntry.id || '',
                description: includedEntry.attributes.description,
                date: DateTime.fromISO(includedEntry.attributes.end_date, { zone: 'UTC' }),
                device,
                contact: possibleContacts[contactRelationshipData.id]
              })
              result.push(deviceUnmountAction)
            }
          }
        }
      }
    }

    return result
  }

  convertModelToJsonApiData (configurationId: string, deviceUnmountAction: DeviceUnmountAction): IJsonApiEntityWithOptionalId {
    const data: any = {
      type: 'device_unmount_action',
      attributes: {
        description: deviceUnmountAction.description,
        end_date: deviceUnmountAction.date.setZone('UTC').toISO()
      },
      relationships: {
        device: {
          data: {
            type: 'device',
            id: deviceUnmountAction.device.id
          }
        },
        contact: {
          data: {
            type: 'contact',
            id: deviceUnmountAction.contact.id
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

    if (deviceUnmountAction.id) {
      data.id = deviceUnmountAction.id
    }

    return data
  }
}
