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
import { DeviceProperty } from '@/models/DeviceProperty'
import { MeasuringRange } from '@/models/MeasuringRange'

import { IJsonApiNestedElement, IJsonApiObject, IJsonApiObjectList, IJsonApiTypeIdAttributes, IJsonApiDataWithOptionalId } from '@/serializers/jsonapi/JsonApiTypes'

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

  convertJsonApiObjectToModel (jsonApiObject: IJsonApiObject): DeviceProperty {
    const data = jsonApiObject.data
    return this.convertJsonApiDataToModel(data)
  }

  convertJsonApiObjectListToModelList (jsonApiObjectList: IJsonApiObjectList): DeviceProperty[] {
    return jsonApiObjectList.data.map(this.convertJsonApiDataToModel)
  }

  convertJsonApiDataToModel (jsonApiData: IJsonApiTypeIdAttributes): DeviceProperty {
    const result = new DeviceProperty()
    result.id = jsonApiData.id.toString()
    result.measuringRange = new MeasuringRange(
      jsonApiData.attributes.measuring_range_min || null,
      jsonApiData.attributes.measuring_range_max || null
    )
    result.failureValue = jsonApiData.attributes.failure_value || null
    result.accuracy = jsonApiData.attributes.accuracy || null
    result.resolution = jsonApiData.attributes.resolution || null
    result.label = jsonApiData.attributes.label || ''
    result.unitUri = jsonApiData.attributes.unit_uri || ''
    result.unitName = jsonApiData.attributes.unit_name || ''
    result.compartmentUri = jsonApiData.attributes.compartment_uri || ''
    result.compartmentName = jsonApiData.attributes.compartment_name || ''
    result.propertyUri = jsonApiData.attributes.property_uri || ''
    result.propertyName = jsonApiData.attributes.property_name || ''
    result.samplingMediaUri = jsonApiData.attributes.sampling_media_uri || ''
    result.samplingMediaName = jsonApiData.attributes.sampling_media_name || ''
    result.resolutionUnitUri = jsonApiData.attributes.resolution_unit_uri || ''
    result.resolutionUnitName = jsonApiData.attributes.resolution_unit_name || ''

    return result
  }

  convertModelToJsonApiData (deviceProperty: DeviceProperty, deviceId: string): IJsonApiDataWithOptionalId {
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
