/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020
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

import { Configuration } from '@/models/Configuration'
import { Contact } from '@/models/Contact'

import { IJsonApiObjectList, IJsonApiObject, IJsonApiDataWithId, IJsonApiDataWithOptionalId, IJsonApiTypeIdAttributes } from '@/serializers/jsonapi/JsonApiTypes'

import { ContactSerializer, IMissingContactData } from '@/serializers/jsonapi/ContactSerializer'
import { DynamicLocation, StationaryLocation, LocationType } from '@/models/Location'

export interface IConfigurationMissingData {
  contacts: IMissingContactData
}

export interface IConfigurationWithMeta {
  configuration: Configuration
  missing: IConfigurationMissingData
}

export class ConfigurationSerializer {
  private contactSerializer: ContactSerializer = new ContactSerializer()

  convertJsonApiObjectListToModelList (jsonApiObjectList: IJsonApiObjectList): IConfigurationWithMeta[] {
    const included = jsonApiObjectList.included || []
    return jsonApiObjectList.data.map((model: IJsonApiDataWithId) => {
      return this.convertJsonApiDataToModel(model, included)
    })
  }

  convertJsonApiObjectToModel (jsonApiObject: IJsonApiObject): IConfigurationWithMeta {
    const included = jsonApiObject.included || []
    return this.convertJsonApiDataToModel(jsonApiObject.data, included)
  }

  convertJsonApiDataToModel (jsonApiData: IJsonApiDataWithId, included: IJsonApiTypeIdAttributes[]): IConfigurationWithMeta {
    const configuration = new Configuration()

    const attributes = jsonApiData.attributes
    const relationships = jsonApiData.relationships

    configuration.id = jsonApiData.id
    configuration.label = attributes.label || ''
    configuration.projectUri = attributes.project_uri || ''
    configuration.projectName = attributes.project_name || ''
    configuration.status = attributes.status || ''

    configuration.startDate = attributes.start_date ? new Date(attributes.start_date) : null
    configuration.endDate = attributes.end_date ? new Date(attributes.end_date) : null

    if (attributes.location_type === LocationType.Stationary) {
      const location = new StationaryLocation()
      if (attributes.longitude != null) { // allow 0 as real values as well
        location.longitude = attributes.longitude
      }
      if (attributes.latitude != null) { // allow 0 as real values as well
        location.latitude = attributes.latitude
      }
      if (attributes.elevation != null) {
        location.elevation = attributes.elevation
      }
      configuration.location = location
    } else if (attributes.location_type === LocationType.Dynamic) {
      const location = new DynamicLocation()
      // TODO: handle longitude_src_device_property
      // and for latitude & elevation as well
      configuration.location = location
    }

    const contactsWithMissing = this.contactSerializer.convertJsonApiRelationshipsModelList(relationships, included)
    configuration.contacts = contactsWithMissing.contacts
    const missingDataForContactIds = contactsWithMissing.missing.ids

    return {
      configuration,
      missing: {
        contacts: {
          ids: missingDataForContactIds
        }
      }
    }
  }

  convertModelToJsonApiData (configuration: Configuration): IJsonApiDataWithOptionalId {
    const contacts = this.contactSerializer.convertModelListToJsonApiRelationshipObject(configuration.contacts)

    let locationAttributes = {}

    const location = configuration.location
    if (location instanceof StationaryLocation) {
      locationAttributes = {
        location_type: LocationType.Stationary,
        longitude: location.longitude,
        latitude: location.latitude,
        elevation: location.elevation
      }
    } else if (location instanceof DynamicLocation) {
      locationAttributes = {
        location_type: LocationType.Dynamic
      }
      // TODO: Add location relationships for the device properties
    }

    const result: IJsonApiDataWithOptionalId = {
      attributes: {
        label: configuration.label,
        project_uri: configuration.projectUri,
        project_name: configuration.projectName,
        status: configuration.status,
        start_date: configuration.startDate != null ? configuration.startDate.toISOString() : null,
        end_date: configuration.endDate != null ? configuration.endDate.toISOString() : null,
        ...locationAttributes
      },
      relationships: {
        ...contacts
      },
      type: 'configuration'
    }
    if (configuration.id) {
      result.id = configuration.id
    }
    return result
  }
}

export const configurationWithMetaToConfigurationByThrowingErrorOnMissing = (configurationWithMeta: IConfigurationWithMeta) : Configuration => {
  const configuration = configurationWithMeta.configuration
  if (configurationWithMeta.missing.contacts.ids.length > 0) {
    throw new Error('Contacts are missing')
  }
  return configuration
}

export const configurationWithMetaToConfigurationByAddingDummyObjects = (configurationWithMeta: IConfigurationWithMeta) : Configuration => {
  const configuration = configurationWithMeta.configuration

  for (const missingContactId of configurationWithMeta.missing.contacts.ids) {
    const contact = new Contact()
    contact.id = missingContactId
    configuration.contacts.push(contact)
  }
  return configuration
}
