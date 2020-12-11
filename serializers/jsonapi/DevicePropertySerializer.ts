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
import { DeviceProperty } from '@/models/DeviceProperty'
import { MeasuringRange } from '@/models/MeasuringRange'

import { IJsonApiNestedElement } from '@/serializers/jsonapi/JsonApiTypes'

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
}
