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

    const devices = this.deviceSerializer.convertJsonApiRelationshipsModelList(included)
    const platforms = this.platformSerializer.convertJsonApiRelationshipsModelList(included)

    const deviceLookupById: {[idx: string]: Device} = {}
    for (const device of devices) {
      const deviceId = device.id
      if (deviceId != null) {
        deviceLookupById[deviceId] = device
      }
    }

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
          calibrationDate: element.calibration_date != null ? new Date(element.calibration_date) : null,
          deviceProperties: []
        })

        listOfDeviceAttributes.push(deviceAttribute)
      }
    }
    const listOfPlatformAttributes: PlatformConfigurationAttributes[] = []
    const listOfDeviceAttributes: DeviceConfigurationAttributes[] = []
    const hierarchy: ConfigurationsTreeNode[] = []
    for (const childNode of jsonApiData.attributes.hierarchy || []) {
      addChildrenRecursivly(childNode, hierarchy, listOfPlatformAttributes, listOfDeviceAttributes)
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
            elementData.calibration_date = calibrationDate.toISOString()
          }
        }
        listOfChildren.push(elementData)
      }
    }
    for (const childNode of configuration.children) {
      addChildrenRecursivly(childNode, hierarchy)
    }

    const result: IJsonApiDataWithOptionalId = {
      attributes: {
        label: configuration.label,
        project_uri: configuration.projectUri,
        project_name: configuration.projectName,
        status: configuration.status,
        start_date: configuration.startDate != null ? configuration.startDate.toISOString() : null,
        end_date: configuration.endDate != null ? configuration.endDate.toISOString() : null,
        hierarchy,
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
