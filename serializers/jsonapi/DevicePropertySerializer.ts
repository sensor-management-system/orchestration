/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020
 * - Kotyba Alhaj Taha (UFZ, kotyba.alhaj-taha@ufz.de)
 * - Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
 * - Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
 * - Helmholtz Centre for Environmental Research GmbH - UFZ
 * (UFZ, https://www.ufz.de)
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
import { DeviceProperty, IDeviceProperty } from '@/models/DeviceProperty'
import { MeasuringRange } from '@/models/MeasuringRange'

import {
  IJsonApiNestedElement,
  IJsonApiEntityEnvelope,
  IJsonApiEntityListEnvelope,
  IJsonApiTypedEntityWithoutDetailsDataDictList,
  IJsonApiEntity,
  IJsonApiEntityWithoutDetails,
  IJsonApiRelationships,
  IJsonApiEntityWithOptionalId
} from '@/serializers/jsonapi/JsonApiTypes'

export interface IMissingDevicePropertyData {
  ids: string[]
}

export interface IDevicePropertiesAndMissing {
  properties: DeviceProperty[]
  missing: IMissingDevicePropertyData
}

export class DevicePropertySerializer {
  convertJsonApiElementToModel (property: IJsonApiNestedElement): DeviceProperty {
    const result = new DeviceProperty()
    result.id = property.id.toString()
    result.measuringRange = new MeasuringRange(
      property.measuring_range_min,
      property.measuring_range_max
    )
    result.failureValue = property.failure_value
    result.accuracy = property.accuracy
    result.resolution = property.resolution
    result.label = property.label || ''
    result.unitUri = property.unit_uri || ''
    result.unitName = property.unit_name || ''
    result.compartmentUri = property.compartment_uri || ''
    result.compartmentName = property.compartment_name || ''
    result.propertyUri = property.property_uri || ''
    result.propertyName = property.property_name || ''
    result.samplingMediaUri = property.sampling_media_uri || ''
    result.samplingMediaName = property.sampling_media_name || ''
    result.resolutionUnitUri = property.resolution_unit_uri || ''
    result.resolutionUnitName = property.resolution_unit_name || ''

    return result
  }

  convertNestedJsonApiToModelList (properties: IJsonApiNestedElement[]): DeviceProperty[] {
    return properties.map(this.convertJsonApiElementToModel)
  }

  convertModelListToNestedJsonApiArray (properties: DeviceProperty[]): IJsonApiNestedElement[] {
    const result = []

    for (const property of properties) {
      const propertyToSave: IJsonApiNestedElement = {}
      if (property.id != null) {
        // currently it seems that the id is always set to a higher value
        // I can set it to 8, but it will be saved with a new id (9)
        // there is already an issue for the backend, so hopefully it will be fixed there
        propertyToSave.id = property.id
      }

      propertyToSave.measuring_range_min = property.measuringRange.min
      propertyToSave.measuring_range_max = property.measuringRange.max
      propertyToSave.failure_value = property.failureValue
      propertyToSave.accuracy = property.accuracy
      propertyToSave.resolution = property.resolution
      propertyToSave.label = property.label
      propertyToSave.unit_uri = property.unitUri
      propertyToSave.unit_name = property.unitName
      propertyToSave.compartment_uri = property.compartmentUri
      propertyToSave.compartment_name = property.compartmentName
      propertyToSave.property_uri = property.propertyUri
      propertyToSave.property_name = property.propertyName
      propertyToSave.sampling_media_uri = property.samplingMediaUri
      propertyToSave.sampling_media_name = property.samplingMediaName
      propertyToSave.resolution_unit_uri = property.resolutionUnitUri
      propertyToSave.resolution_unit_name = property.resolutionUnitName

      result.push(propertyToSave)
    }

    return result
  }

  convertJsonApiObjectToModel (jsonApiObject: IJsonApiEntityEnvelope): DeviceProperty {
    const data = jsonApiObject.data
    return this.convertJsonApiDataToModel(data)
  }

  convertJsonApiObjectListToModelList (jsonApiObjectList: IJsonApiEntityListEnvelope): DeviceProperty[] {
    return jsonApiObjectList.data.map(this.convertJsonApiDataToModel)
  }

  convertModelListToJsonApiRelationshipObject (properties: DeviceProperty[]): IJsonApiTypedEntityWithoutDetailsDataDictList {
    return {
      device_properties: {
        data: this.convertModelListToTupleListWithIdAndType(properties)
      }
    }
  }

  convertJsonApiDataToModel (jsonApiData: IJsonApiEntity): DeviceProperty {
    const newEntry = new DeviceProperty()
    newEntry.id = jsonApiData.id.toString()
    newEntry.measuringRange = new MeasuringRange(
      jsonApiData.attributes.measuring_range_min || null,
      jsonApiData.attributes.measuring_range_max || null
    )
    newEntry.failureValue = jsonApiData.attributes.failure_value || null
    newEntry.accuracy = jsonApiData.attributes.accuracy || null
    newEntry.resolution = jsonApiData.attributes.resolution || null
    newEntry.label = jsonApiData.attributes.label || ''
    newEntry.unitUri = jsonApiData.attributes.unit_uri || ''
    newEntry.unitName = jsonApiData.attributes.unit_name || ''
    newEntry.compartmentUri = jsonApiData.attributes.compartment_uri || ''
    newEntry.compartmentName = jsonApiData.attributes.compartment_name || ''
    newEntry.propertyUri = jsonApiData.attributes.property_uri || ''
    newEntry.propertyName = jsonApiData.attributes.property_name || ''
    newEntry.samplingMediaUri = jsonApiData.attributes.sampling_media_uri || ''
    newEntry.samplingMediaName = jsonApiData.attributes.sampling_media_name || ''
    newEntry.resolutionUnitUri = jsonApiData.attributes.resolution_unit_uri || ''
    newEntry.resolutionUnitName = jsonApiData.attributes.resolution_unit_name || ''

    return newEntry
  }

  convertModelListToTupleListWithIdAndType (properties: IDeviceProperty[]): IJsonApiEntityWithoutDetails[] {
    const result: IJsonApiEntityWithoutDetails[] = []
    for (const property of properties) {
      if (property.id !== null) {
        result.push({
          id: property.id,
          type: 'device_property'
        })
      }
    }
    return result
  }

  convertJsonApiRelationshipsModelList (relationships: IJsonApiRelationships, included: IJsonApiEntity[]): IDevicePropertiesAndMissing {
    const devicePropertyIds = []
    if (relationships.device_properties) {
      const devicePropertyObject = relationships.device_properties
      if (devicePropertyObject.data && (devicePropertyObject.data as IJsonApiEntityWithoutDetails[]).length > 0) {
        for (const relationShipDevicePropertyData of (devicePropertyObject.data as IJsonApiEntityWithoutDetails[])) {
          const devicePropertyId = relationShipDevicePropertyData.id
          devicePropertyIds.push(devicePropertyId)
        }
      }
    }

    const possibleProperties: {[key: string]: DeviceProperty} = {}
    if (included && included.length > 0) {
      for (const includedEntry of included) {
        if (includedEntry.type === 'device_property') {
          const devicePropertyId = includedEntry.id
          if (devicePropertyIds.includes(devicePropertyId)) {
            const deviceProperty = this.convertJsonApiDataToModel(includedEntry)
            possibleProperties[devicePropertyId] = deviceProperty
          }
        }
      }
    }

    const properties = []
    const missingDataForDevicePropertyIds = []

    for (const devicePropertyId of devicePropertyIds) {
      if (possibleProperties[devicePropertyId]) {
        properties.push(possibleProperties[devicePropertyId])
      } else {
        missingDataForDevicePropertyIds.push(devicePropertyId)
      }
    }

    return {
      properties,
      missing: {
        ids: missingDataForDevicePropertyIds
      }
    }
  }

  convertModelToJsonApiData (deviceProperty: DeviceProperty, deviceId: string): IJsonApiEntityWithOptionalId {
    const data: any = {
      type: 'device_property',
      attributes: {
        measuring_range_min: deviceProperty.measuringRange.min,
        measuring_range_max: deviceProperty.measuringRange.max,
        failure_value: deviceProperty.failureValue,
        accuracy: deviceProperty.accuracy,
        resolution: deviceProperty.resolution,
        label: deviceProperty.label,
        unit_uri: deviceProperty.unitUri,
        unit_name: deviceProperty.unitName,
        compartment_uri: deviceProperty.compartmentUri,
        compartment_name: deviceProperty.compartmentName,
        property_uri: deviceProperty.propertyUri,
        property_name: deviceProperty.propertyName,
        sampling_media_uri: deviceProperty.samplingMediaUri,
        sampling_media_name: deviceProperty.samplingMediaName,
        resolution_unit_uri: deviceProperty.resolutionUnitUri,
        resolution_unit_name: deviceProperty.resolutionUnitName
      },
      relationships: {
        device: {
          data: {
            type: 'device',
            id: deviceId
          }
        }
      }
    }
    if (deviceProperty.id) {
      data.id = deviceProperty.id
    }
    return data
  }
}
