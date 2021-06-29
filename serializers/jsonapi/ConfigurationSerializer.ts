/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020-2021
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

import { Configuration } from '@/models/Configuration'
import { Contact } from '@/models/Contact'

import {
  IJsonApiEntityListEnvelope,
  IJsonApiEntityEnvelope,
  IJsonApiEntityWithOptionalId,
  IJsonApiEntityWithoutDetails,
  IJsonApiEntityWithOptionalAttributes,
  IJsonApiRelationships
} from '@/serializers/jsonapi/JsonApiTypes'

import { ContactSerializer, IMissingContactData } from '@/serializers/jsonapi/ContactSerializer'
import { PlatformMountActionSerializer } from '@/serializers/jsonapi/PlatformMountActionSerializer'
import { PlatformUnmountActionSerializer } from '@/serializers/jsonapi/PlatformUnmountActionSerializer'
import { DeviceMountActionSerializer } from '@/serializers/jsonapi/DeviceMountActionSerializer'
import { DeviceUnmountActionSerializer } from '@/serializers/jsonapi/DeviceUnmountActionSerializer'
import { DeviceSerializer } from '@/serializers/jsonapi/DeviceSerializer'
import { PlatformSerializer } from '@/serializers/jsonapi/PlatformSerializer'
import { DynamicLocation, StationaryLocation, LocationType } from '@/models/Location'
import { Platform } from '@/models/Platform'
import { Device } from '@/models/Device'
import { DeviceProperty } from '@/models/DeviceProperty'
import { DevicePropertySerializer } from './DevicePropertySerializer'

export interface IConfigurationMissingData {
  contacts: IMissingContactData
}

export interface IConfigurationWithMeta {
  configuration: Configuration
  missing: IConfigurationMissingData
}

export class ConfigurationSerializer {
  private contactSerializer: ContactSerializer = new ContactSerializer()
  private deviceSerializer: DeviceSerializer = new DeviceSerializer()
  private devicePropertySerializer: DevicePropertySerializer = new DevicePropertySerializer()
  private platformSerializer: PlatformSerializer = new PlatformSerializer()
  private platformMountActionSerializer: PlatformMountActionSerializer = new PlatformMountActionSerializer()
  private platformUnmountActionSerializer: PlatformUnmountActionSerializer = new PlatformUnmountActionSerializer()
  private deviceMountActionSerializer: DeviceMountActionSerializer = new DeviceMountActionSerializer()
  private deviceUnmountActionSerializer: DeviceUnmountActionSerializer = new DeviceUnmountActionSerializer()

  convertJsonApiObjectListToModelList (jsonApiObjectList: IJsonApiEntityListEnvelope): IConfigurationWithMeta[] {
    const included = jsonApiObjectList.included || []
    return jsonApiObjectList.data.map((model) => {
      return this.convertJsonApiDataToModel(model, included)
    })
  }

  convertJsonApiObjectToModel (jsonApiObject: IJsonApiEntityEnvelope): IConfigurationWithMeta {
    const included = jsonApiObject.included || []
    return this.convertJsonApiDataToModel(jsonApiObject.data, included)
  }

