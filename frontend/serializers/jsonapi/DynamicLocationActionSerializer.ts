/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2022 - 2023
 * - Maximilian Schaldach (UFZ, maximilian.schaldach@ufz.de)
 * - Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
 * - Helmholtz Centre for Environmental Research GmbH - UFZ
 *   (UFZ, https://www.ufz.de)
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

import {
  IJsonApiEntityWithOptionalId,
  IJsonApiRelationships,
  IJsonApiEntityWithOptionalAttributes,
  IJsonApiEntityWithoutDetails,
  IJsonApiEntityEnvelope, IJsonApiEntityListEnvelope, IJsonApiEntity
} from '@/serializers/jsonapi/JsonApiTypes'
import { DynamicLocationAction } from '@/models/DynamicLocationAction'
import { ContactSerializer } from '@/serializers/jsonapi/ContactSerializer'
import { DevicePropertySerializer } from '@/serializers/jsonapi/DevicePropertySerializer'

export class DynamicLocationActionSerializer {
  private contactSerializer: ContactSerializer = new ContactSerializer()
  private devicePropertySerializer: DevicePropertySerializer = new DevicePropertySerializer()

  convertJsonApiObjectListToModelList (jsonApiObjectList: IJsonApiEntityListEnvelope): DynamicLocationAction[] {
    const included = jsonApiObjectList.included || []
    return jsonApiObjectList.data.map((model: IJsonApiEntity) => {
      return this.convertJsonApiDataToModel(model, included)
    })
  }

  convertJsonApiObjectToModel (jsonApiObject: IJsonApiEntityEnvelope): DynamicLocationAction {
    const included = jsonApiObject.included || []
    return this.convertJsonApiDataToModel(jsonApiObject.data, included)
  }

  convertJsonApiDataToModel (jsonApiData: IJsonApiEntityWithOptionalAttributes, included: IJsonApiEntityWithOptionalAttributes[]): DynamicLocationAction {
    const attributes = jsonApiData.attributes
    const relationships = jsonApiData.relationships || {}
    const action: DynamicLocationAction = new DynamicLocationAction()

    let x: DeviceProperty | null = null
    let y: DeviceProperty | null = null
    let z: DeviceProperty | null = null
    let endContact = null

    action.id = jsonApiData.id.toString()

    if (attributes) {
      action.label = attributes.label || ''
      action.beginDescription = attributes.begin_description || ''
      action.endDescription = attributes.end_description || ''
      action.beginDate = DateTime.fromISO(attributes.begin_date, { zone: 'UTC' })
      action.endDate = attributes.end_date != null ? DateTime.fromISO(attributes.end_date, { zone: 'UTC' }) : null
      action.epsgCode = attributes.epsg_code || '4326'
      action.elevationDatumName = attributes.elevation_datum_name || 'MSL'
      action.elevationDatumUri = attributes.elevation_datum_uri || ''
    }

    const contactLookup: {[idx: string]: Contact} = {}
    const devicePropertyLookup: {[idx: string]: DeviceProperty} = {}

    for (const includedEntry of included) {
      if (includedEntry.type === 'contact') {
        const contact = this.contactSerializer.convertJsonApiDataToModel(includedEntry)
        if (contact.id !== null) {
          contactLookup[contact.id] = contact
        }
      }
      if (includedEntry.type === 'device_property') {
        const deviceProperty = this.devicePropertySerializer.convertJsonApiDataToModel(includedEntry)
        if (deviceProperty.id !== null) {
          devicePropertyLookup[deviceProperty.id] = deviceProperty
        }
      }
    }

    const beginContact = this.getBeginContact(relationships, contactLookup)

    if (relationships.end_contact && relationships.end_contact.data) {
      endContact = this.getEndContact(relationships, contactLookup)
    }

    if (relationships.x_property && relationships.x_property.data) {
      x = this.getX(relationships, devicePropertyLookup)
    }
    if (relationships.x_property && relationships.y_property.data) {
      y = this.getY(relationships, devicePropertyLookup)
    }
    if (relationships.x_property && relationships.z_property.data) {
      z = this.getZ(relationships, devicePropertyLookup)
    }

    action.beginContact = beginContact
    action.endContact = endContact

    action.x = x
    action.y = y
    action.z = z

    return action
  }

  private getBeginContact (relationships: IJsonApiRelationships, contactLookup: { [p: string]: Contact }) {
    const beginContactRelationship = relationships.begin_contact as IJsonApiRelationships
    return this.getContact(beginContactRelationship, contactLookup)
  }

  private getEndContact (relationships: IJsonApiRelationships, contactLookup: { [p: string]: Contact }) {
    const endContactRelationship = relationships.end_contact as IJsonApiRelationships
    return this.getContact(endContactRelationship, contactLookup)
  }

  private getContact (contactRelationship: IJsonApiRelationships, contactLookup: { [p: string]: Contact }) {
    const contactData = contactRelationship.data as IJsonApiEntityWithoutDetails
    const contactId = contactData.id
    return contactLookup[contactId]
  }

  private getX (relationships: IJsonApiRelationships, devicePropertyLookup: { [p: string]: DeviceProperty }) {
    const r = relationships.x_property as IJsonApiRelationships
    return this.getDeviceProperty(r, devicePropertyLookup)
  }

  private getY (relationships: IJsonApiRelationships, devicePropertyLookup: { [p: string]: DeviceProperty }) {
    const r = relationships.y_property as IJsonApiRelationships
    return this.getDeviceProperty(r, devicePropertyLookup)
  }

  private getZ (relationships: IJsonApiRelationships, devicePropertyLookup: { [p: string]: DeviceProperty }) {
    const r = relationships.z_property as IJsonApiRelationships
    return this.getDeviceProperty(r, devicePropertyLookup)
  }

  private getDeviceProperty (relationship: IJsonApiRelationships, devicePropertyLookup: { [p: string]: DeviceProperty }) {
    const data = relationship.data as IJsonApiEntityWithoutDetails
    const id = data.id
    return devicePropertyLookup[id]
  }

  convertModelToJsonApiData (configurationId: string, action: DynamicLocationAction): IJsonApiEntityWithOptionalId {
    const data: any = {
      type: 'configuration_dynamic_location_action',
      attributes: {
        label: action.label,
        begin_description: action.beginDescription,
        begin_date: action.beginDate!.setZone('UTC').toISO(),
        end_date: action.endDate !== null ? action.endDate.setZone('UTC').toISO() : null,
        end_description: action.endDescription,
        epsg_code: action.epsgCode,
        elevation_datum_uri: action.elevationDatumUri,
        elevation_datum_name: action.elevationDatumName
      },
      relationships: {
        begin_contact: {
          data: {
            type: 'contact',
            id: action.beginContact!.id
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

    if (action.endContact) {
      data.relationships.end_contact = {
        data: {
          type: 'contact',
          id: action.endContact!.id
        }
      }
    } else {
      data.relationships.end_contact = {
        data: null
      }
    }

    if (action.x) {
      data.relationships.x_property = {
        data: {
          type: 'device_property',
          id: action.x.id
        }
      }
    } else {
      data.relationships.x_property = { data: null }
    }

    if (action.y) {
      data.relationships.y_property = {
        data: {
          type: 'device_property',
          id: action.y.id
        }
      }
    } else {
      data.relationships.y_property = { data: null }
    }

    if (action.z) {
      data.relationships.z_property = {
        data: {
          type: 'device_property',
          id: action.z.id
        }
      }
    } else {
      data.relationships.z_property = { data: null }
    }

    if (action.id) {
      data.id = action.id
    }
    return data
  }
}
