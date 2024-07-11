/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2023
 * - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
import { DeviceProperty, IDeviceProperty } from '@/models/DeviceProperty'
import { MeasuringRange } from '@/models/MeasuringRange'

import {
  IJsonApiAttributes,
  IJsonApiEntityEnvelope,
  IJsonApiEntityListEnvelope,
  IJsonApiTypedEntityWithoutDetailsDataDictList,
  IJsonApiEntityWithoutDetails,
  IJsonApiRelationships,
  IJsonApiEntityWithOptionalId,
  IJsonApiEntityWithOptionalAttributes
} from '@/serializers/jsonapi/JsonApiTypes'

export interface IMissingDevicePropertyData {
  ids: string[]
}

export interface IDevicePropertiesAndMissing {
  properties: DeviceProperty[]
  missing: IMissingDevicePropertyData
}

export class DevicePropertySerializer {
  convertModelListToNestedJsonApiArray (properties: DeviceProperty[]): IJsonApiAttributes[] {
    const result = []

    for (const property of properties) {
      const propertyToSave: IJsonApiAttributes = {}
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
      propertyToSave.accuracy_unit_uri = property.accuracyUnitUri
      propertyToSave.accuracy_unit_name = property.accuracyUnitName
      propertyToSave.resolution = property.resolution
      propertyToSave.label = property.label
      propertyToSave.unit_uri = property.unitUri
      propertyToSave.unit_name = property.unitName
      propertyToSave.compartment_uri = property.compartmentUri
      propertyToSave.compartment_name = property.compartmentName
      propertyToSave.property_uri = property.propertyUri
      propertyToSave.property_name = property.propertyName
      propertyToSave.aggregation_type_uri = property.aggregationTypeUri
      propertyToSave.aggregation_type_name = property.aggregationTypeName
      propertyToSave.sampling_media_uri = property.samplingMediaUri
      propertyToSave.sampling_media_name = property.samplingMediaName
      propertyToSave.resolution_unit_uri = property.resolutionUnitUri
      propertyToSave.resolution_unit_name = property.resolutionUnitName
      propertyToSave.description = property.description

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

  convertJsonApiDataToModel (jsonApiData: IJsonApiEntityWithOptionalAttributes): DeviceProperty {
    const newEntry = new DeviceProperty()
    newEntry.id = jsonApiData.id.toString()

    if (jsonApiData.attributes) {
      newEntry.measuringRange = new MeasuringRange(
        !isNaN(jsonApiData.attributes.measuring_range_min) ? jsonApiData.attributes.measuring_range_min : null,
        !isNaN(jsonApiData.attributes.measuring_range_max) ? jsonApiData.attributes.measuring_range_max : null
      )
      newEntry.failureValue = !isNaN(jsonApiData.attributes.failure_value) ? jsonApiData.attributes.failure_value : null
      newEntry.accuracy = !isNaN(jsonApiData.attributes.accuracy) ? jsonApiData.attributes.accuracy : null
      newEntry.resolution = !isNaN(jsonApiData.attributes.resolution) ? jsonApiData.attributes.resolution : null
      newEntry.label = jsonApiData.attributes.label || ''
      newEntry.unitUri = jsonApiData.attributes.unit_uri || ''
      newEntry.unitName = jsonApiData.attributes.unit_name || ''
      newEntry.compartmentUri = jsonApiData.attributes.compartment_uri || ''
      newEntry.compartmentName = jsonApiData.attributes.compartment_name || ''
      newEntry.propertyUri = jsonApiData.attributes.property_uri || ''
      newEntry.propertyName = jsonApiData.attributes.property_name || ''
      newEntry.aggregationTypeUri = jsonApiData.attributes.aggregation_type_uri || ''
      newEntry.aggregationTypeName = jsonApiData.attributes.aggregation_type_name || ''
      newEntry.samplingMediaUri = jsonApiData.attributes.sampling_media_uri || ''
      newEntry.samplingMediaName = jsonApiData.attributes.sampling_media_name || ''
      newEntry.accuracyUnitUri = jsonApiData.attributes.accuracy_unit_uri || ''
      newEntry.accuracyUnitName = jsonApiData.attributes.accuracy_unit_name || ''
      newEntry.resolutionUnitUri = jsonApiData.attributes.resolution_unit_uri || ''
      newEntry.resolutionUnitName = jsonApiData.attributes.resolution_unit_name || ''
      newEntry.description = jsonApiData.attributes.description || ''
    }

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

  convertJsonApiRelationshipsModelList (relationships: IJsonApiRelationships, included: IJsonApiEntityWithOptionalAttributes[]): IDevicePropertiesAndMissing {
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
        aggregation_type_uri: deviceProperty.aggregationTypeUri,
        aggregation_type_name: deviceProperty.aggregationTypeName,
        sampling_media_uri: deviceProperty.samplingMediaUri,
        sampling_media_name: deviceProperty.samplingMediaName,
        accuracy_unit_uri: deviceProperty.accuracyUnitUri,
        accuracy_unit_name: deviceProperty.accuracyUnitName,
        resolution_unit_uri: deviceProperty.resolutionUnitUri,
        resolution_unit_name: deviceProperty.resolutionUnitName,
        description: deviceProperty.description
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