  convertJsonApiDataToModel (jsonApiData: IJsonApiEntityWithOptionalAttributes, included: IJsonApiEntityWithOptionalAttributes[]): IConfigurationWithMeta {
    const configuration = new Configuration()

    const attributes = jsonApiData.attributes
    const relationships = jsonApiData.relationships

    configuration.id = jsonApiData.id.toString()
    if (attributes) {
      configuration.label = attributes.label || ''
      configuration.projectUri = attributes.project_uri || ''
      configuration.projectName = attributes.project_name || ''
      configuration.status = attributes.status || ''

      configuration.startDate = attributes.start_date ? DateTime.fromISO(attributes.start_date, { zone: 'UTC' }) : null
      configuration.endDate = attributes.end_date ? DateTime.fromISO(attributes.end_date, { zone: 'UTC' }) : null
    }

    const deviceLookupById: {[idx: string]: Device} = {}
    const devices = this.deviceSerializer.convertJsonApiRelationshipsModelList(included)

    for (const device of devices) {
      const deviceId = device.id
      if (deviceId != null) {
        deviceLookupById[deviceId] = device
      }
    }

    const devicePropertyLookupById : {[idx: string]: DeviceProperty} = {}

    for (const includedEntry of included) {
      if (includedEntry.type === 'device_property') {
        const relationships = includedEntry.relationships
        if (relationships) {
          const deviceRelationship = relationships.device
          if (deviceRelationship) {
            const deviceRelationshipData = deviceRelationship.data as IJsonApiEntityWithoutDetails
            if (deviceRelationshipData) {
              const deviceId = deviceRelationshipData.id
              if (deviceLookupById[deviceId]) {
                const deviceProperty = this.devicePropertySerializer.convertJsonApiDataToModel(includedEntry)
                deviceLookupById[deviceId].properties.push(deviceProperty)

                if (deviceProperty.id) {
                  devicePropertyLookupById[deviceProperty.id] = deviceProperty
                }
              }
            }
          }
        }
      }
    }

    if (attributes && attributes.location_type === LocationType.Stationary) {
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
    } else if (attributes && attributes.location_type === LocationType.Dynamic) {
      const location = new DynamicLocation()
      const toCheck = [
        { key: 'src_latitude', setFunction (value: DeviceProperty) { location.latitude = value } },
        { key: 'src_longitude', setFunction (value: DeviceProperty) { location.longitude = value } },
        { key: 'src_elevation', setFunction (value: DeviceProperty) { location.elevation = value } }
      ]
      for (const check of toCheck) {
        if (relationships && relationships[check.key] && relationships[check.key].data) {
          const data = relationships[check.key].data as IJsonApiEntityWithoutDetails
          const id = data.id
          if (id != null && devicePropertyLookupById[id]) {
            check.setFunction(devicePropertyLookupById[id])
          }
        }
      }
      configuration.location = location
    }

    let missingDataForContactIds: string[] = []
    if (relationships) {
      const contactsWithMissing = this.contactSerializer.convertJsonApiRelationshipsModelList(relationships, included)
      configuration.contacts = contactsWithMissing.contacts
      missingDataForContactIds = contactsWithMissing.missing.ids
    }

    const platforms = this.platformSerializer.convertJsonApiRelationshipsModelList(included)

    const platformLookupById: {[idx: string]: Platform} = {}
    for (const platform of platforms) {
      const platformId = platform.id
      if (platformId != null) {
        platformLookupById[platformId] = platform
      }
    }

    const allPossibleContacts: {[key: string]: Contact} = {}
    const allPossibleDevices: {[key: string]: Device} = {}
    const allPossiblePlatforms: {[key: string]: Platform} = {}

    if (included && included.length > 0) {
      for (const includedEntry of included) {
        if (includedEntry.type === 'contact') {
          const contactId = includedEntry.id
          const contact = this.contactSerializer.convertJsonApiDataToModel(includedEntry)
          allPossibleContacts[contactId] = contact
        } else if (includedEntry.type === 'platform') {
          const platformId = includedEntry.id
          const platform = this.platformSerializer.convertJsonApiDataToModel(includedEntry, []).platform
          allPossiblePlatforms[platformId] = platform
        }
        // devices are already processed
      }
    }

    for (const deviceId of Object.keys(deviceLookupById)) {
      const device = deviceLookupById[deviceId]
      allPossibleDevices[deviceId] = device
    }

    if (relationships) {
      // seems to be necessary as the pure if clause isn't recognized by typescript to avoid undefined type
      const rs = relationships as IJsonApiRelationships
      configuration.platformMountActions = this.platformMountActionSerializer.convertJsonApiRelationshipsModelList(
        rs, included, allPossibleContacts, allPossiblePlatforms
      )
      configuration.platformUnmountActions = this.platformUnmountActionSerializer.convertJsonApiRelationshipsModelList(
        rs, included, allPossibleContacts, allPossiblePlatforms
      )
      configuration.deviceMountActions = this.deviceMountActionSerializer.convertJsonApiRelationshipsModelList(
        rs, included, allPossibleContacts, allPossibleDevices, allPossiblePlatforms
      )
      configuration.deviceUnmountActions = this.deviceUnmountActionSerializer.convertJsonApiRelationshipsModelList(
        rs, included, allPossibleContacts, allPossibleDevices
      )
    }

    return {
      configuration,
      missing: {
        contacts: {
          ids: missingDataForContactIds
        }
      }
    }
  }

  convertModelToJsonApiData (configuration: Configuration) : IJsonApiEntityWithOptionalId {
    const contacts = this.contactSerializer.convertModelListToJsonApiRelationshipObject(configuration.contacts)

    let locationAttributes = {}
    const locationRelationships: {[idx: string]: any} = {}

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
      const toAdd = [
        { key: 'src_latitude', value: location.latitude },
        { key: 'src_longitude', value: location.longitude },
        { key: 'src_elevation', value: location.elevation }
      ]
      for (const check of toAdd) {
        const key = check.key
        if (check.value != null) {
          locationRelationships[key] = {
            data: {
              id: check.value.id,
              type: 'device_property'
            }
          }
        }
      }
    }

    const result: IJsonApiEntityWithOptionalId = {
      attributes: {
        label: configuration.label,
        project_uri: configuration.projectUri,
        project_name: configuration.projectName,
        status: configuration.status,
        start_date: configuration.startDate != null ? configuration.startDate.setZone('UTC').toISO() : null,
        end_date: configuration.endDate != null ? configuration.endDate.setZone('UTC').toISO() : null,
        // TODO
        hierarchy: [],
        ...locationAttributes
      },
      relationships: {
        ...contacts,
        ...locationRelationships
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
