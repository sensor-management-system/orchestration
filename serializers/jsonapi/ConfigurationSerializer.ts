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

import { DateTime } from 'luxon'

import { Configuration } from '@/models/Configuration'
import { Contact } from '@/models/Contact'

import {
  IJsonApiEntityListEnvelope,
  IJsonApiEntityEnvelope,
  IJsonApiEntityWithOptionalId,
  IJsonApiEntityWithoutDetails,
  IJsonApiEntityWithOptionalAttributes
} from '@/serializers/jsonapi/JsonApiTypes'

import { ContactSerializer, IMissingContactData } from '@/serializers/jsonapi/ContactSerializer'
import { DeviceSerializer } from '@/serializers/jsonapi/DeviceSerializer'
import { PlatformSerializer } from '@/serializers/jsonapi/PlatformSerializer'
import { DynamicLocation, StationaryLocation, LocationType } from '@/models/Location'
import { PlatformNode } from '@/models/PlatformNode'
import { ConfigurationsTreeNode } from '@/models/ConfigurationsTreeNode'
import { DeviceNode } from '@/models/DeviceNode'
import { PlatformConfigurationAttributes } from '@/models/PlatformConfigurationAttributes'
import { DeviceConfigurationAttributes } from '@/models/DeviceConfigurationAttributes'
import { Platform } from '@/models/Platform'
import { Device } from '@/models/Device'
import { ConfigurationsTree } from '@/models/ConfigurationsTree'
import { DeviceProperty } from '@/models/DeviceProperty'

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
  private platformSerializer: PlatformSerializer = new PlatformSerializer()

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

    const devices = this.deviceSerializer.convertJsonApiRelationshipsModelList(included)
    const deviceLookupById: {[idx: string]: Device} = {}
    const devicePropertyLookupById : {[idx: string]: DeviceProperty} = {}

    for (const device of devices) {
      const deviceId = device.id
      if (deviceId != null) {
        deviceLookupById[deviceId] = device
      }
      for (const deviceProperty of device.properties) {
        const devicePropertyId = deviceProperty.id
        if (devicePropertyId != null) {
          devicePropertyLookupById[devicePropertyId] = deviceProperty
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

    // we get all the devices and platforms
    const platforms = this.platformSerializer.convertJsonApiRelationshipsModelList(included)

    const platformLookupById: {[idx: string]: Platform} = {}
    for (const platform of platforms) {
      const platformId = platform.id
      if (platformId != null) {
        platformLookupById[platformId] = platform
      }
    }

    const addChildrenRecursivly = (element: any, listOfChildren: ConfigurationsTreeNode[], listOfPlatformAttributes: PlatformConfigurationAttributes[], listOfDeviceAttributes: DeviceConfigurationAttributes[]) => {
      if (element.type === 'platform') {
        const id = String(element.id)
        const platform = platformLookupById[id]
        const platformNode = new PlatformNode(platform)
        listOfChildren.push(platformNode)

        const platformAttribute = PlatformConfigurationAttributes.createFromObject({
          platform,
          offsetX: element.offset_x || 0.0,
          offsetY: element.offset_y || 0.0,
          offsetZ: element.offset_z || 0.0
        })

        listOfPlatformAttributes.push(platformAttribute)

        if (element.children) {
          const children: ConfigurationsTreeNode[] = []
          for (const child of element.children) {
            addChildrenRecursivly(child, children, listOfPlatformAttributes, listOfDeviceAttributes)
          }
          platformNode.setTree(ConfigurationsTree.fromArray(children))
        }
      } else if (element.type === 'device') {
        const id = String(element.id)
        const device = deviceLookupById[id]
        const deviceNode = new DeviceNode(device)
        listOfChildren.push(deviceNode)

        const deviceAttribute = DeviceConfigurationAttributes.createFromObject({
          device,
          offsetX: element.offset_x || 0.0,
          offsetY: element.offset_y || 0.0,
          offsetZ: element.offset_z || 0.0,
          calibrationDate: element.calibration_date != null ? DateTime.fromISO(element.calibration_date, { zone: 'UTC' }) : null,
          firmwareVersion: element.firmware_version || ''
        })

        listOfDeviceAttributes.push(deviceAttribute)
      }
    }
    const listOfPlatformAttributes: PlatformConfigurationAttributes[] = []
    const listOfDeviceAttributes: DeviceConfigurationAttributes[] = []
    const hierarchy: ConfigurationsTreeNode[] = []
    if (jsonApiData.attributes) {
      for (const childNode of jsonApiData.attributes.hierarchy || []) {
        addChildrenRecursivly(childNode, hierarchy, listOfPlatformAttributes, listOfDeviceAttributes)
      }
    }

    configuration.children = hierarchy
    configuration.platformAttributes = listOfPlatformAttributes
    configuration.deviceAttributes = listOfDeviceAttributes

    return {
      configuration,
      missing: {
        contacts: {
          ids: missingDataForContactIds
        }
      }
    }
  }

  convertModelToJsonApiData (configuration: Configuration): IJsonApiEntityWithOptionalId {
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
        } else {
          // TODO: Figure out how to set those to be deleted then
        }
      }
    }

    const platformAttributeLookupById: {[index: string]: PlatformConfigurationAttributes} = {}
    for (const platformAttribute of configuration.platformAttributes) {
      const id = platformAttribute.platform.id
      if (id !== null) {
        platformAttributeLookupById[id] = platformAttribute
      }
    }
    const deviceAttributeLookupById: {[index: string]: DeviceConfigurationAttributes} = {}
    for (const deviceAttribute of configuration.deviceAttributes) {
      const id = deviceAttribute.device.id
      if (id !== null) {
        deviceAttributeLookupById[id] = deviceAttribute
      }
    }

    const hierarchy: any[] = []

    const addChildrenRecursivly = (node: ConfigurationsTreeNode, listOfChildren: any[]) => {
      if (node.isPlatform()) {
        const platformNode = node as PlatformNode
        const id = platformNode.unpack().id
        const elementData : any = {
          id,
          type: 'platform'
        }
        if (id != null && platformAttributeLookupById[id]) {
          elementData.offset_x = platformAttributeLookupById[id].offsetX
          elementData.offset_y = platformAttributeLookupById[id].offsetY
          elementData.offset_z = platformAttributeLookupById[id].offsetZ
        }
        const childrenList = platformNode.children
        if (childrenList.length > 0) {
          elementData.children = []
          for (const childNode of childrenList) {
            addChildrenRecursivly(childNode, elementData.children)
          }
        }
        listOfChildren.push(elementData)
      } else if (node.isDevice()) {
        const deviceNode = node as DeviceNode
        const id = deviceNode.unpack().id
        const elementData: any = {
          id,
          type: 'device'
        }
        if (id != null && deviceAttributeLookupById[id]) {
          elementData.offset_x = deviceAttributeLookupById[id].offsetX
          elementData.offset_y = deviceAttributeLookupById[id].offsetY
          elementData.offset_z = deviceAttributeLookupById[id].offsetZ

          const calibrationDate = deviceAttributeLookupById[id].calibrationDate
          if (calibrationDate != null) {
            elementData.calibration_date = calibrationDate.setZone('UTC').toISO()
          }
          elementData.firmware_version = deviceAttributeLookupById[id].firmwareVersion
        }
        listOfChildren.push(elementData)
      }
    }
    for (const childNode of configuration.children) {
      addChildrenRecursivly(childNode, hierarchy)
    }

    const result: IJsonApiEntityWithOptionalId = {
      attributes: {
        label: configuration.label,
        project_uri: configuration.projectUri,
        project_name: configuration.projectName,
        status: configuration.status,
        start_date: configuration.startDate != null ? configuration.startDate.setZone('UTC').toISO() : null,
        end_date: configuration.endDate != null ? configuration.endDate.setZone('UTC').toISO() : null,
        hierarchy,
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
