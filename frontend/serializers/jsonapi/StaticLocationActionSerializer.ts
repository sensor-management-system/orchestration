/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2022 - 2023
 * - Maximilian Schaldach <maximilian.schaldach@ufz.de>
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */

import { DateTime } from 'luxon'
import { ContactSerializer } from './ContactSerializer'
import {
  IJsonApiEntityWithOptionalId,
  IJsonApiEntityWithOptionalAttributes,
  IJsonApiEntityEnvelope,
  IJsonApiRelationships,
  IJsonApiEntityWithoutDetails,
  IJsonApiEntityListEnvelope,
  IJsonApiEntity
} from '@/serializers/jsonapi/JsonApiTypes'
import { StaticLocationAction } from '@/models/StaticLocationAction'
import { Contact } from '@/models/Contact'

export class StaticLocationActionSerializer {
  private contactSerializer: ContactSerializer = new ContactSerializer()

  convertJsonApiObjectListToModelList (jsonApiObjectList: IJsonApiEntityListEnvelope): StaticLocationAction[] {
    const included = jsonApiObjectList.included || []
    return jsonApiObjectList.data.map((model: IJsonApiEntity) => {
      return this.convertJsonApiDataToModel(model, included)
    })
  }

  convertJsonApiObjectToModel (jsonApiObject: IJsonApiEntityEnvelope): StaticLocationAction {
    const included = jsonApiObject.included || []
    return this.convertJsonApiDataToModel(jsonApiObject.data, included)
  }

  convertJsonApiDataToModel (jsonApiData: IJsonApiEntityWithOptionalAttributes, included: IJsonApiEntityWithOptionalAttributes[]): StaticLocationAction {
    const attributes = jsonApiData.attributes
    const relationships = jsonApiData.relationships || {}
    const action: StaticLocationAction = new StaticLocationAction()

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
      action.x = !isNaN(attributes.x) ? attributes.x : null
      action.y = !isNaN(attributes.y) ? attributes.y : null
      action.z = !isNaN(attributes.z) ? attributes.z : null
    }

    const contactLookup: {[idx: string]: Contact} = {}

    for (const includedEntry of included) {
      if (includedEntry.type === 'contact') {
        const contact = this.contactSerializer.convertJsonApiDataToModel(includedEntry)
        if (contact.id !== null) {
          contactLookup[contact.id] = contact
        }
      }
    }
    const beginContact = this.getBeginContact(relationships, contactLookup)
    let endContact = null
    if (relationships.end_contact && relationships.end_contact.data) {
      endContact = this.getEndContact(relationships, contactLookup)
    }

    action.beginContact = beginContact
    action.endContact = endContact

    if (relationships.configuration && relationships.configuration.data) {
      const configurationData = relationships.configuration.data as IJsonApiEntityWithoutDetails
      action.configurationId = configurationData.id || null
    }

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

  convertModelToJsonApiData (configurationId: string, action: StaticLocationAction): IJsonApiEntityWithOptionalId {
    const data: any = {
      type: 'configuration_static_location_action',
      attributes: {
        x: action.x,
        y: action.y,
        z: action.z,
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

    if (action.id) {
      data.id = action.id
    }

    return data
  }
}
