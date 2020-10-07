import { DeviceProperty } from '@/models/DeviceProperty'
import { MeasuringRange } from '@/models/MeasuringRange'

export default class DevicePropertySerializer {
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
}
