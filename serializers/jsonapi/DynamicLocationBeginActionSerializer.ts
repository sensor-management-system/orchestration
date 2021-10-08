/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020, 2021
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
import { Contact } from '@/models/Contact'
import { DeviceProperty } from '@/models/DeviceProperty'

import { DynamicLocationBeginAction } from '@/models/DynamicLocationBeginAction'
import { IJsonApiEntityWithOptionalId, IJsonApiRelationships, IJsonApiEntityWithOptionalAttributes, IJsonApiEntityWithoutDetailsDataDictList, IJsonApiEntityWithoutDetails } from '@/serializers/jsonapi/JsonApiTypes'

export class DynamicLocationBeginActionSerializer {
  convertJsonApiRelationshipsModelList (
    relationships: IJsonApiRelationships,
    included: IJsonApiEntityWithOptionalAttributes[],
    possibleContacts: {[key: string]: Contact},
    possibleDeviceProperties: {[key: string]: DeviceProperty}
  ): DynamicLocationBeginAction[] {
    const actionIds = []

    if (relationships.configuration_dynamic_location_begin_actions) {
      const actionObject = relationships.configuration_dynamic_location_begin_actions as IJsonApiEntityWithoutDetailsDataDictList
      if (actionObject.data && actionObject.data.length > 0) {
        for (const relationShipActionData of actionObject.data) {
          const actionId = relationShipActionData.id
          actionIds.push(actionId)
        }
      }
    }
    const result = []

    if (included && included.length > 0) {
      for (const includedEntry of included) {
        if (includedEntry.type === 'configuration_dynamic_location_begin_action') {
          if (actionIds.includes(includedEntry.id) && includedEntry.relationships) {
            if (includedEntry.attributes) {
              const contactRelationshipData = includedEntry.relationships.contact.data as IJsonApiEntityWithoutDetails
              let x: DeviceProperty | null = null
              let y: DeviceProperty | null = null
              let z: DeviceProperty | null = null

              if (includedEntry.relationships.x_property.data) {
                const xProperty = includedEntry.relationships.x_property.data as IJsonApiEntityWithoutDetails
                if (xProperty.id) {
                  x = possibleDeviceProperties[xProperty.id]
                }
              }
              if (includedEntry.relationships.y_property.data) {
                const yProperty = includedEntry.relationships.y_property.data as IJsonApiEntityWithoutDetails
                if (yProperty.id) {
                  y = possibleDeviceProperties[yProperty.id]
                }
              }
              if (includedEntry.relationships.z_property.data) {
                const zProperty = includedEntry.relationships.z_property.data as IJsonApiEntityWithoutDetails
                if (zProperty.id) {
                  z = possibleDeviceProperties[zProperty.id]
                }
              }
              const action = DynamicLocationBeginAction.createFromObject({
                id: includedEntry.id || '',
                description: includedEntry.attributes.description,
                beginDate: DateTime.fromISO(includedEntry.attributes.begin_date, { zone: 'UTC' }),
                contact: possibleContacts[contactRelationshipData.id],
                epsgCode: includedEntry.attributes.epsg_code || '4326',
                elevationDatumName: includedEntry.attributes.elevation_datum_name || 'MSL',
                elevationDatumUri: includedEntry.attributes.elevation_datum_uri || '',
                x,
                y,
                z
              })
              result.push(action)
            }
          }
        }
      }
    }

    return result
  }

  convertModelToJsonApiData (configurationId: string, action: DynamicLocationBeginAction) : IJsonApiEntityWithOptionalId {
    const data: any = {
      type: 'configuration_dynamic_location_begin_action',
      attributes: {
        description: action.description,
        begin_date: action.beginDate!.setZone('UTC').toISO(),
        epsg_code: action.epsgCode,
        elevation_datum_uri: action.elevationDatumUri,
        elevation_datum_name: action.elevationDatumName
      },
      relationships: {
        contact: {
          data: {
            type: 'contact',
            id: action.contact!.id
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

    if (action.x) {
      data.relationships.x_property = {
        data: {
          type: 'device_property',
          id: action.x.id
        }
      }
    }

    if (action.y) {
      data.relationships.y_property = {
        data: {
          type: 'device_property',
          id: action.y.id
        }
      }
    }

    if (action.z) {
      data.relationships.z_property = {
        data: {
          type: 'device_property',
          id: action.z.id
        }
      }
    }

    if (action.id) {
      data.id = action.id
    }

    return data
  }
}
