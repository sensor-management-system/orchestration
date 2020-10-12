import { DeviceProperty } from '@/models/DeviceProperty'
import { MeasuringRange } from '@/models/MeasuringRange'

export class DevicePropertySerializer {
  convertJsonApiElementToModel (property: any): DeviceProperty {
    const result = new DeviceProperty()
    result.id = property.id
    result.measuringRange = new MeasuringRange(
      property.measuring_range_min,
      property.measuring_range_max
    )
    result.failureValue = property.failure_value
    result.accuracy = property.accuracy
    result.label = property.label || ''
    result.unitUri = property.unit_uri || ''
    result.unitName = property.unit_name || ''
    result.compartmentUri = property.compartment_uri || ''
    result.compartmentName = property.compartment_name || ''
    result.propertyUri = property.property_uri || ''
    result.propertyName = property.property_name || ''
    result.samplingMediaUri = property.sampling_media_uri || ''
    result.samplingMediaName = property.sampling_media_name || ''

    return result
  }

  convertNestedJsonApiToModelList (properties: any[]): DeviceProperty[] {
    return properties.map(this.convertJsonApiElementToModel)
  }

  convertModelListToNestedJsonApiArray (properties: DeviceProperty[]): any[] {
    const result = []

    for (const property of properties) {
      const propertyToSave: any = {}
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
      propertyToSave.label = property.label
      propertyToSave.unit_uri = property.unitUri
      propertyToSave.unit_name = property.unitName
      propertyToSave.compartment_uri = property.compartmentUri
      propertyToSave.compartment_name = property.compartmentName
      propertyToSave.property_uri = property.propertyUri
      propertyToSave.property_name = property.propertyName
      propertyToSave.sampling_media_uri = property.samplingMediaUri
      propertyToSave.sampling_media_name = property.samplingMediaName

      result.push(propertyToSave)
    }

    return result
  }
}
